# 05 — Review Report (round 2)

## 0. Nguồn TC

| Trường | Giá trị |
|---|---|
| Nguồn đã dùng | **(1) Studio task #307** (ticket 40544, round 1, branch `ai_fixbug_40544`, status `released`, chưa archived) — fetch 2026-10-05 |
| Tổng số TC review | **160** |

---

## 1. Coverage — đánh giá ảnh hưởng Dev + diff code

| Chiều | Kết quả |
|---|---|
| **(a) dev-impact** — Dev tự kê ở `03-dev-impact.md` mục 4 | **9/12 mục có TC** (BUG + F1–F10 + T1; D1 = "không có") — **CHƯA ĐỦ** (F1, F2, F8 ở trạng thái RISK) |
| **(b) diff code** — Studio `dev_impact` + `spec_delta` (10 file, +714 −171) | **10/16 điểm có TC** (10 file + 4 rủi ro hồi quy + 2 hành vi đổi) — **CHƯA ĐỦ** |

**Kết luận**: 19/28 điểm kiểm chứng đủ TC · 0 GAP · **8 RISK**.

> So với round 1 (112 TC): 48 TC mới (NEW-113 → NEW-160) đã lấp hết 12 GAP/RISK cũ về Google Sheet, friend info, xoá mềm, CSV, 6 endpoint ghi + 8 endpoint đọc ngoài phạm vi, app mobile. RISK còn lại nằm ở **expected mâu thuẫn** (G1, G2, G4) và **TC chưa có kết luận** (G3, G5–G8).

| # | Vùng thiếu | Chiều | TC hiện có | Thiếu gì | Severity |
|---|---|---|---|---|---|
| **G1** | `deleteFolder` — xoá thư mục **đang chứa** biểu mẫu | `dev-impact` F1 · `diff code` (`dev_impact` liệt kê `deleteFolder`) | NEW-41 `pass` (ticket 41403) · NEW-42 · NEW-147 (thư mục rỗng) | **RISK — expected sai chuẩn.** NEW-41 kỳ vọng biểu mẫu "vẫn còn, hiển thị ở ngoài thư mục". LME không có vùng nào "ngoài thư mục" (mọi biểu mẫu đều thuộc 1 thư mục, mặc định 「未分類」). Kho `TC-FORM-18` ghi hành vi ngược lại: biểu mẫu bên trong bị **xoá mềm**, form-result bị xoá. Cả 2 TC cover nhánh này đều dựa trên giả định chưa ai chốt → xem §4 C1 | `[MAJOR]` |
| **G2** | `copyFormanswer` — sao chép biểu mẫu **của chính bot** (REQ-003: bản sao thuộc bot phiên, tính vào hạn mức) | `dev-impact` F1 · `diff code` | NEW-10 | **RISK — mất TC dương.** Tiêu đề NEW-10 là "sao chép… tạo ra bản sao thuộc đúng bot" nhưng expected đã bị sửa thành "422 trùng 管理名". Bộ TC hiện **không còn TC nào** xác nhận copy hợp lệ tạo bản sao thuộc đúng bot A | `[MAJOR]` |
| **G3** | `Api\FormAnswerController` — 4 API mobile, đặc biệt `apiDetailFormanswerResult` (IDOR thật Dev đã vá bằng JOIN `bot_id`) | `dev-impact` F2 · `diff code` | 10 TC: **9 `skip`** (NEW-98/99/100/101/102/103/104/105/110) · 1 `pass` (NEW-106) | **RISK — 0 TC pass cho phần vá IDOR mobile** và cho validate 400 của API mobile. NEW-160 (app) chỉ cover danh sách biểu mẫu | `[BLOCKER]` |
| **G4** | Hành vi đổi: **danh sách id trộn 2 bot** ở `deleteListFormanswer` / `sortFormAnswer` | `diff code` (REQ-002, REQ-006) | NEW-48 `pass` · NEW-119 `pass` · NEW-8 `pass` · NEW-54 `pass` | **RISK — 2 TC cùng thao tác cho expected loại trừ nhau mà đều `pass`** ⇒ ít nhất 1 false pass. Không còn chuẩn để chấm → xem §4 C2, C3 | `[BLOCKER]` |
| **G5** | Rủi ro hồi quy: JS cũ trong cache + phiên mở trước release (REQ-016) | `diff code` | NEW-94 `pass` (kiểm tĩnh) · NEW-95 `blocked` · NEW-96 `blocked` | **RISK** — 2 kịch bản hành vi thật chưa có kết luận | `[MAJOR]` |
| **G6** | Rủi ro hồi quy: trang cũ có `bot_id` trống/lệch vẫn sửa được (REQ-015 — Dev ghi "CHƯA đối chiếu dữ liệu thật") | `diff code` | NEW-36 `blocked` | **RISK** — TC duy nhất chưa chạy được | `[MAJOR]` |
| **G7** | `index_v3.js` — nhánh lỗi mới của màn danh sách (sort lỗi, đang sao lưu) | `dev-impact` F8 · `diff code` | NEW-92 `blocked` · NEW-93 `skip` · NEW-55 `blocked` · NEW-62 `blocked` | **RISK** — REQ-012 "sắp xếp lỗi phải báo thay vì tải lại như thành công" và nhánh đang sao lưu: **0 pass** | `[MAJOR]` |
| **G8** | `Basic\FormAnswerController` — các nhánh nghiệp vụ mới: trùng tên trang (`addPage`/`updatePage`), đổi bot giữa chừng khi lưu v3, tạo thư mục mới (cập nhật vị trí theo `bot_id`) | `dev-impact` F1 · `diff code` (REQ-009) | NEW-26 · NEW-30 · NEW-63 · NEW-38 — **cả 4 `error`** | **RISK** — trùng tên trang và đổi bot giữa chừng: **0 pass** | `[MAJOR]` |

