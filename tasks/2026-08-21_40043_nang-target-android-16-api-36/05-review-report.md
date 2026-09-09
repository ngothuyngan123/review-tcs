# 05 — Review Report

## Thông tin

| Trường | Giá trị |
|---|---|
| Bug ID | `#40043 — Nâng target Android 16 (API 36) theo yêu cầu Google Play` (tracker **Feature**, không phải Bug) |
| Reviewer (Leader) | `<Leader ký tên>` — draft sinh bởi `/review-tc` 2026-08-21 |
| Tester được review | `haodtb` (Đoàn Thị Bích Hảo) — TC ghi vào Studio qua MCP |
| Ngày review | `2026-08-21` |
| Version TCs | `v1` (Studio task #172, `version = 1`, `round = 1`) |
| Vòng review | `Round 1` |
| Nguồn TCs | MCP LME TEST STUDIO `task_id = 172` — 50 TC, `provenance.source = human` |

> **Input thiếu 1**: `02-spec-reference.md` KHÔNG có → fallback `templates/LME-SYSTEM-SPEC.md`. Nhưng spec tổng **chỉ mô tả hệ web/backend**, mobile app chỉ xuất hiện dưới dạng "6 Mobile API endpoints" — **không có spec nào định nghĩa hành vi app mobile Android**. Hệ quả: mọi `Kết quả mong đợi` của 50 TC đều là **suy luận của tester, không có oracle spec**. Điều này khớp với việc `Trạng thái đánh giá spec` = null ở 100% TC.
>
> **Input thiếu 2**: `Commit / Pull Request` trống ở file 03 → không verify được fix shape thực tế (AP-4).
>
> **Input thiếu 3**: Không có ma trận thiết bị × OS bắt buộc; Studio không có field ghi model máy / phiên bản Android đã chạy.

---

## 1. Verdict

- [ ] **APPROVED** — TCs đạt, không cần chỉnh sửa
- [ ] **APPROVED WITH CHANGES** — Approve sau khi fix các issue MINOR (không cần review lại)
- [x] **REJECTED** — Có issue BLOCKER/MAJOR, cần fix và review lại

**Lý do ngắn gọn**: Bộ 50 TC có **bố cục tốt và bám sát mục 4 của Dev**, nhưng **mục tiêu chính của ticket chưa được verify lần nào** (6/6 TC nhóm Build & Compliance đều `skip`) và **37 kết quả "Đạt" không có evidence** (vi phạm RULE-02 → theo định nghĩa là *không được nghiệm thu*). Nghiêm trọng nhất: **không ai xác nhận bản app QA đã test chính là artifact target 36** — TC verify điều đó (`TC-FUNC001-10`) bị skip, nên 37 kết quả pass **có thể đã chạy trên build cũ**.

---

## 2. Tóm tắt cho member

Bộ TC này có nhiều điểm tốt: bám **đúng và đủ** 3 vùng "Trực tiếp" + 6 vùng "Gián tiếp" mà Dev nêu ở mục 4, chia màn hình rõ ràng (15 nhóm `screen`), và chủ động thêm cả những thứ Dev **không** liệt kê (edge-to-edge, runtime permission, cold/warm start) — đó là phản xạ tốt.

Vấn đề lớn nhất **không nằm ở việc viết TC mà ở việc chạy và chứng minh**: 12/50 TC không có kết luận (2 blocked + 9 skip + 1 chưa chạy), và toàn bộ nhóm verify *mục tiêu của ticket* (target 36, 16 KB, upload Play Console) đều bị skip — nghĩa là điều ticket này sinh ra để làm thì chưa ai kiểm chứng độc lập. Cùng lúc, 37 TC ghi "Đạt" nhưng cột Evidence trống hoàn toàn.

Về nội dung, điểm cần bổ sung nhiều nhất là **chiều sâu**: 44/50 TC là `Normal`, gần như không có `Abnormal`/`Boundary`. Đặc biệt với `predictive back` — thay đổi hành vi cốt lõi của target 36 — bộ TC mới test *back hoạt động bình thường*, chưa test *các màn cố tình chặn back* (chỗ Dev thực sự đã sửa code). Xem §5 để lấy 18 TC bổ sung copy thẳng vào file 04 (§5.1 ghi 4 TC đã được Leader loại và lý do).

---

## 3. Coverage Matrix

> Map impact suy luận từ `Tiêu đề test case` / `Điều kiện tiền đề` / `Các bước thực hiện` / `Kết quả mong đợi`.
> Cột **Thực thi** được thêm vì bộ TC này **đã chạy** — Leader cần thấy đồng thời "có TC" và "TC có kết luận không".

| Impact | Loại | Priority | TCs map | # TC | Thực thi | Status |
|---|---|---|---|---|---|---|
| **BUG** — mục tiêu compliance: app target API 36 + 16 KB page size + qua được Play Console | Fix | — | TC-FUNC001-08, -09, -10, TC-ENV003-01, -02 | 5 | **0 pass / 5 skip** | **GAP** |
| **F1** — Build config (compileSdk/targetSdk 35→36, versionCode 397) | Function | Direct | TC-FUNC001-10 (skip), TC-FUNC001-01, TC-COMPATLEGACY001-01 | 3 | 2 pass / 1 skip | **RISK** — TC verify trực tiếp bị skip; 2 TC pass chỉ gián tiếp |
| **F2** — Toolchain (AGP 8.9.1 / Gradle 8.11.1 / Kotlin 2.1.0 / google-services 4.4.2 / **crashlytics 3.0.2**) | Function | Direct | TC-FUNC001-08, -09 (skip); smoke gián tiếp: TC-MEDIA001-01..06, TC-SYNCAPP001-01..04, TC-FUNC001-04 | 12 | 10 pass / 2 skip | **RISK** — 2 TC verify trực tiếp skip. *(crashlytics 3.0.2 không có TC — Leader quyết định không cần, xem §5.1)* |
| **F3** — Manifest (gỡ `package=`, property portrait) | Function | Direct | TC-FUNC001-11 (skip), TC-UI002-01, -02, -03 | 4 | 1 pass / 1 skip / 2 blocked | **RISK** — 3/4 không kết luận |
| **F4** — Back xem ảnh chat (`WillPopScope` → `PopScope`) | Function | Direct | TC-REGSHARED001-06, -07, -08, -05 | 4 | 4 pass | **RISK** — chỉ test **1 màn Dev đã sửa**; không rà màn khác còn dùng `WillPopScope` (xem GAP-1) |
| **F5** — Lifecycle handler ("fix crash hidden state") | Function | Direct | TC-REGSHARED001-09, -10, -11, TC-UI003-01 | 4 | **4 pass** *(#11322 fail→pass 2026-08-21, xem §5.3)* | **RISK** — không TC nào nhắm đúng state `hidden`; cần re-test cả nhóm (`#11785`) |
| **F6** — iOS `project.pbxproj` bump version 397 | Function | Indirect | — | **0** | — | **GAP** (GAP-14) |
| **D0** — Data | Data | — | Dev khẳng định không ảnh hưởng data | — | — | N/A — nhưng xem GAP-16 (dữ liệu local sqflite/SharedPreferences sau rebuild) |
| **T1** — Nút Back / vuốt back **toàn app** | Feature | **High** | TC-REGSHARED001-02, -03, -04 | 3 | 3 pass | **RISK** — chỉ test route push/pop generic + root; "toàn app" chưa được rà (GAP-1) |
| **T2** — Xem ảnh trong chat | Feature | **High** | TC-REGSHARED001-06, -07, -08 | 3 | 3 pass | **OK** (chiều Normal đủ; thiếu Abnormal/Boundary → RULE-01) |
| **T3** — Khóa xoay tablet / máy gập | Feature | **High** | TC-UI002-02, -03 | 2 | **0 pass / 2 blocked** | **GAP** — impact High, **0 bằng chứng** |
| **T4** — Media (ảnh/video/audio/PDF) | Feature | Medium | TC-MEDIA001-01..06, TC-FUNC001-02, -03 | 8 | 8 pass | **RISK** — 8/8 Normal happy path; thiếu Abnormal/Boundary; **100% staging** (RULE-08) |
| **T5** — Realtime chat (Socket.IO) | Feature | Medium | TC-FUNC001-04, TC-REGSHARED001-12, TC-UI003-01 | 3 | 3 pass | **RISK** — không test mất kết nối kéo dài / reconnect backoff |
| **T6** — Push notification (FCM) + điều hướng | Feature | Medium | TC-SYNCAPP001-01..04, TC-UI003-04 | 5 | 5 pass | **OK** — cover foreground/background/terminated + quyền notification |
| **T7** — Booking salon / lesson / event | Feature | Medium | TC-FUNC001-05, -06, -07 | 3 | 3 pass | **RISK** — 3/3 happy path, precondition sạch (AP-3) |
| **T8** — Calendar (**shift ca qua đêm**) | Feature | Medium | TC-FUNCDATE001-01 | 1 | **1 pass** *(#11342 chạy 2026-08-21, xem §5.3)* | **RISK** — đã có bằng chứng đầu tiên, nhưng chỉ 1 TC Boundary; thiếu Normal + Abnormal (`#11782`, `#11783`) |
| **T9** — App lifecycle (khởi động / background / hidden) | Feature | Medium | TC-REGSHARED001-01, -09, -10, -11, TC-UI003-01 | 5 | **5 pass** *(xem §5.3)* | **RISK** — vẫn cần re-test cả nhóm theo RULE-12 (`#11785`) |
| **T10** — Tương thích ngược **Android 13 / 14 / 15** | Feature | **High** | TC-COMPATLEGACY001-02 (A13), -03 (A14), -04 (A15) | 3 | 1 pass / **2 skip** | **GAP** — Dev **yêu cầu rõ**, chỉ A15 được verify |
| **(ngoài mục 4)** — Edge-to-edge Android 16 | Feature | — | TC-UI001-01, -02 | 2 | 2 pass | **OK** — nhưng **Dev bỏ sót** impact này ở mục 4 (GAP-10) |
| **(ngoài mục 4)** — Runtime permission Android | Feature | — | TC-UI003-02, -03, -04 | 3 | 3 pass | **OK** — thiếu case **partial photo access** (GAP-11) |

### ORPHAN TCs

| TC ID | Title | Lý do orphan | Hành động đề xuất |
|---|---|---|---|
| — | — | **Không phát hiện ORPHAN.** Cả 50 TC đều map được về BUG / F1–F5 / T1–T10 hoặc về hành vi target-36 hợp lệ (edge-to-edge, runtime permission). | Giữ nguyên |

> ✅ **Điểm tốt đáng ghi nhận**: bộ TC **không** dính AP-5 (over-coverage layer downstream). Các TC booking/media/chat tuy không chạm code Dev sửa, nhưng **Dev đã chủ động liệt kê chúng là vùng smoke gián tiếp** ở mục 4 → nằm đúng scope regression, không phải case thừa.

---

## 3.5 Fix-shape analysis (adversarial)

| Mục | Giá trị |
|---|---|
| **Fix shape** (đọc mục 2 dev-impact) | **Migration / version-up** (chính) + **Sửa hàm dùng chung** (F4 `WillPopScope`→`PopScope`) + **Build/asset** (toàn bộ toolchain). **Không** phải generic catch-all / validation / race-condition / soft-delete. |
| **Trigger space cần cover** | (1) **Version-up**: nâng cấp app từ bản target 35 → 397, dữ liệu local + đăng nhập giữ nguyên, chạy được trên **A13 / A14 / A15 / A16** (4 nhánh OS). (2) **Shared-code**: **mọi màn còn dùng `WillPopScope` / `onWillPop` / có chặn back** — Dev **không cung cấp danh sách**. (3) **Build/asset**: artifact thật sự target 36, 16 KB align, **font/glyph JP + VN** sau rebuild. *(crashlytics 3.0.2 — Leader loại khỏi phạm vi, §5.1)* |
| **Số trigger TCs hiện cover** | Version-up: **2/4 OS nhánh cũ verify** (A15 pass; A13 + A14 skip). Shared-code: **1/N màn** (chỉ `image_gallery.dart`; N chưa biết vì thiếu danh sách Dev). Build/asset: **0/2** (build artifact skip · font/glyph 0 TC). |
| **KH report dạng** | **N/A** — ticket tracker **Feature**, không có báo cáo khách hàng. `description` Redmine trống. Không áp dụng AP-2 symptom-only. |
| **Alternative root causes cần verify** | **N/A** — root cause là yêu cầu tuân thủ Google Play, không phải lỗi cần đoán nguyên nhân. |
| **Anti-patterns dính** | **AP-3** (happy-path-only regression) · **AP-4** (thiếu PR link → không verify được fix shape thực tế) · **AP-6** (mục 3 không phải danh sách caller) |

### Câu hỏi adversarial bắt buộc — và câu trả lời từ bộ TC hiện tại

| Fix shape | Câu hỏi bắt buộc | Bộ TC hiện tại trả lời được? |
|---|---|---|
| **Migration / version-up** | Data cũ không mất? Lấy mẫu **nhiều thời điểm tạo**? Nhánh cũ chạy song song nhánh mới? | ⚠️ **Một phần** — `TC-COMPATLEGACY001-01` cover "nâng cấp không mất trạng thái" (1 TC, Normal, 1 nhánh OS). Không lấy mẫu app từ nhiều bản cũ. A13/A14 skip. |
| **Sửa hàm dùng chung** | Có **danh sách nơi ảnh hưởng do DEV cung cấp** không? TC test **từng nơi**? | 🔴 **KHÔNG** — mục 3 file 03 là log build/verify, **không phải danh sách caller**. Không TC nào rà các màn khác chặn back. → **BLOCKER GAP-1** |
| **Build / asset (JS/CSS/font/icon)** | Font **không fallback**, glyph kanji/kana + dấu tiếng Việt đủ (không tofu ロ)? Asset còn load đủ sau rebuild? | 🔴 **KHÔNG** — 0 TC về font/glyph/asset sau khi đổi toàn bộ build engine. → **MAJOR GAP-8** |
| **Media / file** | Có TC chạy **trên production** (media staging ≠ production)? | 🔴 **KHÔNG** — 8/8 TC media chạy `env = staging`. → **BLOCKER GAP-2** (RULE-08 / ENV-003) |

---

## 4. Issues phát hiện

### 4.1 Blocker (phải fix trước khi merge)

- **[BLOCKER] FIX-SHAPE — GAP-1 · `REG-SHARED-001`**: Fix F4 đổi `WillPopScope` → `PopScope` là **thay đổi hành vi dùng chung**: ở target 36 predictive back bật mặc định và `onBackPressed` **không còn được gọi**, nên **mọi màn còn dùng `WillPopScope`/`onWillPop` sẽ âm thầm mất handler chặn back**. Dev chỉ sửa `image_gallery.dart` và **không cung cấp danh sách nơi ảnh hưởng** (mục 3 file 03 là log build, không phải caller list). 12 TC `REG-SHARED-001` hiện có đều test back ở **màn không chặn back** (push/pop generic, root, image viewer) — **không TC nào test màn cố tình chặn back** (dialog "rời trang?", form nhập dở, upload đang chạy). `REG-SHARED-001` là quan điểm **Cao** và trigger **BẮT BUỘC**. — **Fix**: yêu cầu Dev `grep -rn "WillPopScope\|onWillPop\|PopScope" lib/` trên branch `master_branch_release_store` và xuất danh sách đầy đủ; thêm `TC-REGSHARED001-13/14/15` (§5) test **từng màn** trong danh sách.

- **[BLOCKER] GAP-3 · Mục tiêu ticket chưa được verify lần nào**: **6/6 TC nhóm "Build & Compliance Android" đều `skip`** (`TC-FUNC001-08`, `-09`, `-10`, `-11`, `TC-ENV003-01`, `-02`) — tức target 36, 16 KB page size, merged manifest, upload Play Console **chưa ai kiểm chứng độc lập**. Bằng chứng duy nhất là lời Dev tự khai ở mục 3 file 03; theo **RULE-11** đó không phải bằng chứng hợp lệ. — **Fix**: chạy đủ 6 TC này trước mọi thứ khác. Nếu QA không có Android toolchain thì phải có **phiếu xác nhận của Dev kèm artifact + output `aapt2 dump badging`** đính vào Evidence, không được để `skip` trắng.

- **[BLOCKER] GAP-4 · `RULE-02` — 37 kết quả "Đạt" không có evidence**: cột `Evidence thực tế` **trống 100%** (50/50 TC) và cột `Ghi chú` **không TC nào ghi loại evidence bắt buộc**. RULE-02 quy định: *"Chỉ tick Đạt khi đã đính kèm đúng loại bằng chứng... Không chấp nhận 'đã xem, OK'"*. Vi phạm RULE → **kết quả test không được nghiệm thu**, dù coverage có đủ. — **Fix**: bổ sung evidence cho toàn bộ 37 TC `Đạt` (screenshot/video máy thật + tên model + phiên bản Android), hoặc hạ về `Chưa test`.

- **[BLOCKER] GAP-5 · Không xác nhận bản app đã test là artifact target 36**: `TC-FUNC001-10` ("Xác nhận artifact khai báo compileSdk và targetSdk 36") bị **skip**, nhưng 37 TC khác vẫn được ghi `pass`. Nghĩa là **không có gì chứng minh 37 kết quả đó chạy trên build target 36** thay vì build cũ target 35 — mà toàn bộ ticket này chỉ có ý nghĩa khi chạy trên build mới. Đây là lỗi **thứ tự thực thi**: TC oracle bị bỏ qua, TC phụ thuộc vẫn kết luận. — **Fix**: thêm `TC-FUNC001-12` (§5) làm **gate bắt buộc chạy đầu tiên**; mọi TC còn lại chỉ hợp lệ sau khi gate pass.

- **[BLOCKER] GAP-2 · `RULE-08` / `ENV-003` — kết luận media từ staging**: task chạm **media** (T4: gửi/tải ảnh, video, audio, PDF) → `ENV-003` trigger **BẮT BUỘC** và **"không được đánh × với lý do staging đã pass"**. Toàn bộ 49 TC đã chạy đều ghi `env = staging`. Theo Catalog D, production dùng **server media riêng qua `p.lmes.jp` + sync B2**, còn dev/staging dùng chung server — nên lỗi path media / xóa file / cache ảnh **chỉ lộ ra trên production**. — **Fix** (điều chỉnh theo Leader 2026-08-21): **KHÔNG viết TC mới** — bộ TC media đã có sẵn trên test tool. Việc cần làm là **chạy lại `TC-MEDIA001-01..06` + `TC-FUNC001-02`, `-03` trên PRODUCTION** (build flavor prod trỏ backend production) và ghi `Môi trường test = PRODUCTION` vào kết quả. Bổ sung thêm `TC-ENV003-04` (§5) cho nhánh Abnormal — nhánh này **chưa có** trong 50 TC hiện tại.

- **[BLOCKER] GAP-6 · Impact `High` T3 (tablet / máy gập) — 0 bằng chứng**: `TC-UI002-02` và `TC-UI002-03` đều `blocked` vì không có thiết bị. Dev xếp T3 vào nhóm **"Trực tiếp, cần test kỹ"** và F3 (`property` giữ portrait trong manifest) là code **đã sửa**. Impact High + 0 evidence = đúng định nghĩa Blocker. — **Fix**: mượn/mua thiết bị, hoặc chạy trên **emulator tablet + foldable Android 16** (`TC-UI002-04` §5) và ghi rõ hạn chế của emulator vào Ghi chú.

- **[BLOCKER] GAP-7 · `RULE-09` / `COMPAT-LEGACY-001` — regression OS cũ bị skip**: Dev **yêu cầu nguyên văn** *"Cần regression thêm trên máy Android 13/14/15 để chắc không hồi quy"*. Thực tế: A15 pass, **A13 và A14 đều `skip`**. `COMPAT-LEGACY-001` là quan điểm **Cao**, và nâng targetSdk là đúng tình huống "cũ & mới song song" mà RULE-09 nhắm tới — hành vi OS khác nhau nhiều nhất chính ở **A13** (POST_NOTIFICATIONS) và **A14** (partial photo access, foreground service type). — **Fix**: chạy `TC-COMPATLEGACY001-02` và `-03`; bổ sung `-05` (§5). *(`-06` đã loại — xem §5.1)*

### 4.2 Major (nên fix)

- **[MAJOR] AP-6 · Mục 3 file 03 không phải danh sách caller**: mục 3 chứa log build + kết quả Dev tự test trên 1 máy, **không liệt kê function/file caller nào**. Đây là gốc của GAP-1. — **Fix**: yêu cầu Dev điền lại mục 3 đúng format bảng (file / function / thay đổi / lý do).

- **[MAJOR] AP-4 · Thiếu link Commit / Pull Request**: file 03 ghi `<chưa có>`, chỉ có `branch code: master_branch_release_store`. Không có PR → **không verify được** danh sách file Dev khai ở mục 4 có khớp diff thật không, và không kiểm được còn `WillPopScope` sót lại ở đâu. — **Fix**: yêu cầu Dev cung cấp link PR/diff.

- **[MAJOR] `RULE-01` — 6 quan điểm ưu tiên **Cao** thiếu loại case, không ghi lý do**: phân bố `Normal 44 / Abnormal 4 / Boundary 2`. Chi tiết: `FUNC-001` (11 TC, **0 Abnormal, 0 Boundary**) · `REG-SHARED-001` (12 TC, **0/0**) · `MEDIA-001` (6 TC, **0/0**) · `COMPAT-LEGACY-001` (4 TC, **0/0**) · `ENV-003` (2 TC, **0 Abnormal**) · `FUNC-DATE-001` (1 TC, **0 Normal, 0 Abnormal**). Không TC nào ghi lý do thiếu ở `Ghi chú`. — **Fix**: bổ sung theo §5, hoặc ghi lý do cụ thể vào `Ghi chú` từng quan điểm.

- **[MAJOR] GAP-8 · `DEPLOY-ASSET-001` — 0 TC về font/glyph/asset sau rebuild**: mục 2 đổi **toàn bộ build engine** (AGP + Gradle + Kotlin major version 1.9→2.1). `DEPLOY-ASSET-001` (**Cao**) trigger khi release sửa asset/font và yêu cầu kiểm *"font không fallback, glyph kanji/kana + dấu tiếng Việt đủ (không tofu ロ)"*. Không TC nào kiểm điều này. Rebuild toolchain là đúng lúc font/asset bundling dễ đổi nhất. — **Fix**: thêm `TC-DEPLOYASSET001-01` (§5).

- ~~**[MAJOR] GAP-9 · Nâng `crashlytics-gradle 2.8.0 → 3.0.2` không có TC nào**~~ — **ĐÃ LOẠI** theo quyết định Leader 2026-08-21 (xem §5.1).

- **[MAJOR] GAP-10 · Dev bỏ sót "edge-to-edge" khỏi mục 4 "Behavior changes"**: mục 4 chỉ liệt kê **predictive back**, nhưng mục 3 của chính Dev lại ghi đã test *"Edge-to-edge render đúng (status bar icon tối trên nền sáng, không đè content)"* — tức Dev biết đây là behavior change của target mới nhưng **không đưa vào danh sách impact**. Tester đã tự bù bằng `TC-UI001-01/-02` (điểm tốt), nhưng danh sách impact thiếu → các vùng edge-to-edge khác (bottom sheet, FAB, danh sách cuộn sát mép, bàn phím) có thể chưa được rà hết. — **Fix**: yêu cầu Dev bổ sung edge-to-edge vào mục 4 và xác nhận đã rà những màn nào.

- **[MAJOR] GAP-11 · `MEDIA-001` thiếu Abnormal/Boundary + thiếu partial photo access**: 8 TC media đều là happy path trên máy đã cấp full quyền. Thiếu: (a) **partial photo access** ("Chọn ảnh" thay vì "Cho phép tất cả") — hành vi Android 14+ mà target 36 siết chặt hơn; (b) file **sát giới hạn** theo Catalog E; (c) **MIME không chuẩn / PDF từ iOS** — đúng bug thật đã ghi trong `MEDIA-001` (*"PDF không hiện trong picker Android do MIME lạ"*). — **Fix**: thêm `TC-MEDIA001-07/08/09` (§5).

- **[MAJOR] GAP-12 · `SYNC-APP-001` bị dùng sai quan điểm**: 4 TC gắn mã `SYNC-APP-001` thực chất test **FCM push + cài đặt app**, không phải nội dung của quan điểm này. `SYNC-APP-001` yêu cầu *"đổi dữ liệu ở web → kiểm app (không restart, pull-to-refresh) và ngược lại"*. **Không TC nào test web ⇔ app**. — **Fix**: đổi mã quan điểm của 4 TC đó cho đúng, và thêm `TC-SYNCAPP001-05` (§5) test đồng bộ web↔app thật.

- **[MAJOR] GAP-13 · `FUNC-DATE-001` — 1 TC duy nhất, chưa chạy lần nào**: Dev **tự nhấn mạnh** calendar ca qua đêm là điểm nhạy cảm (T8). Chỉ có `TC-FUNCDATE001-01` (Boundary) và `last_exec = null`. `FUNC-DATE-001` là **Cao** → cần đủ 3 loại case. — **CẬP NHẬT 2026-08-21**: `#11342` đã được chạy và **pass** (§5.3) → T8 có bằng chứng đầu tiên, hạ từ GAP xuống RISK. — **Fix còn lại**: chạy `#11782` (Normal) + `#11783` (Abnormal) để đủ RULE-01.

- **[MAJOR] GAP-14 · F6 (iOS bump 397) — 0 TC**: Dev liệt kê `ios/Runner.xcodeproj/project.pbxproj` trong danh sách file thay đổi nhưng không TC nào chạm iOS. Nếu iOS **cũng phát hành từ branch này** thì đang release mù. — **Fix**: xác nhận với Dev phạm vi iOS; nếu có release → thêm `TC-FUNC001-14` (§5); nếu không → ghi rõ "iOS không phát hành ở ticket này" vào file 03.

- **[MAJOR] GAP-15 · TC `fail` chưa có kết luận**: `TC-REGSHARED001-11` ("Chuyển nhanh qua lại giữa app khác và L Message nhiều lần không crash") = `fail`, đã raise **#40059** — đúng quy trình, ghi nhận tốt. Nhưng TC này nằm đúng F5 (*"fix crash hidden state"*) — tức **fix của chính ticket này chưa đạt**. Không có TC re-test sau khi #40059 được fix. — **CẬP NHẬT 2026-08-21**: `#11322` đã được chạy lại và **pass** (§5.3) → issue gần như đóng. — **Fix còn lại**: xác nhận **#40059 đã Closed/Fix done** (RULE-11) và chạy `#11785` để re-test **toàn bộ nhóm** Lifecycle, không chỉ 1 TC (RULE-12).

- **[MAJOR] GAP-16 · `TC-SYNCAPP001-04` pass nhưng gắn ticket bug #40062**: TC ghi `pass` mà vẫn có `bug_tickets = [40062]` — mâu thuẫn trạng thái. — **Fix**: Leader xác minh #40062 là bug đã fix rồi mới pass, hay TC pass nhầm.

- **[MAJOR] `AP-3` — Happy-path-only regression**: 44/50 TC là `Normal` với precondition trạng thái sạch. Các vùng regression Dev nêu (booking T7, media T4, realtime T5) đều chỉ có TC happy path — không TC nào chạy regression ở **edge state cũ** (booking gần hết slot, chat có tin lỗi gửi dở, media đang upload dở khi back). — **Fix**: xem `TC-STATE001-01`, `TC-CONC001-01` (§5).

- **[MAJOR] Thiếu `Trạng thái đánh giá spec` ở 100% TC**: cột này null ở cả 50 TC. Với task này lý do có thật — **không có spec nào định nghĩa hành vi app mobile** (xem Input thiếu 1) — nhưng đúng quy trình phải ghi `Spec không ghi` + **nêu rõ đã hỏi ai**, thay vì để trống. Rủi ro: tester tự suy diễn hành vi mong đợi rồi cho `Đạt`. — **Fix**: điền `Spec không ghi` cho toàn bộ 50 TC + ghi tên người đã xác nhận hành vi mong đợi (PM hoặc Dev).

### 4.3 Minor (có thể fix sau)

- **[MINOR] Mã quan điểm `OBS-001` không tồn tại trong framework**: `TC-OBS001-01` dùng mã `OBS-001` — **không có** trong `framework/checklist-lme.md` lẫn `framework/catalog-lme.md`. `/review-tc` không map được coverage cho mã này. — **Fix**: đổi sang mã hợp lệ (đề xuất `ENV-003` hoặc `FUNC-001`), hoặc đề nghị Leader bổ sung nhóm `OBS-*` vào framework theo RULE-10.

- **[MINOR] `UI-003` có 4 TC nhưng 0 `Normal`**: cả 4 đều `Abnormal` (từ chối quyền / mất mạng). Thiếu case Normal (màn danh sách rỗng, loading bình thường). Không nghiêm trọng vì `UI-003` là Trung bình. — **Fix**: bổ sung 1 TC Normal nếu có thời gian.

- **[MINOR] `env_tag = local-only` nhưng ghi env chạy = `staging`**: `TC-FUNC001-08` và `-09` (build APK/AAB) gắn `env_tag = local-only` nhưng `last_exec.env = staging` — dữ liệu môi trường không nhất quán (dù trạng thái là `skip`). — **Fix**: sửa lại trên Studio khi chạy thật.

- **[MINOR] Studio không lưu model máy / phiên bản Android đã test**: cột `Môi trường test` chỉ ghi `staging` (backend), trong khi biến số của cả ticket là **OS/thiết bị**. — **Fix**: quy ước ghi model + OS vào `Ghi chú` hoặc `Evidence thực tế` của từng TC.

### 4.4 Nit (gợi ý)

- **[NIT] `TC-REGSHARED001-05`** ("Predictive back và image viewer vẫn hoạt động đúng sau khi nhận notification") verify 2 mục đích (back + notification) — có thể tách atomic hơn theo §B.2.

- **[NIT] Gộp nhóm `screen`**: "Media trên Android" (8 TC) có thể tách "gửi media" ⇄ "phát/xem media" để dễ phân công chạy song song.

- **[NIT] `PERF-LARGE-001`**: sau khi đổi engine build, cuộn danh sách chat/friend rất dài có thể đổi hiệu năng. Không bắt buộc (Dev không nêu), nhưng nếu có khách hàng dữ liệu lớn thì đáng thêm 1 TC smoke.

- **[NIT] RULE-11 / §4 checklist-lme**: các quan điểm chưa đủ bằng chứng (FORM-01, CHAT-01, ADM-01/03/04, TPL-01) **không** được dùng để flag trong report này — chỉ ghi nhận để Leader tham khảo.

---

## 5. TCs đề xuất bổ sung

> Member copy thẳng vào `04-tc-list.md` ở round tiếp theo — **16 cột canonical**, `TC No.` đã tránh trùng với 50 TC hiện có.
> ⚠️ File 04 hiện là bản **fetch read-only từ Studio**. TC bổ sung nên tạo trên **Studio** (`testcase_create`) rồi fetch lại, hoặc dùng `/sync-review-tc` để push vào sheet TC human.

| TC No. | Mã quan điểm liên kết | Loại case | Tiêu đề test case | Điều kiện tiền đề | Các bước thực hiện | Dữ liệu test/input | Kết quả mong đợi | Kết quả thực thi | Evidence thực tế | Môi trường test | Người thực hiện | Ngày thực hiện | Số ticket bug | Trạng thái đánh giá spec | Ghi chú |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TC-FUNC001-12 | FUNC-001 | Normal | GATE: xác nhận build QA đang test đúng là versionCode 397 / targetSdk 36 trước khi chạy regression | - Bản APK/AAB QA nhận từ Dev (branch `master_branch_release_store`)<br>- Máy thật Android 16 (SDK 36)<br>- Có `aapt2` hoặc app "App Info" đọc được targetSdk | 1. Chạy `aapt2 dump badging <file.apk>` trên chính file QA sắp cài.<br>2. Ghi lại `targetSdkVersion`, `compileSdkVersion`, `versionCode`.<br>3. Cài file đó lên máy test.<br>4. Vào Cài đặt > Ứng dụng > L Message > chi tiết, đối chiếu version hiển thị.<br>5. Chỉ khi khớp mới được bắt đầu chạy các TC còn lại. | File APK/AAB QA thực nhận | `targetSdkVersion='36'`, `compileSdkVersion='36'`, `versionCode=397`; version hiển thị trên máy khớp đúng file vừa cài. Nếu lệch → **DỪNG toàn bộ đợt test**. | Chưa test | | STAGING | | | | Spec không ghi | **Lấp GAP-5 (BLOCKER)**. TC gate — bắt buộc chạy ĐẦU TIÊN; mọi kết quả pass khác chỉ hợp lệ sau khi TC này pass. Evidence bắt buộc: output `aapt2 dump badging` dạng text + screenshot màn App Info. |
| TC-REGSHARED001-13 | REG-SHARED-001 | Normal | Rà TẤT CẢ màn chặn back theo danh sách Dev: back hệ thống vẫn kích hoạt đúng handler sau khi nâng target 36 | - **Danh sách file/màn còn dùng `WillPopScope`/`onWillPop`/`PopScope` do Dev cung cấp** (grep trên branch `master_branch_release_store`)<br>- Máy thật Android 16, app versionCode 397<br>- Tài khoản có đủ quyền vào mọi màn trong danh sách | 1. Yêu cầu Dev chạy `grep -rn "WillPopScope\|onWillPop\|PopScope" lib/` và gửi danh sách đầy đủ.<br>2. Với TỪNG màn trong danh sách: mở màn, đưa về đúng trạng thái mà handler back được kỳ vọng chạy (đang nhập dở / đang tải / có thay đổi chưa lưu).<br>3. Bấm nút Back hệ thống.<br>4. Ghi kết quả từng màn vào bảng đối chiếu (màn / handler kỳ vọng / thực tế). | Danh sách màn Dev cung cấp (kỳ vọng có màn **ngoài** `image_gallery.dart`) | Mọi màn trong danh sách kích hoạt **đúng handler chặn back như trước khi nâng target** (hiện dialog xác nhận / chặn thoát / pop 1 cấp). KHÔNG màn nào bị thoát thẳng app hoặc mất dữ liệu do `onBackPressed` không còn được gọi. | Chưa test | | STAGING | | | | Spec không ghi | **Lấp GAP-1 (BLOCKER)** — `REG-SHARED-001` bắt buộc có danh sách nơi ảnh hưởng do DEV cung cấp. Cover F4 + T1. Evidence bắt buộc: danh sách file Dev gửi + video back trên TỪNG màn. `regression` |
| TC-REGSHARED001-14 | REG-SHARED-001 | Abnormal | Màn có dialog xác nhận rời trang: vuốt predictive back phải hiện dialog, không thoát thẳng | - Màn có thay đổi chưa lưu và có dialog "Bạn có chắc muốn rời?" (lấy từ danh sách Dev ở TC-REGSHARED001-13)<br>- Máy thật Android 16 | 1. Mở màn có dialog xác nhận rời trang.<br>2. Sửa 1 field bất kỳ để tạo trạng thái "chưa lưu".<br>3. Vuốt predictive back từ cạnh trái tới khi thả tay.<br>4. Quan sát có hiện dialog xác nhận không.<br>5. Chọn "Hủy" → kiểm tra còn ở màn cũ và dữ liệu chưa lưu còn nguyên. | 1 field đã sửa, chưa bấm Lưu | Dialog xác nhận **hiện đúng** khi vuốt predictive back (không chỉ khi bấm nút Back). Chọn "Hủy" → ở lại màn, dữ liệu đã nhập còn nguyên. Không thoát thẳng, không mất dữ liệu. | Chưa test | | STAGING | | | | Spec không ghi | **Lấp GAP-1 + RULE-01 (Abnormal cho `REG-SHARED-001`)**. Đây là kịch bản hỏng kinh điển khi `WillPopScope` không được thay bằng `PopScope`. Evidence: video vuốt back + dialog. |
| TC-REGSHARED001-15 | REG-SHARED-001 | Boundary | Hủy cử chỉ predictive back giữa chừng (vuốt ~90% rồi thả về) không được pop màn | - Máy thật Android 16, app versionCode 397<br>- Đang ở màn con đã push từ màn danh sách | 1. Mở màn con bất kỳ (VD chi tiết friend).<br>2. Vuốt predictive back từ cạnh trái tới khoảng 90% chiều ngang màn hình, GIỮ không thả.<br>3. Kéo ngược trở lại cạnh trái rồi thả tay (hủy cử chỉ).<br>4. Lặp lại 5 lần liên tiếp.<br>5. Kiểm tra màn hiện tại và trạng thái dữ liệu. | 5 lần vuốt-hủy liên tiếp | Sau mỗi lần hủy cử chỉ, app **giữ nguyên màn con**, không pop, không nháy màn, không crash. Trạng thái cuộn/dữ liệu của màn không bị reset. | Chưa test | | STAGING | | | | Spec không ghi | **Lấp RULE-01 (Boundary cho `REG-SHARED-001`)**. Biên của cử chỉ predictive back — hành vi mới hoàn toàn ở target 36. Evidence: video quay chậm. |
| TC-ENV003-04 | ENV-003 | Abnormal | Media có path bất thường (thừa `//`, file không phần mở rộng) vẫn mở được trên production Android 16 | - Build flavor prod trỏ production<br>- Có sẵn bản ghi media path chứa `//` hoặc file không có extension (nhờ Dev seed hoặc lấy từ dữ liệu cũ) | 1. Mở hội thoại/màn có media path bất thường.<br>2. Thử hiển thị ảnh trong app.<br>3. Thử tải file đó về máy.<br>4. Mở file vừa tải bằng app mặc định của máy. | Path chứa `//`; file không có phần mở rộng | App hiển thị/tải được media; nếu không hỗ trợ thì **báo lỗi rõ ràng**, không trắng màn, không crash, không tải về file 0 byte. | Chưa test | | **PRODUCTION** | | | | Spec không ghi | **Lấp GAP-2 + RULE-01 (Abnormal cho `ENV-003`)**. Catalog D nêu rõ: dev/staging vẫn nhận diện type, production qua B2 tính là file → chỉ lộ trên production. |
| TC-UI002-04 | UI-002 | Normal | Khóa portrait và layout đúng trên emulator tablet + foldable Android 16 (phương án thay thế khi thiếu máy thật) | - Android Studio có emulator **Pixel Tablet API 36** và **Pixel Fold API 36**<br>- App versionCode 397 cài được trên emulator | 1. Cài app lên emulator Pixel Tablet API 36.<br>2. Mở các màn chính (danh sách chat, chi tiết chat, booking, calendar).<br>3. Xoay emulator sang landscape → kiểm tra app có giữ portrait không.<br>4. Lặp lại toàn bộ trên emulator Pixel Fold API 36, kèm thao tác gập/mở (đổi cấu hình màn hình).<br>5. Ghi rõ vào Ghi chú đây là kết quả emulator, không phải máy thật. | Pixel Tablet API 36; Pixel Fold API 36 | App **giữ portrait** đúng như khai báo `property` trong manifest trên cả tablet và foldable; không vỡ layout, không crash khi đổi cấu hình gập/mở. | Chưa test | | STAGING | | | | Spec không ghi | **Lấp GAP-6 (BLOCKER)** cho impact T3 đang `blocked` vì thiếu thiết bị. Cover F3. ⚠️ Emulator **không thay thế hoàn toàn** máy thật — vẫn phải ghi rủi ro còn lại vào report. Evidence: screenshot cả 2 emulator. |
| TC-COMPATLEGACY001-05 | COMPAT-LEGACY-001 | Abnormal | Nâng cấp app (KHÔNG gỡ) từ bản target 35 lên 397 trên Android 13 — giữ đăng nhập và dữ liệu local | - Máy thật/emulator **Android 13**<br>- Đã cài sẵn bản app cũ (target 35) và **đăng nhập, có dữ liệu chat + cài đặt** | 1. Trên bản cũ: đăng nhập, mở vài hội thoại, đổi 1 cài đặt bất kỳ để sinh dữ liệu local.<br>2. Cài đè bản versionCode 397 (KHÔNG gỡ app).<br>3. Mở app.<br>4. Kiểm tra: còn đăng nhập không, lịch sử chat còn không, cài đặt vừa đổi còn không.<br>5. Gửi 1 tin nhắn để xác nhận hoạt động bình thường. | Bản cũ target 35 → bản mới 397, Android 13 | App **giữ nguyên phiên đăng nhập**, lịch sử chat và cài đặt local (sqflite + SharedPreferences) **không mất**, gửi tin bình thường. Không bắt đăng nhập lại, không mất dữ liệu. | Chưa test | | STAGING | | | | Spec không ghi | **Lấp GAP-7 (BLOCKER) + GAP-16**. RULE-09 cũ&mới song song. Kiểm chứng khẳng định của Dev *"không đụng sqflite/SharedPreferences"* sau khi đổi Kotlin 1.9→2.1. `regression` |
| TC-DEPLOYASSET001-01 | DEPLOY-ASSET-001 | Normal | Font và glyph tiếng Nhật + tiếng Việt hiển thị đủ sau khi đổi toàn bộ toolchain build | - App versionCode 397 trên máy thật Android 16<br>- Dữ liệu test có sẵn text JP (kanji + kana) và VN có dấu<br>- 1 máy Android 13 để đối chiếu | 1. Mở màn chat, hiển thị tin nhắn chứa kanji (漢字), kana (ひらがな/カタカナ), tiếng Việt có dấu (ữ, ọ, ế), emoji.<br>2. Mở màn danh sách friend có tên JP và tên VN.<br>3. Mở màn booking/calendar có nhãn ngày giờ JP.<br>4. Soi từng màn tìm ký tự hiển thị thành ô vuông (tofu ロ) hoặc sai font.<br>5. Đối chiếu cùng nội dung trên Android 13. | Text: `漢字テスト` · `ひらがなカタカナ` · `Tiếng Việt có dấu đầy đủ` · emoji | **Không có ký tự tofu (ロ)**, không glyph nào bị thiếu, font không fallback sang font hệ thống khác. Hiển thị giống hệt giữa Android 16 và Android 13. | Chưa test | | STAGING | | | | Spec không ghi | **Lấp GAP-8 (MAJOR) — `DEPLOY-ASSET-001`**. Đổi AGP/Gradle/Kotlin major là lúc asset & font bundling dễ đổi nhất. Cover F2. Evidence: screenshot từng màn có JP + VN. |
| TC-STATE001-01 | STATE-001 | Abnormal | Predictive back giữa luồng đặt lịch nhiều bước không làm mất dữ liệu đã nhập và không tạo booking trùng | - App versionCode 397, Android 16<br>- Tài khoản có quyền đặt lịch Salon<br>- Salon còn slot trống | 1. Vào luồng đặt lịch Salon, đi tới bước cuối (đã chọn dịch vụ + ngày giờ), CHƯA bấm xác nhận.<br>2. Vuốt predictive back 1 cấp.<br>3. Kiểm tra: quay về bước trước hay thoát cả luồng? Dữ liệu đã chọn còn không?<br>4. Đi lại tới bước cuối và bấm xác nhận.<br>5. Mở danh sách booking, đếm số booking vừa tạo. | 1 booking Salon, back giữa chừng 1 lần | Predictive back quay về **đúng 1 bước trước**, dữ liệu đã chọn **còn nguyên** (không reset về đầu luồng). Sau khi xác nhận, danh sách có **đúng 1 booking**, không trùng, không booking rác ở trạng thái dở. | Chưa test | | STAGING | | | | Spec không ghi | **Lấp GAP-7/AP-3 (MAJOR)** — `STATE-001` (Cao): quy trình nhiều bước bị gián đoạn. Predictive back chính là cơ chế gián đoạn mới của target 36. Cover T1 + T7. |
| TC-CONC001-01 | CONC-001 | Abnormal | Bấm Back liên tiếp nhanh trong lúc animation predictive back đang chạy chỉ pop đúng 1 cấp | - App versionCode 397, Android 16<br>- Đang ở màn con cách màn gốc ≥ 3 cấp (danh sách → chi tiết → ảnh) | 1. Điều hướng: danh sách chat → chi tiết chat → mở ảnh (3 cấp).<br>2. Bấm nút Back **2 lần thật nhanh** (double-tap) ngay khi animation bắt đầu.<br>3. Ghi lại app đang ở màn nào.<br>4. Lặp lại 5 lần, mỗi lần dựng lại 3 cấp.<br>5. Lặp thêm 5 lần bằng vuốt predictive back nhanh liên tiếp. | Double-tap Back × 5 lần; vuốt nhanh liên tiếp × 5 lần | Mỗi thao tác back chỉ pop **đúng 1 cấp** — không nhảy 2 cấp, không thoát thẳng app, không crash, không để lại màn trắng. Kết quả **nhất quán** qua cả 10 lần. | Chưa test | | STAGING | | | | Spec không ghi | **Lấp AP-3 (MAJOR)** — `CONC-001` kịch bản (1) double-click hành động. Liên quan trực tiếp TC-REGSHARED001-11 đang FAIL (#40059). Evidence: video quay chậm + logcat. |
| TC-MEDIA001-07 | MEDIA-001 | Abnormal | Quyền ảnh dạng "chỉ chọn một số ảnh" (partial access) vẫn gửi được ảnh đã chọn trên Android 16 | - Máy thật Android 16, app versionCode 397<br>- App **chưa** được cấp quyền ảnh (hoặc đã reset quyền trong Cài đặt) | 1. Vào chat, bấm gửi ảnh → hệ thống hỏi quyền.<br>2. Chọn **"Chọn ảnh"** (partial access), chỉ chọn 2 ảnh cho phép.<br>3. Kiểm tra picker của app hiển thị được 2 ảnh đó.<br>4. Gửi 1 trong 2 ảnh vào chat.<br>5. Quay lại gửi ảnh lần nữa → chọn "Chọn thêm ảnh", thêm 1 ảnh mới và gửi. | Cấp quyền partial: 2 ảnh, sau đó thêm 1 ảnh | App **hoạt động bình thường với quyền partial**: hiển thị đúng các ảnh đã cho phép, gửi thành công, không crash, không hiện thư viện trắng, không bắt buộc phải cấp full quyền mới dùng được. | Chưa test | | STAGING | | | | Spec không ghi | **Lấp GAP-11 (MAJOR)**. Partial photo access là hành vi Android 14+ mà target 36 siết chặt — thuộc đúng vùng F1. Cover T4. Evidence: screenshot dialog quyền + kết quả gửi. |
| TC-MEDIA001-08 | MEDIA-001 | Boundary | Gửi file sát giới hạn dung lượng theo Catalog E trên Android 16 | - Máy thật Android 16, app versionCode 397<br>- Bộ file test dựng sẵn đúng giới hạn nơi sử dụng (tra `framework/catalog-lme.md` Catalog E — chat 1:1 khác friend info) | 1. Tra Catalog E lấy giới hạn đúng cho chat 1:1.<br>2. Chuẩn bị 3 file: đúng biên, biên−1, biên+1.<br>3. Gửi lần lượt từng file trong chat.<br>4. Ghi lại hành vi từng trường hợp.<br>5. Với file gửi thành công: tải lại về và mở kiểm tra không hỏng. | File đúng biên / biên−1 / biên+1 (theo Catalog E) | File **đúng biên và biên−1** gửi thành công, tải về mở được, không hỏng. File **biên+1** bị chặn với **thông báo lỗi rõ ràng** (nêu giới hạn cụ thể), không treo, không gửi nửa vời. | Chưa test | | STAGING | | | | Spec không ghi | **Lấp GAP-11 + RULE-01 (Boundary cho `MEDIA-001`)**. Bắt buộc tra Catalog E theo **nơi sử dụng**, không dùng giới hạn chung. Cover T4. |
| TC-MEDIA001-09 | MEDIA-001 | Abnormal | File MIME không chuẩn và PDF tạo từ iOS vẫn được picker Android 16 nhận diện | - Máy thật Android 16, app versionCode 397<br>- Bộ file đa nguồn: PDF tạo từ iOS, ảnh từ máy scan, file MIME không chuẩn (đổi đuôi), ảnh từ Google Drive | 1. Copy bộ file đa nguồn vào bộ nhớ máy test.<br>2. Vào chat, mở picker chọn file.<br>3. Kiểm tra từng file có **hiện trong picker** không.<br>4. Gửi từng file gửi được.<br>5. Mở lại file vừa gửi từ phía nhận để xác nhận không hỏng. | PDF từ iOS · ảnh máy scan · file MIME lạ · ảnh Google Drive | Tất cả file hợp lệ **hiện trong picker** và gửi được; file MIME lạ thì hoặc gửi được hoặc **báo lỗi rõ ràng** — không được im lặng biến mất khỏi picker. Bên nhận mở được đúng nội dung. | Chưa test | | STAGING | | | | Spec không ghi | **Lấp GAP-11 (MAJOR)**. Bám đúng bug thật ghi trong `MEDIA-001`: *"PDF không hiện trong picker Android do MIME lạ"*. Cover T4 + F2. |
| TC-SYNCAPP001-05 | SYNC-APP-001 | Normal | Đổi dữ liệu trên web admin phản ánh đúng sang app Android 16 và ngược lại (không restart app) | - App versionCode 397 trên Android 16, đã đăng nhập<br>- Web admin đăng nhập **cùng tài khoản/bot**<br>- 1 friend test có thể sửa thông tin | 1. Trên web admin: đổi tên hiển thị/tag của friend test.<br>2. Trên app (KHÔNG restart): vào màn friend đó, pull-to-refresh.<br>3. Kiểm tra thay đổi đã phản ánh chưa.<br>4. Trên app: đổi 1 trường khác của cùng friend.<br>5. Trên web admin: F5 và kiểm tra thay đổi từ app đã phản ánh chưa. | 1 friend test, đổi tên + tag ở cả 2 phía | Thay đổi từ web hiện đúng trên app sau pull-to-refresh (**không cần restart app**); thay đổi từ app hiện đúng trên web sau F5. Hai bên **không ghi đè lẫn nhau**, không mất dữ liệu. | Chưa test | | STAGING | | | | Spec không ghi | **Lấp GAP-12 (MAJOR)** — 4 TC đang gắn `SYNC-APP-001` thực chất test FCM, không test web⇔app. Đây mới đúng nội dung quan điểm. |
| TC-FUNCDATE001-02 | FUNC-DATE-001 | Normal | Calendar hiển thị đúng ca làm việc trong ngày thường trên Android 16 | - App versionCode 397, Android 16<br>- Tài khoản có shift calendar với ca trong ngày (VD 09:00–18:00)<br>- Timezone máy = JST | 1. Mở màn shift calendar.<br>2. Chọn ngày có ca 09:00–18:00.<br>3. Đối chiếu giờ bắt đầu/kết thúc hiển thị với dữ liệu trên web admin.<br>4. Chuyển sang tuần/tháng khác rồi quay lại.<br>5. Kiểm tra ca vẫn hiển thị đúng. | Ca 09:00–18:00, timezone JST | Ca hiển thị **đúng 09:00–18:00** trên app, khớp 100% với web admin; chuyển tuần/tháng qua lại không làm lệch giờ hay mất ca. | Chưa test | | STAGING | | | | Spec không ghi | **Lấp GAP-13 + RULE-01 (Normal cho `FUNC-DATE-001`)**. Hiện chỉ có 1 TC Boundary (ca qua đêm) và chưa chạy lần nào. Cover T8. |
| TC-FUNCDATE001-03 | FUNC-DATE-001 | Abnormal | Calendar không lệch ca khi đổi timezone máy hoặc bật định dạng 24h trên Android 16 | - App versionCode 397, Android 16<br>- Tài khoản có ca qua đêm (VD 22:00–06:00) và ca trong ngày<br>- Quyền đổi cài đặt ngày giờ của máy | 1. Với timezone JST: ghi lại giờ hiển thị của ca qua đêm và ca trong ngày.<br>2. Đổi timezone máy sang GMT+7, KHÔNG restart app, quay lại calendar.<br>3. Ghi lại giờ hiển thị.<br>4. Bật/tắt định dạng 24h của hệ thống, quay lại calendar.<br>5. Đối chiếu toàn bộ với web admin. | Ca 22:00–06:00 và 09:00–18:00; timezone JST → GMT+7; 24h on/off | Giờ ca hiển thị **theo đúng quy ước spec** (JST cố định hoặc theo máy — phải nhất quán và khớp web admin). **Ca qua đêm không bị tách/mất ngày**, không nhảy sai ngày khi đổi timezone; đổi 24h chỉ đổi cách hiển thị, không đổi giá trị giờ. | Chưa test | | STAGING | | | | Spec không ghi | **Lấp GAP-13 + RULE-01 (Abnormal cho `FUNC-DATE-001`)**. `FUNC-DATE-001` yêu cầu test timezone + 0:00 vs 24:00. ⚠️ Spec chưa định nghĩa quy ước timezone → **bắt buộc hỏi PM/Dev trước khi chấm Đạt**. Cover T8. |
| TC-FUNC001-14 | FUNC-001 | Normal | Smoke iOS build 397 sau khi bump version (chỉ chạy nếu iOS cũng phát hành từ branch này) | - Xác nhận với Dev iOS **có** phát hành từ `master_branch_release_store`<br>- Build iOS version 397 cài được trên máy iPhone thật<br>- Tài khoản test | 1. Xác nhận phạm vi iOS với Dev trước khi chạy.<br>2. Cài build iOS 397 lên iPhone thật.<br>3. Chạy luồng smoke: khởi động → đăng nhập → mở chat → gửi 1 ảnh → nhận push notification → đặt 1 lịch.<br>4. Kiểm tra version hiển thị trong app đúng 397.<br>5. Kiểm tra không có crash trong quá trình. | Build iOS version 397 | Toàn bộ luồng smoke chạy hết, version hiển thị đúng 397, không crash. Nếu Dev xác nhận iOS **không** phát hành → đánh × và ghi lý do vào Ghi chú thay vì bỏ trống. | Chưa test | | STAGING | | | | Spec không ghi | **Lấp GAP-14 (MAJOR)** — F6 hiện 0 TC. TC có điều kiện: chỉ chạy sau khi Dev xác nhận phạm vi iOS. Evidence: screenshot màn About/version + luồng smoke. |
| TC-REGSHARED001-16 | REG-SHARED-001 | Normal | Re-test toàn nhóm Lifecycle sau khi #40059 được fix | - #40059 đã ở trạng thái Fix done/Closed<br>- Build mới đã bao gồm fix của #40059<br>- Máy thật Android 16 | 1. Xác nhận #40059 đã fix và build QA đã bao gồm fix (chạy lại TC-FUNC001-12 gate).<br>2. Chạy lại `TC-REGSHARED001-11` (chuyển nhanh qua lại giữa app khác và L Message nhiều lần).<br>3. Chạy lại toàn bộ nhóm Lifecycle: `TC-REGSHARED001-09`, `-10`, `TC-UI003-01`.<br>4. Chạy thêm `TC-CONC001-01`.<br>5. Ghi kết quả từng TC. | ≥ 20 lần chuyển app qua lại liên tiếp | Toàn bộ nhóm Lifecycle **Đạt**, đặc biệt `TC-REGSHARED001-11` không còn crash. Không phát sinh crash mới ở các TC lifecycle từng pass. | Chưa test | | STAGING | | | | Spec không ghi | **Lấp GAP-15 (MAJOR)** — **RULE-12**: phạm vi regression bắt buộc gồm *"mọi case đã từng Không đạt và được fix"*. Cover F5 + T9. `regression` |

---

### 5.1 — TC đề xuất đã LOẠI theo quyết định Leader (2026-08-21)

> Ghi lại để giữ vết: 4 TC dưới đây có trong draft review vòng 1 nhưng đã được Leader loại. **Không đưa vào file 04.**

| TC No. (đã loại) | Nội dung đề xuất | Lý do loại | Rủi ro còn lại |
|---|---|---|---|
| `TC-FUNC001-13` | Crashlytics 3.0.2 vẫn gửi báo cáo crash kèm đúng versionCode 397 | **Leader: không cần** | Nếu Crashlytics ngừng gửi sau khi nâng `crashlytics-gradle 2.8.0 → 3.0.2` thì mất khả năng phát hiện crash production — **chấp nhận rủi ro**, theo dõi qua số lượng crash report thực tế sau release thay vì bằng TC. |
| `TC-FUNCDRAFT001-01` | Nội dung tin nhắn soạn dở không mất khi predictive back rồi quay lại | **Leader: app không hỗ trợ giữ draft** → không có hành vi để verify | Không còn. `FUNC-DRAFT-001` chuyển sang **×** ở bảng F.1 với lý do hợp lệ (RULE-03). |
| `TC-ENV003-03` | Gửi/tải media trong chat trên PRODUCTION | **Leader: test tool đã có sẵn TC media** — chỉ cần chạy chúng trên production | Không còn — nhưng **GAP-2 vẫn là BLOCKER**: bắt buộc chạy lại `TC-MEDIA001-01..06` + `TC-FUNC001-02`, `-03` với `Môi trường test = PRODUCTION`, không được kết luận từ staging (RULE-08). |
| `TC-COMPATLEGACY001-06` | Nâng cấp từ bản app cũ nhất còn hỗ trợ lên 397 trên Android 14 | **Trùng với TC đã có** — `TC-COMPATLEGACY001-01` (Studio #11307) đã cover đường nâng cấp đè không gỡ app, giữ session + dữ liệu local | Thấp. Delta duy nhất là **độ lớn bước nhảy version**; vì Dev khẳng định *không có migration local*, nâng cấp từ bản cũ nhất và từ bản liền trước là **cùng một thao tác** → giá trị biên không đáng kể. |

> **Ghi chú về `TC-COMPATLEGACY001-05`** (vẫn giữ trong §5): TC này **không** trùng `#11307`. Khác biệt thật: `#11307` chạy nâng cấp trên **Android 16**, còn `TC-COMPATLEGACY001-02/-03` (A13/A14) là **cài mới**, không phải nâng cấp đè. Tổ hợp *"nâng cấp đè × OS cũ"* hiện **chưa có TC nào** — quan trọng ở **Android 13** vì đó là mốc ra đời quyền `POST_NOTIFICATIONS` (app nâng cấp đã có quyền ≠ app cài mới phải xin quyền).
>
> 👉 Nếu Leader muốn gọn hơn: thay vì thêm TC mới, có thể **sửa precondition của `TC-COMPATLEGACY001-02` (A13) và `-03` (A14) trên Studio** từ "cài versionCode 397" thành "**cài đè** lên bản cũ target 35 đã đăng nhập" — vừa lấp gap vừa không tăng số TC.

### 5.2 — 18 TC đã được TẠO trên Studio (2026-08-21)

> Toàn bộ 18 TC ở §5 đã được push lên **Studio task #172** bằng `testcase_create`. Trạng thái: `draft`, `Kết quả thực thi = Chưa test`, `spec_status = Spec không ghi`.
> `client_ref` dùng tiền tố **`T172-RV-*`** (RV = review) để phân biệt với 50 TC gốc (`T172-0xx`) — cũng là khóa **idempotent**, chạy lại `testcase_create` sẽ không tạo trùng.

| TC No. (repo) | client_ref | Studio ID | Quan điểm | Loại case | Lấp GAP |
|---|---|---|---|---|---|
| TC-FUNC001-12 | `T172-RV-01` | **#11764** | FUNC-001 | Normal | GAP-5 (BLOCKER) — TC **GATE** |
| TC-REGSHARED001-13 | `T172-RV-02` | **#11765** | REG-SHARED-001 | Normal | GAP-1 (BLOCKER) |
| TC-REGSHARED001-14 | `T172-RV-03` | **#11766** | REG-SHARED-001 | Abnormal | GAP-1 + RULE-01 |
| TC-REGSHARED001-15 | `T172-RV-04` | **#11767** | REG-SHARED-001 | Boundary | RULE-01 |
| TC-ENV003-04 | `T172-RV-05` | **#11768** | ENV-003 | Abnormal | GAP-2 (BLOCKER) — `env_scope = prd` |
| TC-UI002-04 | `T172-RV-06` | **#11769** | UI-002 | Normal | GAP-6 (BLOCKER) |
| TC-COMPATLEGACY001-05 | `T172-RV-07` | **#11774** | COMPAT-LEGACY-001 | Abnormal | GAP-7 (BLOCKER) |
| TC-DEPLOYASSET001-01 | `T172-RV-08` | **#11775** | DEPLOY-ASSET-001 | Normal | GAP-8 |
| TC-STATE001-01 | `T172-RV-09` | **#11776** | STATE-001 | Abnormal | GAP-7 / AP-3 |
| TC-CONC001-01 | `T172-RV-10` | **#11777** | CONC-001 | Abnormal | AP-3 |
| TC-MEDIA001-07 | `T172-RV-11` | **#11778** | MEDIA-001 | Abnormal | GAP-11 |
| TC-MEDIA001-08 | `T172-RV-12` | **#11779** | MEDIA-001 | Boundary | GAP-11 + RULE-01 |
| TC-MEDIA001-09 | `T172-RV-13` | **#11780** | MEDIA-001 | Abnormal | GAP-11 |
| TC-SYNCAPP001-05 | `T172-RV-14` | **#11781** | SYNC-APP-001 | Normal | GAP-12 |
| TC-FUNCDATE001-02 | `T172-RV-15` | **#11782** | FUNC-DATE-001 | Normal | GAP-13 + RULE-01 |
| TC-FUNCDATE001-03 | `T172-RV-16` | **#11783** | FUNC-DATE-001 | Abnormal | GAP-13 + RULE-01 |
| TC-FUNC001-14 | `T172-RV-17` | **#11784** | FUNC-001 | Normal | GAP-14 (có điều kiện) |
| TC-REGSHARED001-16 | `T172-RV-18` | **#11785** | REG-SHARED-001 | Normal | GAP-15 / RULE-12 |

**Tác dụng lên phân bố loại case** — đây là điểm sửa lớn nhất:

| | Normal | Abnormal | Boundary | Tổng |
|---|---|---|---|---|
| 50 TC gốc | 44 (88%) | 4 (8%) | 2 (4%) | 50 |
| 18 TC review thêm | 8 | 8 | 2 | 18 |
| **Sau khi thêm** | **52 (76%)** | **12 (18%)** | **4 (6%)** | **68** |

> Vẫn lệch so với gợi ý 40/35/25 của §C, nhưng đã cải thiện đáng kể. Phần lệch còn lại nằm ở `FUNC-001` (11 TC gốc đều Normal) — chấp nhận được vì đây là quan điểm "luồng chính hoàn tất đúng đặc tả".

### 5.3 — ⚠️ Thay đổi TRÊN STUDIO trong lúc review (không do reviewer)

> Phát hiện khi đối chiếu Studio trước/sau: `haodtb` đã thao tác song song sáng **2026-08-21**. Ghi lại để Leader nắm, vì có mục làm **thay đổi kết luận của report này**.

**A. 2 TC được chạy lại → đổi kết quả (ảnh hưởng issue đã nêu):**

| Studio ID | TC | Trước | Sau | Ảnh hưởng |
|---|---|---|---|---|
| **#11322** | Chuyển nhanh qua lại giữa app khác và L Message nhiều lần không crash | `fail` (#40059) | **`pass`** (03:17) | **GAP-15 gần như đã đóng** — TC từng Không đạt nay Đạt. Vẫn cần chạy `#11785` để re-test **cả nhóm** Lifecycle (RULE-12), và xác nhận #40059 đã Closed. |
| **#11342** | Calendar hiển thị đúng ca làm việc qua đêm trên Android 16 | `null` (chưa chạy) | **`pass`** (03:16) | **T8 đã có bằng chứng đầu tiên** — coverage matrix mục T8 chuyển từ `GAP` (chưa chạy) sang `RISK` (1 TC Boundary pass, vẫn thiếu Normal + Abnormal → `#11782`, `#11783`). |

**B. 2 TC mới do `haodtb` thêm (ngoài 18 TC của review):**

| Studio ID | TC | Vấn đề |
|---|---|---|
| **#11741** | "Regression app: login, logout, đặt lịch booking, nhận notify, chat 1:1,..." — đã `pass` | 🔴 **`viewpoint = null`, `client_ref = null`** — thiếu `Mã quan điểm liên kết` (cột **BẮT BUỘC** để map coverage). Ngoài ra tiêu đề gộp ≥ 5 mục đích → vi phạm §B.2 *atomic*. `provenance.source = human` ghi thẳng qua web UI, không qua MCP. — **`[MAJOR]` Fix**: gán mã quan điểm (đề xuất `REG-SHARED-001`) và tách thành các TC atomic, hoặc ghi rõ đây là "bộ smoke cố định" theo **RULE-12** phần (1). |
| **#11758** | "Nhận và mở push khi đang mở app ở màn Notify" — `SYNC-APP-001`, chưa chạy | Hợp lệ, bổ sung tốt cho T6. Lưu ý cùng vấn đề mã quan điểm với 4 TC `SYNC-APP-001` cũ (GAP-12): TC này test **push notification**, không phải đồng bộ web⇔app. |

**Tổng trạng thái Studio task #172 sau tất cả thay đổi:**

| Chỉ số | Trước review | Sau review |
|---|---|---|
| Tổng TC | 50 | **70** (50 gốc + 18 review + 2 của `haodtb`) |
| `pass` | 37 | **40** |
| `fail` | 1 | **0** |
| `blocked` + `skip` | 11 | **11** *(không đổi — 7 BLOCKER vẫn nguyên)* |
| Chưa chạy | 1 | **19** (18 TC review + #11758) |

> 🔴 **Lưu ý quan trọng cho Leader**: `fail = 0` **không có nghĩa là đã an toàn**. **11 TC `blocked`/`skip` vẫn y nguyên** — bao gồm toàn bộ 6 TC Build & Compliance (mục tiêu ticket) và 2 TC regression Android 13/14. **7 BLOCKER của report này chưa có cái nào được đóng.**

### 5.4 — Vòng sửa theo làm rõ của Dev về "nút Back" (2026-08-21)

> **Làm rõ**: "nút Back" trong mục 4 = **nút Back của hệ thống Android trên navigation bar** (chế độ **3 nút**), không phải nút back trong giao diện app. Chi tiết + hệ quả: [03-dev-impact.md §4.4](03-dev-impact.md).
>
> ⚠️ **Redmine không đổi text** (`updated_on` vẫn `2026-08-21T00:09:17Z`) — đây là làm rõ ngữ nghĩa do Leader chuyển lại, đã ghi vết ở file 03.

**Vấn đề phát hiện**: Android có 2 chế độ điều hướng **loại trừ nhau** — chế độ cử chỉ **không có nút Back để bấm**, chế độ 3 nút **không có cử chỉ vuốt**. Rà lại 73 TC:

| Nhóm | Tình trạng trước khi sửa |
|---|---|
| TC "vuốt / predictive back" (#11315, #11318, #11346) | ✅ **Có** ghi `gesture navigation` trong precondition |
| TC "bấm nút Back" (#11314, #11317) | 🔴 **KHÔNG** ghi chế độ nào → nếu máy để chế độ cử chỉ thì **không có nút Back nào để bấm**, nhưng TC vẫn ghi `pass` |
| TC dùng chữ "**hoặc**" (#11316 *"Bấm HOẶC vuốt"*, #11319 *"Back hệ thống HOẶC predictive back"*) | 🔴 Tester chỉ chạy **1 nhánh**, nhánh còn lại bỏ trống mà vẫn tính `pass` |

**A. Đã UPDATE 4 TC gốc** (`testcase_update` — chốt rõ chế độ, bỏ chữ "hoặc"):

| Studio ID | TC | Sửa gì | Ảnh hưởng kết quả cũ |
|---|---|---|---|
| **#11314** → v2 | Bấm Back từ route đã push | Chốt precondition = **chế độ 3 nút**; steps ghi rõ "bấm nút Back trên NAVIGATION BAR" | ⚠️ `pass` cũ không ghi chế độ → **chạy lại** |
| **#11316** → v3 | Back tại route gốc thoát app | Bỏ "hoặc" → tách **2 lượt bắt buộc** (3 nút + cử chỉ) | ⚠️ `pass` cũ chỉ đại diện 1 nhánh → **chạy lại đủ 2 lượt** |
| **#11317** → v2 | Back bằng nút hệ thống khi xem ảnh | Chốt precondition = **chế độ 3 nút** | ⚠️ `pass` cũ không ghi chế độ → **chạy lại**. Đây là TC verify **trực tiếp** code Dev sửa (`image_gallery.dart`) |
| **#11319** → v3 | Back sau khi zoom/kéo ảnh | Bỏ "hoặc" → **2 lượt**; expected nêu thêm rủi ro riêng của lượt cử chỉ (ảnh đang zoom có thể **nuốt cử chỉ vuốt cạnh** — lỗi này không xảy ra ở chế độ 3 nút) | ⚠️ `pass` cũ chỉ đại diện 1 nhánh → **chạy lại đủ 2 lượt** |

> 🔴 **4 TC này đang ở trạng thái `pass` nhưng kết quả đó không còn kết luận được** — vì không ghi lại chế độ điều hướng đã dùng. Studio không cho reset `last_exec` qua `testcase_update`, nên **Leader cần yêu cầu QA chạy lại** và ghi chế độ vào Evidence. Đã ghi cảnh báo này vào `note` của từng TC.

**B. Đã UPDATE 4 TC review** (đều `Chưa test`, sửa an toàn):

| Studio ID | Sửa gì |
|---|---|
| **#11765** → v2 | Rà màn chặn back: mỗi màn chạy **2 lượt**; bảng đối chiếu đổi thành 4 cột (màn / handler kỳ vọng / kết quả 3 nút / kết quả cử chỉ); expected thêm điều kiện **kết quả 2 chế độ phải GIỐNG NHAU** |
| **#11766** → v2 | Đổi tên TC từ "vuốt predictive back" → "back hệ thống ở **CẢ 2 chế độ**"; tách 2 lượt |
| **#11767** → v2 | Ghi rõ **CHỈ ÁP DỤNG chế độ cử chỉ** — "vuốt 90% rồi thả về" không tồn tại ở chế độ 3 nút (nút bấm là thao tác rời rạc, không hủy giữa chừng được). Ghi vào precondition để tester không hiểu nhầm là thiếu lượt |
| **#11777** → v2 | Double-tap back: tách 2 lượt; note thêm rằng chế độ 3 nút **dễ tạo double-tap nhanh hơn** cử chỉ nên khả năng lộ lỗi pop 2 cấp cao hơn |

**C. Đã TẠO 3 TC mới** — nhánh back hệ thống chưa TC nào trong 73 TC cover:

| TC No. (repo) | client_ref | Studio ID | Loại case | Nội dung & vì sao cần |
|---|---|---|---|---|
| TC-REGSHARED001-17 | `T172-RV-19` | **#11888** | Abnormal | **Đổi chế độ điều hướng khi app đang chạy**. Đây là configuration change xảy ra lúc app còn sống — app phải đăng ký lại đường dẫn back cho chế độ mới. Chạy cả 2 chiều. |
| TC-REGSHARED001-18 | `T172-RV-20` | **#11889** | Abnormal | **Back khi bàn phím đang mở** → back lần 1 chỉ đóng bàn phím, lần 2 mới pop màn. Thứ tự ưu tiên xử lý back của hệ thống — rất dễ hỏng khi `onBackPressed` ngừng được gọi. |
| TC-REGSHARED001-19 | `T172-RV-21` | **#11890** | Abnormal | **Back khi đang mở dialog / bottom sheet / picker** → chỉ đóng lớp phủ trên cùng, không pop màn nền. Test 3 loại lớp phủ × 2 chế độ. |

**Trạng thái Studio task #172 sau vòng này:**

| Chỉ số | Trước vòng 5.4 | Sau vòng 5.4 |
|---|---|---|
| Tổng TC | 70 | **73** |
| TC review (`T172-RV-*`) | 18 | **21** |
| `Normal` / `Abnormal` / `Boundary` | 52 / 12 / 4 | **54 / 15 / 4** |
| TC cần **chạy lại** do đổi precondition | — | **4** (#11314, #11316, #11317, #11319) |

> **Tác dụng phụ tích cực**: `Abnormal` tăng 4 → **15**, giúp `REG-SHARED-001` (quan điểm **Cao**, trước đây 12 TC nhưng **0 Abnormal**) nay có đủ Normal + Abnormal + Boundary → **RULE-01 của quan điểm này đã đạt**.

---

## 6. Spec update needed

- [ ] Không cần update spec
- [x] **Cần update spec — chi tiết:**

  **6.1 — Không có spec cho app mobile (gốc rễ)**
  - **Section**: `templates/LME-SYSTEM-SPEC.md` — hiện chỉ mô tả web/backend, mobile app chỉ xuất hiện qua "6 Mobile API endpoints".
  - **Nội dung cần update**: bổ sung mục spec hành vi app mobile — tối thiểu: quy ước điều hướng/back, quy ước timezone hiển thị calendar, giới hạn media theo nơi sử dụng trên app, hành vi khi bị từ chối quyền. Đây là lý do 100% TC để trống `Trạng thái đánh giá spec` và là rủi ro "tester tự suy diễn rồi cho Đạt".
  - **Người chịu trách nhiệm**: PM + Dev mobile.

  **6.2 — Mục 4 file 03 thiếu behavior change "edge-to-edge"**
  - **Section**: `03-dev-impact.md` mục 4 "Behavior changes của target 36".
  - **Nội dung cần update**: bổ sung edge-to-edge (Dev đã test ở mục 3 nhưng không đưa vào danh sách impact) + liệt kê những màn đã rà.
  - **Người chịu trách nhiệm**: Đoàn Thị Bích Hảo (người viết đánh giá).

  **6.3 — Mục 3 file 03 chưa đúng format danh sách caller**
  - **Section**: `03-dev-impact.md` mục 3.
  - **Nội dung cần update**: thay log build bằng **bảng file/function caller** — đặc biệt danh sách đầy đủ nơi còn dùng `WillPopScope`/`onWillPop`.
  - **Người chịu trách nhiệm**: Dev phụ trách (Thinh Nguyen).

  **6.4 — RULE-10: bổ sung nhóm quan điểm cho app mobile**
  - **Section**: `framework/checklist-lme.md`.
  - **Nội dung cần update**: `OBS-001` (runtime diagnostics/logcat) đang được dùng trên Studio nhưng không tồn tại trong framework. Leader quyết định bổ sung nhóm `OBS-*` hoặc quy về mã hiện có. Cân nhắc thêm quan điểm riêng cho **nâng target SDK / OS behavior change** vì đây là loại task sẽ lặp lại hằng năm.
  - **Người chịu trách nhiệm**: QA Lead.

---

## 7. Checklist đã chạy

- [x] **A. Coverage** — chạy đủ; A.1 N/A (Feature, không có bug root cause), A.2 **fail** (F6 GAP), A.3 N/A (D0), A.4 **fail** (T3/T8/T10 GAP), A.5 **pass** (không ORPHAN), A.6 **fail** (fix-shape, xem §3.5)
- [x] **B. Chất lượng từng TC** — **pass phần lớn**: title có keyword rõ, precondition/steps/expected đầy đủ và đo lường được. Trừ `TC-REGSHARED001-05` không atomic (§4.4)
- [x] **C. Chất lượng bộ TC (tổng thể)** — **fail**: tỷ lệ `Normal 88% / Abnormal 8% / Boundary 4%` lệch rất xa gợi ý 40/35/25; không trùng lặp TC; phân bố quan điểm hợp lý về số lượng nhưng dồn 12 TC vào `REG-SHARED-001` mà đều 1 chiều
- [x] **D. Spec alignment** — **không đánh giá được**: không có spec app mobile (xem §6.1)
- [x] **E. Hành chính** — TC No. đúng format canonical (do `/new-task` sinh); file lưu đúng folder; **thiếu**: `Trạng thái đánh giá spec` 100% trống, `Evidence` 100% trống
- [x] **F. Base quan điểm test LME**
  - [x] F.1 Quan điểm (tầng 1) — bảng dưới
  - [x] F.2 Catalog (tầng 2) — **fail ở D**: task chạm media nhưng 0 TC production (GAP-2); **fail ở E**: không dùng giới hạn theo nơi sử dụng (GAP-11); A/B áp dụng hạn chế vì task không có form nhập liệu mới
  - [x] F.3 RULE quy trình — **RULE-01 fail** (6 quan điểm Cao thiếu loại case) · **RULE-02 fail** (37 Đạt không evidence) · RULE-03 N/A (không có bảng ×) · **RULE-06 pass** (TC đi tới máy thật, không dừng ở màn admin — điểm tốt) · RULE-07 N/A (không CRUD DB) · **RULE-08 fail** (media kết luận từ staging) · **RULE-09 fail** (A13/A14 skip) · **RULE-12 fail** (chưa re-test case đã Không đạt)

### F.1 — Bảng quan điểm đối chiếu

| Mã quan điểm | Ưu tiên | Trigger khớp task? | TC cover (suy luận) | Kết luận |
|---|---|---|---|---|
| `FUNC-001` | **Cao** | ◯ — luôn bắt buộc | TC-FUNC001-01..11 (11 TC, **11 Normal / 0 Abnormal / 0 Boundary**) | **RISK** — RULE-01 thiếu 2 loại case, không ghi lý do |
| `FUNC-DATE-001` | **Cao** | ◯ — calendar ca qua đêm (T8) | TC-FUNCDATE001-01 (1 Boundary, **chưa chạy**) | **RISK** → GAP thực thi. Thiếu Normal + Abnormal |
| `FUNC-DRAFT-001` | Trung bình | **×** — Leader xác nhận 2026-08-21: **app không hỗ trợ giữ nội dung soạn dở** → không có hành vi để verify | — | × có lý do — Leader duyệt |
| `FUNC-SEQ-001` | Trung bình | ◯ — back liên tiếp không reload | — | **GAP** → gộp vào `TC-CONC001-01` |
| `CONC-001` | **Cao** | ◯ — double-tap back / cử chỉ back liên tiếp (kịch bản 1) | — | **GAP** → `[MAJOR]` (AP-3). Không nâng BLOCKER vì fix không chạm logic nghiệp vụ |
| `DATA-MIG-001` | **Cao** | ◯ — nâng cấp app, dữ liệu local qua rebuild Kotlin 2.1 | TC-COMPATLEGACY001-01 (1 TC, Normal) | **RISK** — 1 chiều, 1 nhánh OS |
| `COMPAT-LEGACY-001` | **Cao** | ◯ **BẮT BUỘC** — RULE-09 cũ & mới song song | TC-COMPATLEGACY001-01..04 (4 Normal; **2 skip**) | **GAP** → `[BLOCKER]` (GAP-7) |
| `REG-SHARED-001` | **Cao** | ◯ **BẮT BUỘC** — sửa hành vi back dùng chung toàn app | TC-REGSHARED001-01..12 (12 TC, **12 Normal**) | **GAP** → `[BLOCKER]` (GAP-1) — thiếu danh sách nơi ảnh hưởng của Dev |
| `REG-RUN-001` | **Cao** | × — release app client, không có job/dữ liệu server chạy dở; Dev xác nhận không đụng backend | — | × có lý do — Leader duyệt |
| `ENV-003` | **Cao** | ◯ **BẮT BUỘC** — task chạm media (T4) | TC-ENV003-01, -02 (**cả 2 skip**); 0 TC production | **GAP** → `[BLOCKER]` (GAP-2, GAP-3) |
| `DEPLOY-ASSET-001` | **Cao** | ◯ — đổi toàn bộ build engine, ảnh hưởng font/asset bundling | — | **GAP** → `[MAJOR]` (GAP-8) |
| `DEPLOY-LIVE-001` | **Cao** | × — không đổi payload API / cấu trúc request; app cũ vẫn gọi backend cũ | — | × có lý do — Leader duyệt |
| `STATE-001` | **Cao** | ◯ — predictive back là cơ chế gián đoạn mới cho luồng nhiều bước | — | **GAP** → `[MAJOR]` (GAP-7) |
| `SYNC-APP-001` | TB → **Cao** | ◯ — tính năng có mặt cả web và app | TC-SYNCAPP001-01..04 — **thực chất test FCM, không test web⇔app** | **GAP** → `[MAJOR]` (GAP-12) — mã quan điểm dùng sai |
| `MEDIA-001` | TB → **Cao** (output hiển thị khách cuối) | ◯ **BẮT BUỘC** — app gửi/nhận file, ảnh | TC-MEDIA001-01..06 + TC-FUNC001-02, -03 (8 TC, **8 Normal**) | **RISK** → `[MAJOR]` (GAP-11) — thiếu Abnormal + Boundary |
| `MEDIA-CLEAN-001` | TB → Cao | × — app không xóa/thay thế file trên server; fix không chạm luồng xóa media | — | × có lý do |
| `MEDIA-IMG-001` | TB → Cao | × — không đổi logic resize; ảnh gửi từ app đi qua backend không đổi | — | × có lý do — nhưng nên smoke 1 ảnh lớn (đã gộp `TC-MEDIA001-08`) |
| `UI-001` | TB → Cao | ◯ — edge-to-edge, bàn phím che ô nhập | TC-UI001-01, -02 (2 Normal) | **OK** (đủ mức tối thiểu cho TB) |
| `UI-002` | Trung bình | ◯ — khác biệt thiết bị (phone / tablet / foldable) | TC-UI002-01, -02, -03 (**2 blocked**) | **GAP** → `[BLOCKER]` (GAP-6) vì impact T3 = High |
| `UI-003` | TB → Cao | ◯ — permission bị từ chối, mất mạng | TC-UI003-01..04 (**4 Abnormal, 0 Normal**) | **OK** — điểm tốt; chỉ thiếu Normal `[MINOR]` |
| `UI-INPUT-001` | Trung bình | × — không thêm/sửa ô nhập liệu nào | — | × có lý do |
| `OUT-TRUTH-001` | **Cao** | ◯ — thao tác gửi media/tin có thông báo kết quả | Gián tiếp qua TC-MEDIA001-01..06 | **RISK** — không TC nào đối chiếu "báo thành công" với dữ liệu thật ở phía nhận |
| `PERF-LARGE-001` | TB → Cao | × — Dev không nêu; không đổi logic xử lý danh sách | — | × có lý do — `[NIT]` gợi ý smoke |
| `PERM-001/002/003/004` | **Cao** | × — không chạm phân quyền LME (khác runtime permission Android, đã cover ở `UI-003`) | — | × có lý do |
| `MSG-001..005`, `BULK-001`, `FRIEND-001` | **Cao** | × — không chạm logic gửi tin / lọc đối tượng / friend info | — | × có lý do |
| `PAY-*` | **Cao** | × — không chạm thanh toán / gói cước | — | × có lý do |
| `LIFF-ENTRY-001` | **Cao** | × — không phát sinh URL cho LINE user | — | × có lý do |
| `INTG-*`, `JOB-001`, `DATA-AUDIT-001`, `SEC-*` | **Cao** | × — không chạm webhook / job nền / audit log / bảo mật token | — | × có lý do |

> **Tổng kết F.1**: **6 GAP ở quan điểm ưu tiên Cao** → `REG-SHARED-001`, `COMPAT-LEGACY-001`, `ENV-003`, `DEPLOY-ASSET-001`, `STATE-001`, `UI-002` (qua impact T3 High). Trong đó 4 mục nâng `[BLOCKER]`, 2 mục `[MAJOR]`.

---

## 8. Ký duyệt

| Người | Tên | Ngày |
|---|---|---|
| Reviewer (Leader) | | |
| Tester | (đã đọc & hiểu feedback) | |

---

<!-- Draft sinh bởi /review-tc ngày 2026-08-21. Nguồn: 01-bug-task.md + 03-dev-impact.md + 04-tc-list.md (fetch từ MCP LME TEST STUDIO task #172, 50 TC). KHÔNG có 02-spec-reference.md → fallback templates/LME-SYSTEM-SPEC.md (không cover app mobile). Đây là DRAFT cho Leader verify, không phải final. -->