---

## 2. Thiếu so với quan điểm test

**Kết luận: 20/24 quan điểm Trigger khớp đã cover đủ · 0 GAP · 4 RISK.**

| # | Mã quan điểm | Ưu tiên | Thiếu gì | Severity |
|---|---|---|---|---|
| **Q1** | `DATA-DB-001` | Cao | Normal (NEW-118) + Abnormal (NEW-69, NEW-53) đã `pass`, nhưng TC `Boundary` duy nhất (NEW-119) mâu thuẫn với NEW-48 về cùng `WHERE` scope → chưa kết luận được biên "danh sách trộn". Lấp bằng G4 sau khi chốt §4 C2 | `[MAJOR]` |
| **Q2** | `PERM-002` + `SEC-001` | Cao | **RULE-01**: 21 TC đều là `Abnormal`, **Normal = 0, Boundary = 0** (TC đối chứng dương nằm ở `FUNC-001`, chấp nhận được), không ghi lý do thiếu Boundary. Biên chưa ai test: biểu mẫu **của chính bot A nhưng đã xoá mềm** — helper `findFormForCurrentBot` có loại bản ghi xoá mềm không → `TC-PERM002-01` | `[MAJOR]` |
| **Q3** | `PERM-003` | Cao | Ca change bot / 2 tab lệch phiên chỉ có NEW-63 và đang `error` (= G8) | `[MAJOR]` |
| **Q4** | `DATA-BACKUP-001` | Cao | Nhánh "đang sao lưu → chặn" chỉ có NEW-55, NEW-62, cả 2 `blocked` (= G7). Nhánh khôi phục xoá mềm đã đủ (NEW-12, NEW-145, NEW-60, NEW-61) | `[MAJOR]` |

**Đã loại sau kiểm chứng**: `COMPAT-LEGACY-001` — NEW-45/NEW-76 mang mã lạ `RULE-09`, nhưng nội dung v1 đã được NEW-111 (`REG-SHARED-001`) + NEW-112 (`OUT-TRUTH-001`) cover và cả 2 đều `pass`. `ENV-003`/RULE-08: cả 160 TC có lần chạy gần nhất trên `prd` (run 2472), tổng cộng 3 run trên prd + 14 run trên staging.

---

## 3. TC trùng lặp nội dung

Đã rà 160 TC theo 4 yếu tố. Phát hiện **3 nhóm DUP-SUBSET**, không có DUP-EXACT hay DUP-INFLATE.

| Nhóm trùng | TC giữ lại | TC đề nghị xóa / gộp | Loại trùng | 4 yếu tố trùng nhau | Severity |
|---|---|---|---|---|---|
| Di chuyển biểu mẫu vào thư mục của chính bot | NEW-146 (3 chiều: 未分類→A, A→未分類, A→B) | **NEW-50** → gộp | `DUP-SUBSET` | `FUNC-001` × Normal × 一括フォルダ変更 của bot A × chiều 未分類→thư mục đã nằm trong NEW-146 | `[MINOR]` |
| Khôi phục biểu mẫu đã xoá của chính bot | NEW-145 (đúng thư mục cũ, đủ setting + item, số người trả lời = 0) | **NEW-12** → gộp, chuyển ý "thư mục chứa nó cũng được khôi phục nếu bị xoá cùng" sang NEW-145 | `DUP-SUBSET` | Khôi phục × Normal × biểu mẫu bot A đã xoá mềm × kỳ vọng quay lại đủ trang/câu hỏi/cài đặt | `[MINOR]` |
| Người trả lời upload tệp hợp lệ | NEW-156 (mọi định dạng, file hiển thị ở màn kết quả) | **NEW-88** → gộp | `DUP-SUBSET` | `MEDIA-001` × Normal × upload ảnh hợp lệ trên màn trả lời v3 × file mở được ở phía quản trị | `[MINOR]` |

Không xếp vào nhóm trùng: các TC `TOOL-ERRHYG-001` thiếu tham số (NEW-9/21/49/51/68/71) và NEW-73 (gom 8 endpoint). NEW-73 chỉ kiểm thiếu tham số, các TC lẻ còn kiểm cả **sai kiểu** của từng endpoint. Không có TC duy nhất nào bị đề nghị xoá.

---

## 4. Mâu thuẫn trong TCs

Đã rà 160 TC × `spec-features/admin/form-answer/feature-spec.md` + `kho-tcs/fa011-taobieumau-フォーム作成.md` (nhóm Folder form · Copy form · Xóa & khôi phục form · Form rẽ nhánh — page) + bảng 1.1 RULE-13. Phát hiện **6 mâu thuẫn**.

| # | Loại | TC liên quan | Nội dung check trùng nhau | Expected A | Expected B / nguồn đối chiếu | Khả năng sai | Severity | Ai chốt |
|---|---|---|---|---|---|---|---|---|
| **C1** | `CONF-KHO` + `CONF-TC` | NEW-41, NEW-42 ↔ kho `TC-FORM-18`, NEW-12 | Xoá thư mục đang chứa biểu mẫu | NEW-41: thư mục mất, biểu mẫu "**vẫn còn, hiển thị ở ngoài thư mục**, không bị xoá theo". NEW-42 ngầm cùng giả định ("2 biểu mẫu không bị đưa ra ngoài thư mục") | `TC-FORM-18`: biểu mẫu bên trong **xoá mềm** sang 「削除したフォーム」, form-result bị xoá, remind bị huỷ. NEW-12 cũng ngầm theo hướng này ("thư mục… được khôi phục nếu trước đó bị xoá cùng") | (a) NEW-41/42 do AI tự suy ("đối chứng âm"), cụm "ngoài thư mục" không tồn tại trên UI → **TC sai**; hoặc (b) bản fix #40544 / ticket 41403 đã đổi hành vi thành "chuyển về 未分類" → kho `TC-FORM-18` cần update. NEW-41 đang `pass` nên cần xem ticket 41403 kết luận thế nào | `[MAJOR]` | Leader + Dev |
| **C2** | `CONF-TC` | NEW-48 ↔ NEW-119 | `deleteListFormanswer` với danh sách trộn id bot A + bot B, phiên bot A | NEW-48: ID_A1 **bị xoá**, ID_B1 giữ nguyên (xử lý phần hợp lệ, đúng REQ-002 "lọc id bot khác ra") | NEW-119: **403**, không xoá được biểu mẫu nào ở cả 2 bot | **Cả 2 đều `pass`** ⇒ chắc chắn 1 false pass. NEW-119 do ngannt viết lại theo kết quả thực tế (sau ticket 41492 đổi cross-bot sang 403) → nhiều khả năng NEW-48 lỗi thời; hoặc 403 toàn request là regression so với REQ-002 | `[BLOCKER]` | Dev |
| **C3** | `CONF-TC` | NEW-8 ↔ NEW-54 (+ REQ-006) | Sắp xếp với danh sách id trộn 2 bot | NEW-8 (`sortFormAnswer`): **403**, thứ tự cả 2 bot giữ nguyên. Tiêu đề NEW-8 vẫn là "chỉ ảnh hưởng biểu mẫu của bot mình" | NEW-54 (sắp xếp thư mục): thư mục bot A **được sắp xếp**, bot B giữ nguyên. REQ-006: "id không thuộc bot thì bỏ qua và vẫn trả 200 cho phần hợp lệ" | Khác endpoint nhưng cùng một quy tắc "danh sách trộn". Hoặc NEW-8 đúng hành vi mới (403 toàn request) → REQ-006 + NEW-54 cần update; hoặc NEW-8 đang ghi lại regression | `[MAJOR]` | Dev |
| **C4** | `CONF-TC` | NEW-25 ↔ NEW-31 | Tên trang để trống bị từ chối | NEW-25 (thêm trang): 「**ページ名**を入力してください」 | NEW-31 (đổi tên trang): 「**管理名**を入力してください」 — đây là message của **tên quản lý biểu mẫu** (kho `TC-FORM-39`), không phải tên trang | NEW-31 đang test nhầm field, hoặc màn sửa trang dùng sai message (ticket 41649 gắn vào NEW-31) | `[MAJOR]` | Leader |
| **C5** | `CONF-KHO` | NEW-10 ↔ kho `TC-FORM-53`, `TC-FORM-57` | Sao chép biểu mẫu giữ nguyên 管理名 mặc định | NEW-10: **422** 「管理名[00]はすでに登録済みです。重複する管理名は登録できません。」. Ghi chú: "tính năng mới không cho tạo/sao chép/edit trùng tên quản lý" | Kho: modal copy mặc định 管理名 = tên gốc (`TC-FORM-53`) và copy thành công khi giữ nguyên (`TC-FORM-57`) | Quy tắc chống trùng 管理名 là tính năng mới → kho FA-011 nhóm Copy form + Tạo form cần update; hoặc NEW-10 ghi nhầm | `[MAJOR]` | Leader / PM |
| **C6** | `CONF-SPEC` (RULE-13) | NEW-83 | Biểu mẫu đổi số câu hỏi khi người dùng đang trả lời | NEW-83: **409** | Bảng 1.1 `checklist-lme.md`: vi phạm rule nghiệp vụ = **422**, bảng không có 409 | Expected đang ghi theo code Dev (Dev chuẩn hoá 409) thay vì quy ước dự án. Theo RULE-13: giữ expected theo quy ước, ghi mã code đang trả ở `Ghi chú` và báo Dev | `[MAJOR]` | Dev |

---

## 5. Issues khác

### Chất lượng nguồn TC

| # | Severity | TC / phạm vi | Vấn đề | Đề xuất fix |
|---|---|---|---|---|
| 1 | **[BLOCKER]** | NEW-26 · NEW-30 · NEW-38 · NEW-135 · NEW-140 · NEW-141 · NEW-143 · NEW-152 · NEW-159 | 9 TC `error` **chưa gắn ticket bug** và chưa ghi lý do (harness hay sản phẩm). Task đã `released` | Triage từng TC: lỗi sản phẩm → raise ticket; lỗi harness → ghi lý do + chạy lại |
| 2 | **[MAJOR]** | 28 TC (11 `skip` · 7 `blocked` · 10 `error`) | Pass 132/160 = 82,5% (đạt ngưỡng 80%). Nhưng phần không có kết luận lại rơi đúng vào các điểm rủi ro nhất: API mobile (9/10 skip), deploy/cache (NEW-95/96), sao lưu (NEW-55/62), trang cũ (NEW-36) | Ưu tiên chạy lại theo thứ tự G3 → G7 → G5 → G6 |
| 3 | **[MAJOR]** | 28 TC `status = draft` | Task `reviewState = done`, đã `released` nhưng 28 TC chưa được duyệt | Duyệt hoặc xoá trước khi đóng task |

### Chất lượng từng TC

| # | Severity | TC / phạm vi | Vấn đề | Đề xuất fix |
|---|---|---|---|---|
| 4 | **[MAJOR]** | NEW-10 · NEW-119 · NEW-8 | **Tiêu đề và expected nói 2 chuyện khác nhau** (mục 3 BƯỚC 4a). NEW-10: "tạo ra bản sao" ↔ expected lỗi trùng tên. NEW-119: "chỉ xoá phần của mình" ↔ expected 403 không xoá gì. NEW-8: "chỉ ảnh hưởng bot mình" ↔ expected 403 không đổi gì | Sửa tiêu đề theo expected đã chốt (sau §4 C2, C3, C5). NEW-10 nên đổi thành TC trùng tên rồi bổ sung TC dương `TC-FUNC001-01` |
| 5 | **[MAJOR]** | NEW-123 · NEW-131 · NEW-132 (403 **hoặc** rỗng) · NEW-103 · NEW-105 · NEW-110 (không ghi mã) | **RULE-13**: TC nhóm `API` không ghi 1 mã HTTP cụ thể. Expected chấp nhận 2 kết quả thì TC không bao giờ fail ở tầng mã | Chốt 1 mã theo bảng 1.1 (cross-bot = 403 hoặc 404, chọn 1), ghi mã code đang trả ở `Ghi chú` |
| 6 | **[MAJOR]** | NEW-72 | Expected trộn "ghi nhận thực tế trả 200" với "theo quy ước phải 403" → TC `pass` dù mã sai (ticket 41623 đang mở) | Expected chỉ giữ 403 + bản ghi bot B còn nguyên. Mã thực tế ghi ở `Ghi chú` |
| 7 | **[MINOR]** | NEW-41 · NEW-147 · NEW-38 · NEW-148 | Expected chỉ kiểm UI, không kiểm `form_answer_folder` / `form_answer.group_id` (RULE-07) — chính vì vậy câu "hiển thị ở ngoài thư mục" của NEW-41 không đo được | Thêm điểm kiểm `group_id` của biểu mẫu sau thao tác |
| 8 | **[NIT]** | NEW-56 · NEW-65 · NEW-94 | Đây là kiểm tĩnh bằng đọc source/route, manual tester không chạy được | Giữ làm bằng chứng phạm vi, ghi rõ `Chạy = manual vì đọc source` |

---

## 6. TCs thừa / ngoài phạm vi task

| # | TC | Vì sao ngoài phạm vi | Bằng chứng | Đề xuất | Severity |
|---|---|---|---|---|---|
| 1 | NEW-135 | Kiểm layout modal 項目を追加 (2 nhóm, màu `#FFFFFF` trên nền `#5799DB`) — tầng giao diện không bị diff chạm | `setting_form_items.js` chỉ +/−20 dòng, thêm nhánh `error` cho upload, không đổi modal | Chuyển sang bộ regression chung của kho FA-011 (`TC-FORM` nhóm Màn edit form) | `[NIT]` |
| 2 | NEW-141 | Kiểm mặc định 作成しない và 2 vùng hiển thị khi bật chẩn đoán — tầng hiển thị không bị diff chạm | `diagnostic_content.js` chỉ +9 dòng, bắt khoảng 400-499 khi bật/tắt bị từ chối. Phần đó đã có NEW-16/NEW-17 | Chuyển sang bộ regression chung | `[NIT]` |

Các TC regression khác lấy từ kho (NEW-136 → NEW-160) **không** flag: đều dẫn được về REQ-014 (luồng chính không hồi quy) và đi qua handler JS hoặc endpoint có trong diff.

---

## 7. TCs đề xuất bổ sung (2)

**Đã đối chiếu trước khi viết** (BƯỚC 5a/5b):

| Mục | Kết quả |
|---|---|
| File kho TCs đã đọc | `kho-tcs/fa011-taobieumau-フォーム作成.md` — nhóm Folder form (14 TC), Copy form (19), Xóa & khôi phục form (8), Form rẽ nhánh — page |
| Vùng regression phát hiện từ kho | `TC-FORM-18` (xoá folder có form → xoá mềm form + form-result) · `TC-FORM-53/57/59` (copy form) · `TC-FORM-73/76` (xoá/khôi phục) |
| Conflict expected vs kho | NEW-41/42 vs `TC-FORM-18` → C1 · NEW-10 vs `TC-FORM-53/57` → C5. Đã đưa §4 + §8 |
| GAP dùng lại TC kho (không viết mới) | **G1 → `TC-FORM-18`** "Xóa folder ĐANG CHỨA form → xóa mềm toàn bộ form trong folder". Chỉ đẩy lên Studio **sau khi** Leader/Dev chốt C1; nếu chốt hành vi mới là "về 未分類" thì sửa expected NEW-41 thay vì dùng TC kho |
| GAP dùng lại TC đã có trên Studio (chỉ cần chạy / sửa) | **G3** → chạy NEW-98…NEW-105, NEW-110 · **G4** → sửa NEW-48 hoặc NEW-119 sau khi chốt C2, sửa NEW-8 sau C3 · **G5** → NEW-95, NEW-96 · **G6** → NEW-36 · **G7** → NEW-55, NEW-62, NEW-92, NEW-93 · **G8** → NEW-26, NEW-30, NEW-38, NEW-63 (= Q3). Nội dung các TC này đã đúng phạm vi, viết mới chỉ tạo trùng |
| Căn cứ TC regression `R<x>` | Không có TC R |
| Xác nhận chống trùng | Đã đối chiếu 160 TC ở BƯỚC 0 + kho FA-011. **Không TC đề xuất nào trùng**. `TC-FUNC001-01` khác NEW-10 (copy với 管理名 mới, kiểm chủ sở hữu + hạn mức); `TC-PERM002-01` khác NEW-13 (bản ghi xoá mềm **của chính bot**, không phải bot khác) |

| ID | Nhóm | Mã quan điểm | Màn hình/chức năng | Loại case | Chạy | Phạm vi ENV | Tên case | Tiền điều kiện | Các bước thực hiện | Dữ liệu nhập | Kết quả mong đợi | Kết quả thực thi | Ghi chú |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TC-FUNC001-01 | UI | FUNC-001 | Form answer — Danh sách biểu mẫu (v3) | Normal | auto | dev, local, prd, staging | Sao chép biểu mẫu của chính bot với 管理名 mới tạo bản sao thuộc đúng bot đang chọn và được tính vào hạn mức | Tài khoản quản trị có 2 bot A, B. Đang chọn bot A (gói Free mới, đang có 2 biểu mẫu). Bot A có biểu mẫu 「TC307-A-フォーム」 gồm 2 trang, 3 câu hỏi, nằm trong thư mục 「TC307-A-フォルダ」. Bot A không ở trạng thái đang sao lưu. Ghi lại số biểu mẫu của bot B | 1. Mở màn danh sách biểu mẫu của bot A<br>2. Bấm menu 3 chấm của 「TC307-A-フォーム」, chọn sao chép<br>3. Đổi 管理名 thành 「TC307-A-コピー」, giữ thư mục 「TC307-A-フォルダ」, bấm コピーを作成<br>4. Tải lại màn danh sách, mở thư mục 「TC307-A-フォルダ」 và mở bản sao<br>5. Bấm tạo biểu mẫu mới (lần thứ 4)<br>6. Chuyển sang bot B, mở màn danh sách biểu mẫu | 管理名 mới: 「TC307-A-コピー」 | Bước 3: sao chép thành công, không hiện thông báo lỗi<br>Bước 4: bản sao 「TC307-A-コピー」 nằm trong 「TC307-A-フォルダ」 của bot A, đủ 2 trang và 3 câu hỏi như bản gốc; bản gốc không đổi<br>Bước 5: bị chặn với thông báo 「現在のプランは利用できない機能です。アップグレードが必要になります。」 (bản sao đã tính vào hạn mức 3 biểu mẫu của bot A)<br>Bước 6: danh sách bot B không có 「TC307-A-コピー」, số biểu mẫu bot B không đổi |  | Lấp G2 · REQ-003 · Môi trường: dev/staging/prd · Đánh giá spec: Spec ghi rõ (REQ-003 Studio; kho `TC-FORM-57`) · Evidence: ảnh danh sách bot A/B trước–sau · thay vai trò TC dương mà NEW-10 đã mất |
| TC-PERM002-01 | API | PERM-002 | Form answer — Danh sách biểu mẫu đã xoá | Boundary | auto | dev, local, staging | Thao tác ghi lên biểu mẫu của chính bot đã bị xoá mềm bị từ chối và biểu mẫu vẫn ở trạng thái đã xoá | Đang chọn bot A. Bot A có biểu mẫu 「TC307-A-削除済み」 (id = ID_ADEL) vừa xoá, đang nằm trong màn 削除したフォーム. Ghi lại trạng thái công khai và tin nhắn trả lời hiện tại của ID_ADEL | 1. Ở phiên bot A, gửi yêu cầu đổi trạng thái công khai (`changePublicFormAnswer`) với id = ID_ADEL<br>2. Ghi lại mã trạng thái và thân phản hồi<br>3. Gửi yêu cầu lưu tin nhắn trả lời (`saveMessageReply`) với id = ID_ADEL, nội dung 「削除後の更新」<br>4. Ghi lại mã trạng thái và thân phản hồi<br>5. Mở màn danh sách chính và màn 削除したフォーム của bot A | id = ID_ADEL · nội dung tin nhắn 「削除後の更新」 | Bước 2 và 4: **404** với thông báo 「フォームが見つかりません。」, không trả 200 hoặc 500<br>Bước 5: 「TC307-A-削除済み」 vẫn chỉ nằm ở 削除したフォーム, không quay lại danh sách chính; khôi phục ra thì trạng thái công khai và tin nhắn trả lời đúng như trước bước 1 |  | Lấp Q2 (RULE-01 Boundary cho `PERM-002`) · biên của helper `findFormForCurrentBot`: id thuộc đúng bot nhưng đã xoá mềm · Môi trường: dev/staging (abnormal ghi dữ liệu) · Đánh giá spec: Spec không ghi — cần Dev xác nhận helper có loại bản ghi xoá mềm không · Mã 404 theo bảng 1.1 RULE-13 (dữ liệu không tồn tại) |

---

## 8. Spec update needed

| # | Section spec | Nội dung cần update | Nguồn mâu thuẫn | Ai chốt |
|---|---|---|---|---|
| 1 | `spec-features/admin/form-answer/feature-spec.md` EP-27 + kho `TC-FORM-18` | Spec chỉ ghi "Xóa thư mục", không ghi số phận biểu mẫu bên trong. Chốt: xoá mềm theo thư mục (như kho) hay chuyển về 「未分類」 → sửa NEW-41/NEW-42 hoặc kho `TC-FORM-18` cho khớp | §4 C1 · ticket 41403 | Leader + Dev |
| 2 | REQ-002 · REQ-006 (Studio) | Quy tắc "danh sách id trộn 2 bot": xử lý phần hợp lệ + bỏ id lạ (REQ hiện tại) hay 403 toàn request (hành vi NEW-8/NEW-119 đang ghi nhận). Áp chung cho `deleteListFormanswer`, `sortFormAnswer`, sắp xếp thư mục | §4 C2, C3 | Dev |
| 3 | Kho FA-011 nhóm Form rẽ nhánh — page | Message khi tên trang để trống ở màn **sửa** trang: 「ページ名を入力してください」 hay 「管理名を入力してください」 | §4 C4 · ticket 41649 | Leader |
| 4 | Kho FA-011 nhóm Copy form + Tạo form (`TC-FORM-53`, `TC-FORM-57`) | Bổ sung quy tắc mới "không cho tạo/sao chép/sửa trùng 管理名" (422 + message) | §4 C5 | Leader / PM |
| 5 | REQ-009 · REQ-010 (Studio) | Dev chuẩn hoá 403/409/410 cho nhánh nghiệp vụ; bảng 1.1 dự án dùng 422 (và 403/404 cho cross-bot). Phần lớn TC đã theo bảng 1.1, riêng NEW-83 còn 409 | §4 C6 | Dev |
| 6 | `03-dev-impact.md` mục 4.2 | Ghi "Không có data ảnh hưởng" nhưng Studio `dev_impact` nêu xoá lan 7 bảng con ở `deleteItem`/`deleteItemV3`/`deleteListFormanswer` và `saveFormAnswerPointSetting` ghi `form_answer.using_old_version` | Studio `dev_impact` | Dev |
