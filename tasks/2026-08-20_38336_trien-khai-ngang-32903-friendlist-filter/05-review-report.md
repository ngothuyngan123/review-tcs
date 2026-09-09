# 05 — Review Report

## Thông tin

| Trường | Giá trị |
|---|---|
| Bug ID | `#38336 — Triển khai ngang Bug KH #32903: Action friend list redirect từ các màn send all, csv, tag, richmenu thì bị lỗi không theo filter` |
| Reviewer (Leader) | `<Leader điền>` — draft sinh bởi `/review-tc` |
| Tester được review | **`AI` (MCP LME TEST STUDIO, job #338)** — 48/49 TC do AI sinh, 1 TC `cucdtk@mcp`, **0 TC do human viết** |
| Ngày review | `2026-08-20` |
| Version TCs | Studio `round 2`, toàn bộ TC `status=draft` |
| Vòng review | `Round 1` (Studio `reviewed=false`, `reviewState=tester`) |

> **Input thiếu**: không có `02-spec-reference.md` → **Spec reference: dùng [LME-SYSTEM-SPEC](../../templates/LME-SYSTEM-SPEC.md) tổng, không có spec riêng cho task này.**
> **Input thiếu**: `01-bug-task.md` **không có Steps to reproduce / Expected / Actual** (ticket dạng "Triển khai ngang", không phải bug report từ KH) → không có baseline KH để đối chiếu TC.

---

## 1. Verdict

- [ ] **APPROVED**
- [ ] **APPROVED WITH CHANGES**
- [x] **REJECTED** — Có issue BLOCKER, cần fix và review lại

**Lý do ngắn gọn**: Bộ TC có **độ phủ trigger tốt** (12 màn nguồn đều có TC, expected đo lường được bằng số đếm tay), nhưng **không thể nghiệm thu** vì 3 nhóm lý do: (1) **42/49 TC (86%) chưa có kết luận** — 37 `skip` + 5 chưa chạy, và **1 TC đang FAIL với ticket #40060 chưa đóng**; (2) thiếu hẳn **3 quan điểm ưu tiên Cao có trigger khớp task** — `DATA-DB-001`, `PERM-003`, `ENV-003` (+ `COMPAT-LEGACY-001` còn thiếu nhánh bản ghi cũ); (3) **0 TC chạy trên production** trong khi task chạm **job nền + asset cache** (RULE-08).

---

## 2. Tóm tắt cho member

Bộ TC này **phủ trigger rất tốt** — cả 12 màn nguồn bàn giao bộ lọc (gửi hàng loạt, tag, CSV ×2 điểm vào, rich menu, khoá trả lời tự động, bước sự kiện, lịch hành động, phân tích chéo, lịch hẹn, salon, URL param) đều có TC riêng, và `Kết quả mong đợi` viết theo kiểu **đếm tay số người rồi đối chiếu** (VD "đúng 201 bạn được gắn tag, không phải tổng số bạn bè") — đúng tinh thần `BULK-001`. Đây là điểm mạnh thật, giữ nguyên cách viết này.

Ba việc phải làm trước vòng review sau: (1) **chạy cho xong** — 37 TC đang `skip` và 5 TC chưa chạy khiến 86% bộ TC không có giá trị nghiệm thu, và TC-FUNC004-03 đang FAIL (ticket #40060) nghĩa là **fix chưa đạt ở biên 0 người**; (2) **bổ sung 3 quan điểm Cao còn trống** — đặc biệt `PERM-003` (localStorage là **của trình duyệt, không thuộc bot nào** — bàn giao ở bot A rồi đổi sang bot B thì sao?) và `DATA-DB-001` (thao tác hàng loạt chưa TC nào kiểm ở tầng DB); (3) **dọn 8 cặp TC trùng** — 16/49 TC là bản sao, trong đó vài cặp có `Kết quả mong đợi` **khác nhau**, không biết bản nào là chuẩn.

---

## 3. Coverage Matrix

> Cột **Chạy** thêm ngoài template: bộ TC này đã được thực thi nên trạng thái chạy quyết định giá trị nghiệm thu. Ký hiệu: `P`=pass · `F`=fail · `S`=skip · `—`=chưa chạy.

| Impact | Loại | Priority | TCs map (suy luận) | # TC | Chạy | Status |
|---|---|---|---|---|---|---|
| **BUG** — 4 điều kiện sai dấu ngoặc trong `modal.orderBy` nuốt hết nhánh nạp bộ lọc | Fix | — | TC-TOOLKNOW002-01 (tái hiện #32903), TC-FUNC001-01 (không bàn giao → mặc định) | 2 | 1S / 1P | **RISK** — TC tái hiện bug gốc đang `skip`, chưa có bằng chứng fix chạy |
| **F1** — `modal.orderBy` | Function | **Direct** | TC-FUNC001-01, TC-TOOLKNOW002-01, TC-FUNCSEQ001-01, TC-TOOLOLDREC001-01/02, TC-CONC003-01, TC-FUNC004-01/02, TC-UI003-01 | 9 | 2P / 7S | **RISK** — đủ 3 chiều Normal/Abnormal/Boundary nhưng 7/9 chưa kết luận |
| **F2** — `modal.searchFormAll` | Function | Indirect | Gián tiếp qua mọi TC hiển thị danh sách | ~20 | — | OK (regression) |
| **F3** — `actionListFriend.sendActionFriends` | Function | Indirect | TC-FUNC001-06/07, TC-FUNC004-04/05, TC-TOOLNEGCTRL001-02/03, TC-SELECTSCOPE001-01 | 7 | 1P / 5S / 1— | RISK |
| **F4** — `addTag` / `removeTag` / `addRichMenu` / `SendTemplate` | Function | Indirect | TC-BULK001-01/02/03, TC-MSG001-01/02 | 5 | 1P / 3S / 1— | **RISK** — cả 5 TC đều `Normal`, **không có Abnormal/Boundary** (xem RULE-01) |
| **F5** — `FriendlistController::sendActionFriend` | Function | Indirect | TC-FUNC004-04 (=200), TC-FUNC004-05 (>200), TC-TOOLNEGCTRL001-02/03, TC-JOB002-01/02 | 6 | 1P / 3S / 2— | RISK |
| **F6** — `FriendlistController::index` (bàn giao qua URL param) | Function | Indirect | TC-REGSHARED001-13, TC-STATE001-01 | 2 | **2—** | **RISK** — cả 2 TC **chưa từng chạy** |
| **F7** — `Conversation::advanceFilterPost` | Function | Indirect | Không có TC verify riêng ở tầng query | 0 | — | **GAP** — chỉ verify gián tiếp qua số người trên UI, không có kiểm chứng DB |
| **F8** — `showFriendhasTag` (`tag/index.js` **+** `tag/index_v2.js`) | Function | Indirect | TC-FUNC001-03, TC-FUNC004-03 (**FAIL**) | 2 | 1F / 1S | **GAP (một phần)** — không TC nào phân biệt **2 phiên bản file** (RULE-09) |
| **F9** — `showNumberFilter` CSV (`csv_management.js` + `create_download_file.js`) | Function | Indirect | TC-FUNC001-04 (tạo file tải về), TC-REGSHARED001-03 (danh sách bản ghi) | 2 | 2S | OK — đủ **2 điểm vào** |
| **F10** — `showNumberFilter` broadcast | Function | Indirect | TC-FUNC001-02, TC-REGSHARED001-02, TC-TOOLNEGCTRL001-01 | 3 | 1P / 2S | OK |
| **F11** — `showNumberFilter` rich menu | Function | Indirect | TC-FUNC001-05, TC-SEARCH001-01/02 | 3 | 3S | OK |
| **D1** — bản ghi lịch 【自動生成】友だち一括アクション + điều kiện lọc kèm theo | Data | — | TC-FUNC004-05, TC-JOB002-01/02, TC-TOOLNEGCTRL001-02/03 | 5 | 1P / 2S / 2— | **RISK** — không TC nào **query DB** xác nhận điều kiện đã lưu; **không TC nào test bản ghi tạo TRƯỚC fix** |
| **D2** — khoá localStorage bàn giao (reply_filter / CSV / lịch / rich menu) | Data | — | TC-TOOLOLDREC001-01/02, TC-CONC003-01, TC-FUNCSEQ001-01, TC-STATE001-01 | 5 | 4S / 1— | OK (đủ chiều one-shot + tồn đọng) |
| **D3** — schema DB | Data | — | Dev khẳng định KHÔNG đổi schema | — | — | N/A |
| **T1** — Friend List (FA-013) | Feature | **High** | 14 TC màn 友だちリスト + 12 TC panel 一括アクション | 26 | 4P / 19S / 3— | RISK |
| **T2** — Broadcast (FA-008) | Feature | **High** | TC-FUNC001-02, TC-REGSHARED001-02, TC-TOOLNEGCTRL001-01 | 3 | 1P / 2S | OK |
| **T3** — Tag Management (FA-012) | Feature | **High** | TC-FUNC001-03, TC-FUNC004-03 | 2 | **1F** / 1S | **RISK** — có TC **đang FAIL** (ticket #40060) |
| **T4** — CSV Management (FA-014) | Feature | **High** | TC-FUNC001-04, TC-REGSHARED001-03 | 2 | 2S | OK |
| **T5** — Rich Menu (FA-004) | Feature | **High** | TC-FUNC001-05, TC-SEARCH001-01/02 | 3 | 3S | OK |
| **T6** — Action Schedule (FA-016) — job nền | Feature | **High** | TC-JOB002-01/02, TC-FUNC004-05 | 3 | 1S(local) / 1— / 1S | **RISK** — chỉ chạy `local`, **chưa chạy production** (RULE-08) |
| **T7** — 自動応答 + イベントステップ *(Dev không liệt kê ở 4.3)* | Feature | **High** | TC-REGSHARED001-04/05/06 | 3 | 3S | OK |
| **T8** — アクションスケジュール (thêm/sửa) *(Dev không liệt kê ở 4.3)* | Feature | **High** | TC-REGSHARED001-07/08/09 | 3 | 3S | OK |
| **T9** — クロス分析 *(Dev không liệt kê ở 4.3)* | Feature | Medium–High | TC-REGSHARED001-10 | 1 | 1S | **RISK** — 1 TC, chỉ `Normal` (AP-3 happy-path-only) |
| **T10** — シナリオ / bàn giao qua URL param *(Dev không liệt kê ở 4.3)* | Feature | Medium | TC-REGSHARED001-13, TC-STATE001-01 | 2 | **2—** | **RISK** — cả 2 chưa chạy |

**Tổng kết**: 0 GAP tuyệt đối ở tầng F/D/T (trừ F7 và một phần F8) — **độ phủ trigger tốt**. Rủi ro nằm ở **trạng thái chạy** và ở **tầng quan điểm** (§F.1), không ở tầng liệt kê impact.

### ORPHAN TCs

| TC ID | Title | Lý do orphan | Hành động đề xuất |
|---|---|---|---|
| **TC-TOOLSCOPE001-01** | Rà soát nhánh bàn giao không còn màn nào kích hoạt — xác nhận không cần test giao diện | Không test sản phẩm — đây là **hoạt động rà soát nội bộ của tool** (audit phạm vi), nhưng đang được tính là 1 TC `pass` ở staging → **thổi phồng tỷ lệ pass** | **Remove** khỏi bộ TC, chuyển nội dung sang phần ghi chú phạm vi. Nếu giữ thì phải đánh dấu không tính vào coverage |
| TC-LIST001-01 | Sau khi mở Friend List bằng bộ lọc bàn giao — chuyển trang vẫn giữ đúng phạm vi đã lọc | **`requirement_keys` rỗng** — TC hợp lệ về nội dung (map T1/F2) nhưng không liên kết requirement nào | **Map lại** vào REQ-001 hoặc REQ-004, không remove |

---

## 3.5 Fix-shape analysis (adversarial)

| Mục | Giá trị |
|---|---|
| **Fix shape** (đọc mục 2 dev-impact) | **Specific code check** (KHÔNG phải generic catch-all) — dời dấu ngoặc đóng ở **đúng 4 điều kiện** đã biết trước, trong 1 file JS. **Kết hợp 3 shape phụ**: `sửa hàm dùng chung / shared` (→ REG-SHARED-001) · `JS / asset` (→ DEPLOY-ASSET-001) · `filter / đối tượng gửi tin` (→ MSG-001, BULK-001) |
| **Trigger space cần cover** | 4 điều kiện được sửa (khoá trả lời tự động · quản lý CSV · lịch hành động · rich menu) + **các nhánh nạp bộ lọc lần đầu được chạy sau nhiều năm**: gửi hàng loạt · tag · CSV (2 điểm vào) · rich menu · lịch hành động · phân tích chéo · bước sự kiện · lịch hẹn · salon + **fallback không bàn giao** + **bàn giao qua URL param** |
| **Số trigger TCs hiện cover** | **12/12 màn nguồn có TC** (broadcast · tag · CSV×2 · richmenu · 自動応答 · イベントステップ · アクションスケジュール · クロス分析 · カレンダー予約 · サロン予約 · URL param) + fallback không bàn giao ✓ → **độ phủ trigger ĐẠT**. Dev có cung cấp **danh sách nơi ảnh hưởng** đầy đủ ở mục 3 (11 mục) → thoả điều kiện REG-SHARED-001 |
| **KH report dạng** | **Không có report KH** — ticket dạng "Triển khai ngang", description chỉ nêu phạm vi test, **không có Steps/Expected/Actual**. Bug gốc KH là **#32903** (ticket khác, không nằm trong folder review này) |
| **Alternative root causes cần verify** | Rủi ro thấp: Dev đã **quét toàn repo** xác nhận đúng 4 chỗ cùng mẫu lỗi, và TC test **end-to-end từng màn nguồn** nên sẽ bắt được cả trường hợp màn nguồn không ghi khoá bàn giao. **Còn 1 nhánh chưa loại trừ**: bản ghi lịch/CSV/broadcast **tạo TRƯỚC fix** có thể mang định dạng bộ lọc cũ (xem BLOCKER-1, BLOCKER-5) |
| **Anti-patterns dính** | **AP-2** (một phần) · **AP-3** (T9, T10) · **AP-4** · **AP-5** (TC-TOOLSCOPE001-01). **Không dính AP-1** (fix không phải generic catch) · **Không dính AP-6** (mục 3 đầy đủ 11 caller) |

> **Kết luận fix-shape**: trigger space **đã cover đủ** — đây KHÔNG phải chỗ bỏ lọt. Rủi ro bỏ lọt thật nằm ở **phạm vi WHERE ở tầng DB** (DATA-DB-001), **cách ly đa bot của localStorage** (PERM-003), **môi trường production** (ENV-003) và **bản ghi tạo trước version-up** (COMPAT-LEGACY-001).
>
> **Cập nhật 2026-08-21 — Leader thu hẹp phạm vi**: nhóm TC `REG-RUN-001` (lịch 【自動生成】 tạo trước fix / job chạy dở khi release) đã được **Leader quyết định là KHÔNG cần thiết** và gỡ khỏi §5. Rủi ro này vì vậy **không còn được tính là BLOCKER** trong report. Ghi nhận lại để truy vết: mục 4.2 dev-impact có nêu *trước fix, lịch tự sinh được tạo với điều kiện lọc rỗng*.

---

## 3.6 Audit ĐIỂM VÀO Friend List — rà toàn hệ thống LME

> Bổ sung theo yêu cầu Leader (2026-08-20): *"hệ thống LME còn chỗ nào mà click vào sẽ nhảy ra màn friend list nữa không?"*
>
> **Nguồn đối chiếu** (không suy đoán): [`spec-features/admin/friend-filter/`](../../spec-features/admin/friend-filter/) — SC-003 「絞り込みモーダル」, modal lọc **dùng chung cho 61+ màn hình**. Bảng `parent_type` lấy từ [`db/db-mapping.md`](../../spec-features/admin/friend-filter/db/db-mapping.md) (15 giá trị) + [`web/api-spec.md`](../../spec-features/admin/friend-filter/web/api-spec.md) + [`web/logic-spec.md`](../../spec-features/admin/friend-filter/web/logic-spec.md) §side-effects, đối chiếu chéo với mục 3 `03-dev-impact.md`.
>
> **Nguyên tắc lọc**: chỉ `parent_type` **có tính `filterNumber`** mới hiển thị được con số bạn bè → mới có thể bấm để nhảy sang friend list. `step_message` và `filter_manager` **không tính `filterNumber`** nên không có số để bấm.

| # | `parent_type` / điểm vào | Màn hình | Tính `filterNumber`? | TC hiện có | Status |
|---|---|---|---|---|---|
| 1 | `broadcast` / `broadcast-v2` — màn **tạo** | 一斉配信 tạo tin | Có | TC-FUNC001-02, TC-TOOLNEGCTRL001-01 | **OK** |
| 2 | `broadcast` — màn **sửa** | 一斉配信 sửa tin | Có | — (TC-FUNC001-02 chỉ ghi "Mở màn **tạo**") | **GAP** |
| 3 | `broadcast` — **copy** (EP-16 `/ajax/copy-broadcast-v2`) | 一斉配信 sao chép | Có | — | **GAP** ⚠️ |
| 4 | `broadcast` — tab **配信予約** (`wait_to_send`) | Danh sách tin, cột 配信数 | Có | TC-REGSHARED001-02 ghi *"下書き **(hoặc** 配信予定)"* → tester chỉ chạy **1 trong 2** | **RISK** |
| 5 | `broadcast` — tab **下書き** (`draft`) | Danh sách tin, cột 配信数 | Có | như trên — chỉ 1 trong 2 | **RISK** |
| 6 | `broadcast` — tab **配信履歴** (`delivered`/`delivering`/`send_false`) | Danh sách tin, cột 配信数 | Có | — | **GAP** ⚠️ |
| 7 | Tag list — số người mỗi tag | タグ管理 | (không qua `filters_v2`) | TC-FUNC001-03, TC-FUNC004-03 (**FAIL** #40060) | RISK |
| 8 | CSV — màn tạo file tải về | CSV管理 作成 | Có | TC-FUNC001-04 | **OK** |
| 9 | CSV — danh sách bản ghi | CSV管理 一覧 | Có | TC-REGSHARED001-03 | **OK** |
| 10 | `setting_rich_menu` | リッチメニュー 表示設定 | Có | TC-FUNC001-05, TC-SEARCH001-01/02 | **OK** |
| 11 | **`filter-rich-menu-toggle`** | **リッチメニュー切り替え** (tab 3 của action tap area, bảng `rich_menu_switch_items`) | Có | — | **GAP** ⚠️ |
| 12 | Auto-reply (filter V1/V2) | 自動応答 | Có | TC-REGSHARED001-04/05 | **OK** |
| 13 | `filter_remind_form` | イベントステップ | Có | TC-REGSHARED001-06 | **OK** |
| 14 | `action_schedule` | アクションスケジュール | Có | TC-REGSHARED001-07/08/09 | **OK** |
| 15 | `cross_analysis` | クロス分析 | Có (`isCountOnly=true`) | TC-REGSHARED001-10 | RISK (1 TC Normal) |
| 16 | `calendar-course-setting-status-send-after-booking` → `calendar_courses.filter_id_send_after_booking` | **レッスン予約** — コース (tin sau đặt lịch) | Có | TC-REGSHARED001-11 | **OK** |
| 17 | **`calendar-salon-course-setting-status-send-after-booking`** → `calendar_salon_courses.filter_id` + `filter_number` | **サロン予約 — コースの絞り込み表示** | Có | — | **GAP** ⚠️ *(Leader chỉ định)* |
| 18 | **`calendar-salon-staff-setting-status-send-after-booking`** → `calendar_salon_staffs.filter_id` + `filter_number` | **サロン予約 — スタッフ詳細の絞り込み表示** | Có | — | **GAP** ⚠️ *(Leader chỉ định)* |
| 19 | **`calendar-setting-show-booking-form`** → `calendar_managements.filter_id_show_booking` | **レッスン予約 — 予約フォーム表示設定** | Có | — | **GAP** ⚠️ |
| 20 | **`filter-calendar-salon-booking`** → `calendar_salons.filter_calendar_salon_ids` + `number_filter_salon` | **サロン予約 — cấp salon** | Có | TC-REGSHARED001-12 *(mô tả "サロン予約 > cài đặt lịch > tin nhắn" — **không rõ** map vào `filter-calendar-salon-booking` hay `calendar-salon-course-...`)* | **AMBIGUOUS** |
| 21 | `modal_action` (action details) | Modal multi action | — (chỉ dùng khi xóa: `deleteActionFilters`) | — | GAP (ưu tiên thấp) |
| 22 | `step_message` | ステップ / シナリオ | **KHÔNG** | TC-REGSHARED001-13, TC-STATE001-01 (qua **URL param**, không qua localStorage) | RISK — cả 2 chưa chạy |
| 23 | `filter_manager` | Quản lý bộ lọc lưu sẵn | **KHÔNG** | — | Không áp dụng (không có số để bấm) |

**Kết luận audit — 6 điểm vào CHƯA có TC nào**, đều thuộc phạm vi bản sửa (cùng dùng `modal_filter_v2.js`):

| GAP | Điểm vào | Vì sao nguy hiểm |
|---|---|---|
| **GAP-11** | 一斉配信 tab **配信履歴** | Cột 配信数 ở tab này map `send_count` **hoặc** `filter_number` (db-mapping dòng 184) — khác 2 tab kia. Broadcast đã gửi thì filter **read-only** (`preview_filter_broadcast = "全員"`), hành vi bàn giao có thể khác hẳn |
| **GAP-12** | 一斉配信 **copy** | *"Khi copy: broadcast, templates, actions, **filters**, child broadcasts đều được clone"* (`FilterV2::cloneFilters()`). Quan điểm **`MSG-001` liệt kê đích danh rủi ro "filter bị mất sau copy/sort"** |
| **GAP-13** | 一斉配信 màn **sửa** | TC hiện chỉ mở màn **tạo**; broadcast cha còn có logic **cascade copy filter sang broadcast con** khi save |
| **GAP-14** | **サロン予約 — コースの絞り込み表示** | Salon course dùng cột `filter_id`/`filter_number` **riêng**, khác lesson (`filter_*_send_after_booking`) → nhánh code khác, chưa ai test |
| **GAP-15** | **サロン予約 — スタッフ詳細の絞り込み表示** | Salon staff cũng có `filter_id`/`filter_number` riêng; thêm ràng buộc `is_all_course` / `course_ids` |
| ~~GAP-16~~ | ~~リッチメニュー切り替え (`filter-rich-menu-toggle`)~~ | **ĐÃ BỎ** — Leader xác nhận (2026-08-21) màn này **không có mục nhảy ra friend list**. TC-REGSHARED001-17 cũ đã gỡ khỏi §5 |
| **GAP-17** | **レッスン予約 — cài đặt 予約ページの非表示** | `calendar_managements.filter_number_show_booking` + `filter_id_show_booking` — nhánh riêng, chưa có TC *(Leader đính chính tên màn: **予約ページの非表示**, không phải "予約フォーム表示設定")* |
| **GAP-18** | **レッスン予約 — コースの絞り込み表示** | ⚠️ **Reviewer nhận định sai ở vòng trước**: TC-REGSHARED001-11 (file 04) test mục 「対象人数」 của *tin nhắn gửi sau khi đặt lịch*, **KHÔNG phải** 「絞り込み表示」 của コース. Đây là 2 setting khác nhau → lesson course **vẫn là GAP** |
| **GAP-19** | **サロン予約 — cài đặt 予約ページの非表示** | Cặp đối xứng của GAP-17 bên salon; ứng viên `parent_type=filter-calendar-salon-booking` |

> ⚠️ **Lưu ý về mức tin cậy**: bảng trên xác định **nơi modal lọc được dùng** (chắc chắn, từ spec + DB schema). Việc con số bạn bè ở từng màn có **render thành link bấm được** hay không thì spec không ghi rõ, và `get_salon_detail` qua MCP **không trả về** `filter_id`/`filter_number`. Vì vậy TC bổ sung ở §5 đều có **bước 1 xác nhận phần tử UI có tồn tại**; nếu không bấm được thì ghi `N/A` kèm screenshot, **không tự dựng request thay thế** (cùng cách xử lý mà Studio đã dùng ở TC-FUNC004-03).

---

## 4. Issues phát hiện

### 4.1 Blocker (phải fix trước khi merge)

- **[BLOCKER] GAP-2 — `DATA-DB-001` (Cao, BẮT BUỘC với mọi UPDATE/DELETE): không TC nào xác minh ở tầng DB, không TC nào kiểm `WHERE` scope trên 2 tài khoản.** Task có **UPDATE hàng loạt** (gắn tag / gỡ tag / đổi rich menu / gửi mẫu tin) nhưng mọi `Kết quả mong đợi` chỉ đếm trên **UI** (VD "số người của tag giảm đúng 2"). Vi phạm **RULE-07** (kiểm DB là bắt buộc, không thay bằng UI). — **Fix**: thêm TC-DATADB001-01/02/03 ở §5, mỗi TC kèm câu query và ảnh chụp kết quả trước/sau trên **2 bot**.

- **[BLOCKER] GAP-3 — `PERM-003` (Cao, BẮT BUỘC khi có change bot): localStorage là bộ nhớ của TRÌNH DUYỆT, không gắn với bot nào — nhưng không TC nào test đổi bot.** Kịch bản chưa ai kiểm: bấm số người ở bot A (ghi khoá bàn giao) → **đổi sang bot B** → mở danh sách bạn bè. Bộ lọc của bot A có bị áp cho friend list của bot B không? Nếu điều kiện chứa `tag_id` của bot A thì bot B sẽ lọc theo ID không thuộc về nó. Đối chiếu Catalog `MAP-PERM-01`. — **Fix**: thêm TC-PERM003-01/02/03 ở §5.

- **[BLOCKER] GAP-4 — `ENV-003` (Cao) + **RULE-08**: 0/49 TC chạy trên production.** Phân bố env thực tế: `staging` 41 · `local` 3 · `chưa chạy` 5 · **`prd` 0**. Task chạm **job nền** (D1 — lịch tự sinh, Catalog `ENV-JOB`: production tách **3 job độc lập** callback/broadcast/scenario trong khi staging chỉ có 1 job) và **asset cache** (Catalog `ENV-ASSET`). RULE-08 ghi rõ: **job không được kết luận từ staging**. — **Fix**: thêm TC-ENV003-01/02/03 ở §5 với `Môi trường test = PRODUCTION`.

- **[MAJOR] GAP-5 — `COMPAT-LEGACY-001` (Cao) + **RULE-09**: chưa TC nào kiểm bản ghi tạo TRƯỚC version-up.** Chưa ai kiểm bản ghi CSV / broadcast / lịch **tạo trước lần version-up gần nhất** có mở được danh sách đã lọc không — đúng chỗ Dev tự cảnh báo *"nhánh nạp bộ lọc lần đầu thực sự chạy sau nhiều năm bị chặn"*. — **Fix**: thêm TC-COMPATLEGACY001-02 ở §5.
  > **Cập nhật 2026-08-21**: Leader quyết định **bỏ** 2 TC còn lại của nhóm này — TC-COMPATLEGACY001-01 (`tag/index.js` ⇄ `index_v2.js`) và TC-COMPATLEGACY001-03 (rich menu bản cũ ⇄ v2). Vì vậy hạng mục hạ từ **[BLOCKER] → [MAJOR]**, chỉ còn nhánh bản ghi cũ.

- **[BLOCKER] TC-FUNC004-03 (Studio #10570) đang FAIL với ticket #40060 — fix CHƯA đạt ở biên 0 người.** TC "Quản lý tag — bấm số người của tag chưa gắn cho ai" kỳ vọng `検索結果：0人`; kết quả `fail` ở staging ngày 2026-08-20. Đây **đúng là triệu chứng của bug gốc** (bộ lọc mất → hiện toàn bộ bạn bè). **Không được approve khi TC này còn đỏ.** Ghi chú thêm: Studio báo `openBugs: 0` nhưng TC vẫn `fail` và có ticket #40060 → **số liệu mâu thuẫn**, cần xác minh #40060 đã đóng chưa. — **Fix**: Dev xử lý #40060, chạy lại TC, rồi mới review vòng 2.

- **[BLOCKER] 42/49 TC (86%) không có kết luận — bộ TC chưa đủ điều kiện nghiệm thu (RULE-11).** Chi tiết: `skip` 37 · chưa chạy 5 · `pass` 6 · `fail` 1. Trong đó **TC quan trọng nhất đang `skip`**: TC-TOOLKNOW002-01 (tái hiện bug gốc #32903), TC-BULK001-01/02/03 (phạm vi thao tác hàng loạt), TC-FUNC004-05 (lịch tự sinh >200 người, **có gắn ticket #39711 nhưng chưa từng chạy**). — **Fix**: chạy hết 37 TC `skip` + 5 TC chưa chạy, hoặc ghi rõ lý do `skip` cho từng TC nếu môi trường không dựng được.

- **[BLOCKER] GAP-11/12/13 — màn "send all" là phạm vi ticket nêu ĐÍCH DANH nhưng mới phủ 1 màn tạo + 1 trong 2 tab.** Description Redmine ghi rõ *"Test triển khai ngang khi access friend list từ các MH: **Màn send all**..."*. Thực tế:
  - **配信履歴** (`delivered`/`delivering`/`send_false`): **0 TC**. Cột 配信数 ở tab này map `send_count` **hoặc** `filter_number` (khác 2 tab kia), và broadcast đã gửi thì filter ở trạng thái **read-only** (`preview_filter_broadcast = "全員"`) → hành vi bàn giao có thể khác hẳn.
  - **配信予約 + 下書き**: chỉ có TC-REGSHARED001-02, và bước 1 viết *"chuyển sang tab 下書き **(hoặc 配信予定)**"* → tester chỉ chạy **1 trong 2**, không phải cả hai.
  - **Màn sửa** broadcast: TC-FUNC001-02 bước 1 chỉ ghi *"Mở màn **tạo** tin gửi hàng loạt"*. Màn sửa còn có logic **cascade copy filter sang broadcast con** khi save.
  - **Copy** broadcast (EP-16 `/ajax/copy-broadcast-v2`): **0 TC**, dù spec ghi *"Khi copy: broadcast, templates, actions, **filters**, child broadcasts đều được clone"* và quan điểm **`MSG-001` liệt kê đích danh rủi ro "filter bị mất sau copy/sort"**.
  — **Fix**: thêm TC-LIST001-02/03/04, TC-FUNC001-08, TC-DATAREF001-02 ở §5. Tách TC-REGSHARED001-02 thành **2 TC riêng** cho 2 tab, bỏ chữ "hoặc".

### 4.2 Major (nên fix)

- **[MAJOR] GAP-14/15/17/18/19 — 5 điểm vào Friend List khác chưa có TC nào** (xem §3.6). Tất cả đều dùng chung `modal_filter_v2.js` nên nằm trong bán kính ảnh hưởng của bản sửa, dù không có tên trong ticket:
  - **`calendar-salon-course-...`** — サロン予約 **コースの絞り込み表示** (`calendar_salon_courses.filter_id` + `filter_number`). **Khác lesson**: lesson dùng `filter_id_send_after_booking`, salon dùng `filter_id` → **2 nhánh code khác nhau**, chỉ nhánh lesson có TC.
  - **`calendar-salon-staff-...`** — サロン予約 **スタッフ詳細の絞り込み表示** (`calendar_salon_staffs.filter_id` + `filter_number`), thêm ràng buộc `is_all_course` / `course_ids`.
  - **レッスン予約 — コースの絞り込み表示** (GAP-18): ⚠️ **đính chính nhận định vòng trước** — TC-REGSHARED001-11 ở file 04 test mục 「対象人数」 của *tin nhắn gửi sau khi đặt lịch*, **không phải** 「絞り込み表示」 của コース. Lesson course vì vậy **vẫn trống**. Spec `friend-filter` chưa ghi `parent_type`/cột cho setting này → **phải hỏi Dev** trước khi chạy.
  - **レッスン予約 — cài đặt 予約ページの非表示** (GAP-17): `calendar_managements.filter_number_show_booking` + `filter_id_show_booking`.
  - **サロン予約 — cài đặt 予約ページの非表示** (GAP-19): cặp đối xứng bên salon, ứng viên `parent_type=filter-calendar-salon-booking`.
  — **Fix**: thêm TC-REGSHARED001-14, -15, -16, -17, -18, -19 ở §5.
  > **Đã bỏ theo quyết định Leader (2026-08-21)**: `filter-rich-menu-toggle` (リッチメニュー切り替え) — Leader xác nhận màn này **không có mục nhảy ra friend list**.

- **[MAJOR] TC-REGSHARED001-12 map `parent_type` KHÔNG rõ ràng.** Tiêu đề "Cài đặt tin nhắn đặt lịch salon", bước 1 ghi *"サロン予約 > cài đặt lịch > tin nhắn"*, mục 「対象人数」 — không xác định được đang test `filter-calendar-salon-booking` (cấp salon, cột `number_filter_salon`) hay `calendar-salon-course-setting-status-send-after-booking` (cấp course, cột `filter_number`). Đây đúng là trường hợp **"TC mơ hồ"** theo coverage-matrix. — **Fix**: yêu cầu ghi rõ trong `Ghi chú` TC đó `parent_type` + cột DB đang verify; nếu chỉ cover cấp salon thì cấp course vẫn là GAP-14.

- **[MAJOR] AP-2 / SYMPTOM-ONLY: `01-bug-task.md` không có Steps to reproduce / Expected / Actual.** Ticket "Triển khai ngang" chỉ nêu phạm vi, bug gốc nằm ở ticket khác (#32903) không có trong folder review. Không có baseline KH để đối chiếu TC nào là "đúng flow khách gặp". — **Fix**: lấy Steps/Expected/Actual từ **#32903** bổ sung vào file 01, hoặc ghi rõ "không tái hiện được, chỉ verify theo cách fix".

- **[MAJOR] AP-4: thiếu link PR / diff để verify fix shape thực tế.** Trường "Commit / Pull Request" trong `03-dev-impact.md` = `<chưa có PR>`; chỉ có commit hash `c94956fb05` + branch `ai_fixbug_38336`. Không xem được diff nên **không kiểm chứng được** khẳng định "đúng 4 chỗ, đã sửa hết, không sót". — **Fix**: yêu cầu Dev cung cấp link diff/PR.

- **[MAJOR] RULE-01 — `BULK-001` (ưu tiên **Cao**) chỉ có 3 TC và **cả 3 đều `Normal`**, không có Abnormal/Boundary, không ghi lý do.** TC-BULK001-01/02/03. — **Fix**: thêm TC-BULK001-04 (Abnormal: bộ lọc khớp 0 người mà vẫn bấm thao tác hàng loạt) + TC-BULK001-05 (Boundary: đúng biên 200 / 201) — xem §5.

- **[MAJOR] RULE-06 — `MSG-001` dừng ở tầng bản ghi tin nhắn, KHÔNG verify nhận thật trên LINE app.** TC-MSG001-01 `Kết quả mong đợi` = *"Số bản ghi tin nhắn tạo thêm đúng bằng 3"*. Quan điểm `MSG-001` yêu cầu **"bắt buộc xác nhận nhận thật trên LINE app, không chỉ nhìn số đếm"**, evidence phải là **danh sách người nhận thật trên LINE app**. `MSG-001` là quan điểm có cảnh báo *"gửi nhầm đối tượng = lỗi nghiêm trọng nhất"*. — **Fix**: thêm TC-MSG001-03 ở §5 (nhận thật trên LINE app, iOS + Android).

- **[MAJOR] `DATA-COUNT-001` (Cao, BẮT BUỘC khi màn có số đếm) mới đối chiếu 2 nguồn, quan điểm yêu cầu 4 nguồn.** TC hiện đối chiếu *số người ở màn nguồn* ⇄ *`検索結果：N人` ở friend list*. Thiếu **CSV export** và **API**. Quan điểm này được đánh dấu *"lỗi lặp nhiều nhất lịch sử bug — 12 ticket Closed"*. — **Fix**: thêm TC-DATACOUNT001-01 ở §5.

- **[MAJOR] 8 cặp TC TRÙNG — 16/49 TC (33%) là bản sao, một số cặp có `Kết quả mong đợi` KHÁC NHAU.** Toàn bộ 8 TC nhân bản (Studio id `11092`–`11099`) được tạo cùng lúc `2026-08-18 09:18:32`, `temp_id = null` (round 2 append nhưng **không gỡ bản round 1**):

  | Cặp trùng | Studio ID | Nội dung |
  |---|---|---|
  | TC-DEPLOYASSET001-01 / -02 | 10564 / 11092 | steps + expected + precondition **đều khác nhau** |
  | TC-FUNC004-01 / -02 | 10560 / 11093 | **giống hệt 100%** (steps + expected + precondition trùng khớp) |
  | TC-SEARCH001-01 / -02 | 10574 / 11094 | **đều khác nhau** |
  | TC-MSG001-01 / -02 | 10578 / 11095 | steps + precondition giống, **expected KHÁC** |
  | TC-FUNC001-06 / -07 | 10579 / 11096 | **đều khác nhau** |
  | TC-TOOLNEGCTRL001-02 / -03 | 10584 / 11098 | steps + precondition giống, **expected KHÁC** |
  | TC-REGSHARED001-08 / -09 | 10588 / 11099 | steps + expected giống, precondition khác |
  | TC-JOB002-01 / -02 | 10583 / 11097 | **đều khác nhau** |

  Hệ quả: không xác định được bản nào là chuẩn để chấm; và 3/5 TC "chưa chạy" chính là bản nhân đôi. — **Fix**: trên Studio, **merge từng cặp** thành 1 TC (giữ bản có expected đầy đủ hơn), rồi `/new-task` fetch lại file 04.

- **[MAJOR] Toàn bộ 49 TC thiếu cột `Trạng thái đánh giá spec`** (`spec_status = null`). Không TC nào ghi `Spec ghi rõ` / `Spec không ghi` / `Đã hỏi leader` → **nguy cơ tự suy diễn rồi cho Đạt**, đặc biệt với hành vi "bấm số người mở danh sách đã lọc" vốn **không có spec viết rõ** (Dev tự nhận là *"hành vi đúng theo thiết kế"*). — **Fix**: điền `spec_status` cho từng TC; case `Spec không ghi` phải ghi rõ **đã hỏi ai**.

- **[MAJOR] RULE-02 — cột `Evidence thực tế` trống toàn bộ 49/49 TC, trong đó 6 TC đã tick `pass`.** `testcase_list` không trả về evidence và không TC nào ghi **loại evidence bắt buộc** ở `Ghi chú`. RULE-02: *chỉ tick Đạt khi đã đính kèm đúng loại bằng chứng; không chấp nhận "đã xem, OK"*. — **Fix**: với mỗi TC ghi loại evidence bắt buộc; 6 TC `pass` phải bổ sung evidence hoặc trả về `Chưa test`.

- **[MAJOR] 12/49 TC (24%) dùng mã quan điểm KHÔNG tồn tại trong `framework/checklist-lme.md` → không map được coverage.** `TOOL-NEGCTRL-001` (3) · `TOOL-OLDREC-001` (2) · `SEARCH-001` (2) · `JOB-002` (2, checklist chỉ có `JOB-001`) · `TOOL-KNOW-002` (1) · `SELECT-SCOPE-001` (1) · `TOOL-SCOPE-001` (1). Nhóm `TOOL-*` là quan điểm nội bộ của Studio về **chất lượng bộ TC**, không phải quan điểm test nghiệp vụ LME. — **Fix**: map lại về mã tầng 1 (gợi ý: `SEARCH-001`→`LIST-001`; `JOB-002`→`JOB-001`; `SELECT-SCOPE-001`→`BULK-001`; `TOOL-OLDREC-001`→`DATA-CACHE-001`; `TOOL-KNOW-002`→`FUNC-001`), hoặc Leader quyết định bổ sung mã mới vào checklist theo **RULE-10**.

- **[MAJOR] `01-bug-task.md` auto-fill từ Redmine nhưng checkbox "Tester verify auto-fill chính xác" CHƯA tick.** Yêu cầu tester đọc lại detail Redmine #38336 và tick trước khi review có giá trị.

- **[MAJOR] `03-dev-impact.md` auto-fill từ Redmine nhưng checkbox "Tester verify auto-fill chính xác" CHƯA tick.** Đặc biệt quan trọng ở task này vì **bảng 4.1 là SUY RA từ mục 3** (báo cáo AI chỉ liệt kê *file* thay đổi, không liệt kê function) và **T7–T10 do reviewer bổ sung**, Dev không đưa vào 4.3. F/D/T có thể chưa đầy đủ hoặc mapping sai.

- **[MAJOR] GAP-6 — `DEPLOY-LIVE-001` (Cao): không TC nào test tab mở sẵn TRƯỚC deploy.** Khác `DEPLOY-ASSET-001` (đã có 2 TC): đây là **client cũ gọi server mới**. Vì Dev **không tăng version asset**, kịch bản "user đang mở màn friend list với JS cũ khi release diễn ra" là rất thực tế. — **Fix**: thêm TC-DEPLOYLIVE001-01 ở §5.

- **[MAJOR] GAP-7 — `PERF-LARGE-001` (→Cao với gửi tin/bulk): quy mô test tối đa mới 201 bạn bè.** Quan điểm yêu cầu **hỏi/tra số liệu khách hàng lớn nhất thực tế** rồi tạo test data bằng hoặc lớn hơn. Bug thật đã ghi nhận: *"CSV chỉ export 500 dòng đầu"*. — **Fix**: hỏi PM số friend của khách lớn nhất, bổ sung TC ở quy mô đó.

- **[MAJOR] GAP-8 — `LIST-001` (BẮT BUỘC với màn danh sách có filter) mới cover 1/4 góc.** Chỉ có TC-LIST001-01 (giữ filter khi chuyển trang). Thiếu: search bằng **tên LINE** và **tên quản lý** trong phạm vi đã lọc; **xóa hết bản ghi ở trang cuối → tự lùi trang**. Lưu ý góc thứ 4 — *"click vào số đếm phải mở đúng danh sách tương ứng"* — **chính là bug này**. — **Fix**: bổ sung TC cho 2 góc còn thiếu.

- **[MAJOR] GAP-9 — `SEC-ISO-001` (Cao): chưa test 2 tab cùng ghi khoá bàn giao.** TC-CONC003-01 có test "2 bộ lọc bàn giao cùng tồn tại" nhưng ở **1 tab**. Kịch bản thiếu: tab 1 bấm số người ở màn tag, tab 2 bấm số người ở màn CSV, rồi mở friend list ở tab 3. — **Fix**: bổ sung TC multi-tab.

- **[MAJOR] GAP-10 — `DATA-REF-001` (Cao): chưa test tag bị xóa/đổi tên GIỮA lúc bàn giao.** Catalog `MAP-TAG-05` yêu cầu: *tag bị xóa hoặc đổi tên khi đang được điều kiện gửi tin tham chiếu → nơi tham chiếu không được hỏng, **đối tượng gửi không được sai***. Khoá bàn giao lưu điều kiện tag trong localStorage và **tiêu thụ ở lần mở sau** → có cửa sổ thời gian để tag bị xóa. — **Fix**: thêm TC-DATAREF001-01 ở §5.

- **[MAJOR] AP-3 — regression happy-path-only cho T9 (クロス分析) và T10 (シナリオ URL param).** Mỗi tính năng chỉ 1–2 TC, precondition đều là data sạch, không có edge state. T9 chỉ có 1 TC `Normal`; T10 có 2 TC nhưng **cả 2 chưa chạy**. Lưu ý Dev tự cảnh báo: các nhánh này *"lần đầu thực sự chạy sau nhiều năm bị chặn"* → rủi ro định dạng dữ liệu bàn giao đã lỗi thời **cao hơn** bình thường. — **Fix**: mỗi tính năng thêm ≥1 TC ở trạng thái biên (0 người / điều kiện phức hợp AND+OR / bản ghi cũ).

- **[MAJOR] TC-FUNC004-05 (Studio #10582) có gắn ticket bug #39711 nhưng `last_exec = skip` — chưa từng chạy.** Không rõ ticket #39711 phát sinh từ đâu nếu TC chưa chạy. — **Fix**: xác minh quan hệ TC ↔ #39711; nếu là bug đã biết thì phải chạy TC để xác nhận trạng thái sau fix.

- **[MAJOR] `REQ-010` được 4 TC tham chiếu nhưng KHÔNG có trong danh sách requirements active của Studio.** `task_get_context(requirements)` chỉ trả REQ-001→REQ-009 và REQ-011. 4 TC liên quan: TC-REGSHARED001-10/11/12 (phân tích chéo, lịch hẹn, salon) và TC-TOOLSCOPE001-01. — **Fix**: hỏi Studio/Dev xem REQ-010 bị gỡ hay bị ẩn; nếu đã gỡ thì 3 TC màn クロス分析 / カレンダー / サロン đang **mồ côi requirement**.

### 4.3 Minor (có thể fix sau)

- **[MINOR] `TC No.` trong file 04 là do `/new-task` sinh lại theo quy ước repo, KHÔNG phải ID gốc của Studio.** Studio dùng `temp_id` (`NEW-1`…`NEW-33`) và `id` (10556–11099). Đã giữ trace ngược ở cột `Ghi chú` (`Studio #<id> (<temp_id>)`), nhưng 8 TC nhân bản có `temp_id = null` nên chỉ trace được bằng `id`.

- **[MINOR] TC-LIST001-01 không có `requirement_keys`** — TC duy nhất trong bộ bị bỏ trống liên kết requirement.

- **[MINOR] 1/49 TC có `priority = Medium`, 48 TC còn lại `priority = null`.** Không nhất quán. Theo quy ước repo thì ưu tiên suy từ **mã quan điểm**, không phải cột riêng — nên bỏ hẳn cho đồng nhất.

- **[MINOR] Tiêu đề TC chưa chứa **tên function** để Leader suy ra impact.** VD "Quản lý tag — bấm số người của một tag mở đúng danh sách bạn có tag đó" đọc được nhưng không có keyword `showFriendhasTag` / `modal.orderBy`. Template khuyến nghị tiêu đề chứa keyword (tên function / DB table / màn hình) — hiện mới có **màn hình**. — **Fix**: thêm tên function vào tiêu đề hoặc `Ghi chú`.

### 4.4 Nit (gợi ý)

- **[NIT] AP-5 — TC-TOOLSCOPE001-01 nên tách khỏi bộ TC nghiệm thu** (xem bảng ORPHAN §3). Nó đang là 1 trong 6 TC `pass`, làm tỷ lệ pass thật (6/49) trông khả quan hơn thực tế (5/49 nếu loại TC này).

- **[NIT] Cân nhắc gộp TC-FUNC001-06/07 và TC-BULK001-01/02/03 theo hướng data-driven** (1 TC + bảng biến thể thao tác) thay vì nhân TC cho từng loại thao tác hàng loạt — giúp bộ TC gọn và dễ bảo trì hơn.

- **[NIT] `DATA-ID-001`**: nếu hệ thống cho phép **2 tag trùng tên hiển thị**, nên có 1 TC bàn giao bộ lọc theo tag trùng tên để chắc điều kiện lưu bằng `tag_id` chứ không phải tên. Ưu tiên thấp vì fix không chạm logic định danh.

- **[NIT] Theo RULE-11**, các mục ở §4 `checklist-lme.md` (`ADM-01` — *bộ lọc/tìm kiếm phải đúng ngay lần đầu thao tác, không cần bấm lại lần 2*) **rất gần** với task này nhưng chưa đủ bằng chứng nên **chỉ nêu ở mức gợi ý**, không flag. Nếu task này lọt bug ra production thì đây là ứng viên để nâng thành quan điểm chính thức (**RULE-10**).

---

## 5. TCs đề xuất bổ sung

> Member copy thẳng vào `04-tc-list.md` ở round tiếp theo. **16 cột canonical.** TC No. không trùng với TC đã có ở file 04.

| TC No. | Mã quan điểm liên kết | Loại case | Tiêu đề test case | Điều kiện tiền đề | Các bước thực hiện | Dữ liệu test/input | Kết quả mong đợi | Kết quả thực thi | Evidence thực tế | Môi trường test | Người thực hiện | Ngày thực hiện | Số ticket bug | Trạng thái đánh giá spec | Ghi chú |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TC-DATADB001-01 | DATA-DB-001 | Normal | `sendActionFriends`: query DB xác nhận bộ lọc bàn giao ghi đúng `WHERE` — 2 bot cùng tên tag | - 2 bot A và B do cùng 1 tài khoản quản lý<br>- **Cả 2 bot** đều có tag tên `TC38336_SAME` (khác `tag_id`)<br>- Bot A: tag gắn cho 3 bạn; Bot B: tag gắn cho 5 bạn | 1. Chọn bot A, vào タグ管理, bấm số người của tag `TC38336_SAME`.<br>2. Ở friend list mở ra, gắn tag `TC38336_MARK` cho toàn bộ nhóm đã lọc.<br>3. Query DB đếm số bạn có tag `TC38336_MARK` theo `bot_id` của A và theo `bot_id` của B.<br>4. Lặp lại bước 1–3 với bot B. | Bot A: 3 bạn có `TC38336_SAME`.<br>Bot B: 5 bạn có `TC38336_SAME`.<br>Phép tính tay: A→3, B→5. | Query DB: bot A có **đúng 3** bạn được gắn `TC38336_MARK`, bot B **không thay đổi** (0 bạn). Sau khi lặp cho bot B: bot B có **đúng 5**, bot A vẫn giữ 3. Điều kiện `WHERE` phải có đủ `bot_id`. | Chưa test | | STAGING | | | | Spec không ghi | Bổ sung theo review — lấp **GAP-2 / BLOCKER-2**, cover **F3 + F4 + D1**. **RULE-07**: evidence bắt buộc là **ảnh chụp kết quả query kèm câu query**, trước và sau, trên **cả 2 bot** |
| TC-DATADB001-02 | DATA-DB-001 | Abnormal | `removeTag` hàng loạt ở bot A không được đụng dữ liệu bot B | - Như TC-DATADB001-01<br>- Cả 2 bot đều có tag `TC38336_TARGET` gắn cho toàn bộ bạn bè | 1. Chọn bot A, mở friend list qua bàn giao bộ lọc tag `TC38336_SAME` (3 bạn).<br>2. Gỡ tag `TC38336_TARGET` cho nhóm đã lọc.<br>3. Query DB đếm số bạn còn tag `TC38336_TARGET` ở bot A và bot B. | Bot A: 10 bạn có `TC38336_TARGET`, lọc còn 3.<br>Bot B: 10 bạn có `TC38336_TARGET`. | Bot A còn **7** bạn có `TC38336_TARGET` (10−3). Bot B vẫn **nguyên 10**. Không có bản ghi liên kết mồ côi sau khi gỡ. | Chưa test | | STAGING | | | | Spec không ghi | Bổ sung theo review — lấp **GAP-2**, cover **F4**. Evidence: query DB 2 bot trước/sau |
| TC-DATADB001-03 | DATA-DB-001 | Boundary | Bộ lọc bàn giao khớp toàn bộ bạn bè — thao tác hàng loạt không tạo khoá mồ côi | - Bot có đúng 20 bạn bè<br>- Bộ lọc bàn giao đặt điều kiện khớp **cả 20** | 1. Từ 一斉配信 đặt điều kiện khớp toàn bộ 20 bạn, bấm số người.<br>2. Chạy action đổi rich menu cho toàn bộ nhóm.<br>3. Query DB đếm bản ghi liên kết friend ↔ rich menu.<br>4. Xóa rich menu vừa gán, mở lại friend list và màn cài đặt hiển thị. | 20 bạn bè, bộ lọc khớp 20/20. | Đúng **20** bản ghi liên kết được tạo, không thừa không thiếu. Sau khi xóa rich menu, **không còn ID mồ côi** trỏ tới rich menu đã xóa; mở lại list/detail/preview không lỗi. | Chưa test | | STAGING | | | | Spec không ghi | Bổ sung theo review — lấp **GAP-2**, cover **F4 + D2**. `DATA-DB-001` mục (3) khóa mồ côi |
| TC-PERM003-01 | PERM-003 | Normal | Đổi bot sau khi đã ghi khoá bàn giao — bộ lọc của bot A không được áp cho bot B | - 1 tài khoản quản lý 2 bot A và B<br>- Bot A có tag `TC38336_A` (3 bạn)<br>- Bot B có ≥ 10 bạn bè, **không** có tag nào tên `TC38336_A`<br>- localStorage đã xoá sạch trước khi bắt đầu | 1. Chọn bot A, vào タグ管理, bấm số người của tag `TC38336_A` — xác nhận friend list mở đúng 3 bạn.<br>2. Quay lại, bấm số người lần nữa để **ghi khoá bàn giao** nhưng **không mở** friend list (đóng tab vừa mở).<br>3. Dùng chức năng đổi bot sang **bot B**.<br>4. Mở màn 友だちリスト của bot B.<br>5. Quan sát 「検索結果：N人」 và vùng 「検索条件：」; mở DevTools > Application > Local Storage kiểm khoá bàn giao. | Bot A: tag `TC38336_A` = 3 bạn.<br>Bot B: 10 bạn bè. | Friend list của **bot B hiển thị đủ 10 bạn** của bot B, **không** áp điều kiện tag của bot A, **không** hiện 「検索条件：」 chứa tag lạ, **không** ra 0 người. Khoá bàn giao còn sót phải bị bỏ qua hoặc dọn khi đổi bot. | Chưa test | | STAGING | | | | Spec không ghi | Bổ sung theo review — lấp **GAP-3 / BLOCKER-3**, cover **D2 + T1**. Catalog `MAP-PERM-01`. localStorage thuộc **trình duyệt**, không thuộc bot → đây là lỗ hổng cách ly chưa ai kiểm |
| TC-PERM003-02 | PERM-003 | Abnormal | Bàn giao bộ lọc chứa `tag_id` của bot A, mở friend list ở bot B — không được lọc theo ID lạ | - Như TC-PERM003-01<br>- Ghi lại `tag_id` của tag `TC38336_A` (bot A) | 1. Ở bot A bấm số người của tag `TC38336_A` để ghi khoá bàn giao, đóng tab friend list vừa mở.<br>2. Đổi sang bot B.<br>3. Mở 友だちリスト của bot B.<br>4. Ghi lại số người hiển thị và nội dung 「検索条件：」.<br>5. Chạy thao tác gắn tag hàng loạt trên danh sách đang hiển thị.<br>6. Query DB đếm số bạn của bot B bị tác động. | `tag_id` của bot A không tồn tại ở bot B. | Danh sách bot B **không** lọc theo `tag_id` của bot A. Nếu hệ thống vẫn áp điều kiện → hoặc ra **0 người** (lọc theo ID không thuộc bot), hoặc tệ hơn là ra **sai nhóm** — **cả hai đều là bug, phải raise ticket**. Số bạn bot B bị tác động ở bước 6 phải khớp đúng danh sách đang hiển thị. | Chưa test | | STAGING | | | | Spec không ghi | Bổ sung theo review — lấp **GAP-3**, cover **D2 + F3**. Evidence: screenshot 「検索条件：」 + query DB bot B |
| TC-PERM003-03 | PERM-003 | Boundary | Staff chỉ có quyền trên bot B mở friend list khi trình duyệt còn khoá bàn giao của bot A | - Tài khoản **staff** chỉ được cấp quyền trên **bot B**<br>- Trình duyệt trước đó đã đăng nhập owner bot A và còn khoá bàn giao trong localStorage<br>- Không xoá localStorage giữa 2 phiên | 1. Đăng nhập owner bot A, bấm số người ở màn tag để ghi khoá bàn giao, đóng tab friend list.<br>2. Đăng xuất, đăng nhập tài khoản **staff của bot B** trên **cùng trình duyệt**.<br>3. Mở 友だちリスト của bot B.<br>4. Kiểm 「検索結果：N人」, 「検索条件：」 và localStorage. | Staff chỉ có quyền bot B.<br>Khoá bàn giao còn lại từ phiên owner bot A. | Friend list bot B hiển thị đúng phạm vi bạn bè bot B theo quyền của staff. **Không rò rỉ** điều kiện lọc hay dữ liệu của bot A. Khoá bàn giao của phiên trước bị bỏ qua/dọn. | Chưa test | | STAGING | | | | Spec không ghi | Bổ sung theo review — lấp **GAP-3**, liên kết `SEC-ISO-001` (cross-account cùng trình duyệt). Catalog `MAP-PERM-01` dòng "staff của 1 bot" |
| TC-ENV003-01 | ENV-003 | Normal | Production: lịch tự sinh chạy đúng nhóm đã lọc khi 3 job độc lập cùng hoạt động | - **Môi trường production** (`step.lme.jp`)<br>- Bot thật có ≥ 250 bạn bè<br>- Đã deploy `ai_fixbug_38336`<br>- Tránh tạo/xoá data thật ngoài phạm vi TC | 1. Trên production, đặt bộ lọc khớp 210 bạn ở màn 一斉配信, bấm số người.<br>2. Chọn 「条件に一致する全員」, chạy action gắn tag.<br>3. Xác nhận bản ghi lịch 【自動生成】友だち一括アクション được tạo.<br>4. Theo dõi log của **cả 3 job** (callback / broadcast / scenario) tới khi job hoàn tất.<br>5. Đếm số bạn bị tác động. | 210 bạn khớp bộ lọc / tổng 250. | Đúng **210** bạn bị tác động. Log **cả 3 job** không có tranh chấp, không xử lý trùng bản ghi. Số bản ghi vào = số xử lý thành công + số vào hàng đợi lỗi. | Chưa test | | PRODUCTION | | | | Spec không ghi | Bổ sung theo review — lấp **GAP-4 / BLOCKER-4**, cover **D1 + T6**. **RULE-08** + Catalog `ENV-JOB` (production tách 3 job, staging chỉ 1) |
| TC-ENV003-02 | ENV-003 | Abnormal | Production loadbalance 2 server: bàn giao bộ lọc hoạt động đúng trên từng router | - Môi trường production<br>- Xác định được **router id** của mỗi server | 1. Ghi lại router id đang phục vụ phiên hiện tại.<br>2. Chạy luồng cơ bản: bấm số người ở màn tag → friend list mở đúng nhóm đã lọc → chạy 1 thao tác hàng loạt.<br>3. Chuyển sang router còn lại, lặp lại bước 2.<br>4. So sánh kết quả 2 router. | Bộ lọc tag khớp 3 bạn. | **Cả 2 router** cho cùng kết quả: friend list đúng 3 bạn, thao tác hàng loạt tác động đúng 3 bạn. Không router nào rơi về toàn bộ bạn bè. | Chưa test | | PRODUCTION | | | | Spec không ghi | Bổ sung theo review — lấp **GAP-4**, Catalog `ENV-LB`. Evidence: ghi rõ **router id** trong kết quả từng lần chạy |
| TC-ENV003-03 | ENV-003 | Boundary | Production: user còn cache JS bản cũ chỉ F5 thường sau release — bộ lọc bàn giao có hiệu lực không | - Môi trường production<br>- Trình duyệt **đã mở màn friend list TRƯỚC release** để cache `modal_filter_v2.js` bản cũ<br>- Dev **KHÔNG tăng** `config('sns-line.version')` | 1. Trước release: mở 友だちリスト trên production để browser cache JS cũ.<br>2. Release bản sửa.<br>3. **Chỉ F5 thường** (KHÔNG Ctrl+F5).<br>4. DevTools > Network: kiểm `modal_filter_v2.js` — mã trả về, query version, có 404 không.<br>5. Bấm số người ở màn tag, quan sát friend list. | Bộ lọc tag khớp 3 bạn.<br>Tổng bạn bè bot ≥ 20. | Ghi nhận **thực tế**: nếu Network cho thấy JS vẫn là bản cũ (200 from disk cache, query version không đổi) và friend list hiện **toàn bộ** bạn bè thay vì 3 → **xác nhận rủi ro cache đã hiện thực hoá**, phải báo cáo và yêu cầu tăng version asset ở lần deploy chung trước khi thông báo KH. | Chưa test | | PRODUCTION | | | | Đã hỏi leader | Bổ sung theo review — lấp **GAP-4**, cover **BUG + T1**. Catalog `ENV-ASSET`. **Đây là TC quyết định fix có tới tay KH hay không** — Dev đã tự nêu rủi ro này ở mục "Rủi ro khi test" |
| TC-COMPATLEGACY001-02 | COMPAT-LEGACY-001 | Abnormal | Bản ghi CSV / broadcast / lịch hành động tạo TRƯỚC version-up — bấm số người vẫn mở đúng danh sách đã lọc | - Có sẵn bản ghi cũ trong DB: 1 bản ghi CSV, 1 broadcast bản nháp, 1 lịch hành động **tạo từ trước lần version-up gần nhất**<br>- Nếu không có sẵn, xin Dev sample từ production | 1. Vào CSV管理, mở bản ghi CSV cũ, bấm số người.<br>2. Ghi lại số người ở friend list và so với số hiển thị trên màn CSV.<br>3. Lặp với broadcast bản nháp cũ.<br>4. Lặp với lịch hành động cũ.<br>5. Với mỗi bản ghi, mở → sửa → **lưu lại** rồi bấm số người lần nữa. | 3 bản ghi tạo trước version-up, mỗi bản ghi có điều kiện lọc đã lưu. | Cả 3 bản ghi cũ đều mở friend list đúng số người khớp với số hiển thị ở màn nguồn. Sau khi sửa và lưu lại, kết quả **không đổi**. Không bản ghi nào rơi về toàn bộ bạn bè, không lỗi định dạng điều kiện. | Chưa test | | STAGING | | | | Spec không ghi | Bổ sung theo review — lấp **GAP-5**, cover **F9 + F10 + T4**. **RULE-09**. Đây là chỗ Dev tự cảnh báo: nhánh nạp bộ lọc *"lần đầu thực sự chạy sau nhiều năm bị chặn"* → định dạng dữ liệu bàn giao cũ có thể đã lỗi thời |
| TC-BULK001-04 | BULK-001 | Abnormal | Thao tác hàng loạt khi bộ lọc bàn giao khớp 0 người — không được rơi về toàn bộ bạn bè | - Bot có ≥ 20 bạn bè<br>- Tag `TC38336_ZERO` **chưa gắn cho ai** | 1. Vào タグ管理, bấm số người của tag `TC38336_ZERO`.<br>2. Xác nhận friend list hiện 「検索結果：0人」, bảng rỗng.<br>3. Thử thao tác gắn tag hàng loạt trên danh sách rỗng (nếu UI cho phép bấm).<br>4. Query DB đếm số bạn bị tác động. | Tag `TC38336_ZERO` = 0 bạn / tổng ≥ 20 bạn. | Danh sách hiện **0 người**. Nút thao tác hàng loạt **không bấm được** (hoặc bấm thì báo lỗi rõ ràng), và **0** bạn bị tác động trong DB. Tuyệt đối không tác động lên 20 bạn. | Chưa test | | STAGING | | | | Spec không ghi | Bổ sung theo review — lấp **RULE-01** cho `BULK-001` (Cao, đang thiếu Abnormal), cover **F4**. **Liên quan trực tiếp TC-FUNC004-03 đang FAIL (#40060)** — cùng biên 0 người |
| TC-BULK001-05 | BULK-001 | Boundary | Thao tác hàng loạt tại đúng biên 200 và 201 người sau bàn giao bộ lọc | - Bot có ≥ 250 bạn bè<br>- Tag `TC38336_200` gắn đúng **200** bạn<br>- Tag `TC38336_201` gắn đúng **201** bạn | 1. Bấm số người của tag `TC38336_200`, chạy action gắn tag `TC38336_DONE`.<br>2. Ghi nhận: có hiện lựa chọn 「条件に一致する全員」 không, có tạo lịch tự sinh không.<br>3. Đếm số bạn có `TC38336_DONE` (UI + DB).<br>4. Lặp toàn bộ với tag `TC38336_201`. | 200 bạn / 201 bạn / tổng 250 bạn.<br>Phép tính tay: mốc 200 → chạy trực tiếp; 201 → tạo lịch tự sinh. | Với **200**: chạy trực tiếp, không tạo lịch tự sinh, đúng **200** bạn bị tác động. Với **201**: hiện thông điệp ngưỡng 200, tạo bản ghi 【自動生成】友だち一括アクション **kèm đúng điều kiện lọc**, job chạy tác động đúng **201** bạn — không phải 250. | Chưa test | | STAGING | | | | Spec ghi rõ | Bổ sung theo review — lấp **RULE-01** cho `BULK-001` (đang thiếu Boundary), cover **F5 + D1**. Evidence: đếm DB + ảnh bản ghi lịch tự sinh kèm điều kiện |
| TC-MSG001-03 | MSG-001 | Normal | Gửi mẫu tin hàng loạt sau bàn giao bộ lọc — xác nhận NHẬN THẬT trên LINE app (iOS + Android) | - Bot Standard còn quota tin nhắn<br>- Tag `TC38336_LINE` gắn cho đúng 3 bạn, gồm **1 máy iOS thật** và **1 máy Android thật** đã kết bạn<br>- 1 bạn ngoài nhóm lọc cũng là máy thật để đối chứng | 1. Vào タグ管理, bấm số người của tag `TC38336_LINE`.<br>2. Ở friend list (3 bạn), chạy thao tác gửi mẫu tin `TPL_TC38336`.<br>3. Mở **LINE app trên iOS thật** của bạn trong nhóm — kiểm tin đã nhận.<br>4. Mở **LINE app trên Android thật** của bạn trong nhóm — kiểm tin đã nhận.<br>5. Mở LINE app của bạn **ngoài** nhóm lọc — xác nhận KHÔNG nhận tin.<br>6. Đối chiếu nội dung nhận thật với preview ở màn admin. | Tag `TC38336_LINE` = 3 bạn.<br>Tổng bạn bè ≥ 20.<br>Phép tính tay: đúng 3 người nhận, ≥ 17 người không nhận. | Đúng **3** bạn nhận tin trên LINE app thật; bạn ngoài nhóm **không nhận**. Nội dung trên LINE app (emoji, xuống dòng, ảnh) **khớp preview admin** trên **cả iOS và Android**. | Chưa test | | STAGING | | | | Spec ghi rõ | Bổ sung theo review — lấp **MAJOR RULE-06**, cover **F4 + T1**. `MSG-001` bắt buộc *"xác nhận nhận thật trên LINE app, không chỉ nhìn số đếm"*. Evidence: **screenshot LINE app thật iOS VÀ Android** |
| TC-DATACOUNT001-01 | DATA-COUNT-001 | Normal | Số người sau bàn giao bộ lọc khớp trên đủ 4 nguồn: màn nguồn / friend list / CSV export / API | - Tag `TC38336_COUNT` gắn cho đúng 7 bạn<br>- Trong 7 bạn có **1 bạn đã block bot**<br>- Bot có ≥ 30 bạn bè | 1. Ghi lại số người hiển thị ở màn タグ管理 cho tag `TC38336_COUNT`.<br>2. Bấm số người → ghi 「検索結果：N人」 ở friend list.<br>3. Từ friend list đã lọc, export CSV → đếm số dòng dữ liệu.<br>4. Gọi API danh sách bạn bè với cùng điều kiện lọc → đếm số bản ghi.<br>5. Lập bảng đối chiếu 4 số + ghi rõ cách xử lý bạn đã block. | Tag `TC38336_COUNT` = 7 bạn (1 bạn đã block).<br>Phép tính tay: 7 nếu tính cả bạn block, 6 nếu loại trừ. | **Cả 4 nguồn cho cùng một số.** Cách xử lý bạn đã block phải **nhất quán** giữa 4 nguồn (cùng tính hoặc cùng loại trừ) và khớp spec. Lệch bất kỳ nguồn nào → raise ticket. | Chưa test | | STAGING | | | | Spec không ghi | Bổ sung theo review — lấp **MAJOR `DATA-COUNT-001`**, cover **F2 + F7 + T1**. Quan điểm này là **lỗi lặp nhiều nhất lịch sử bug (12 ticket Closed)**. Evidence: bảng đối chiếu 4 nguồn + phép tính tay |
| TC-DEPLOYLIVE001-01 | DEPLOY-LIVE-001 | Abnormal | Tab friend list mở sẵn TRƯỚC release — thao tác tiếp mà không reload | - Tab đang mở màn 友だちリスト với bộ lọc bàn giao đã áp, chạy JS **bản cũ**<br>- Release diễn ra **không bật maintain** | 1. Trước release: mở friend list qua bàn giao bộ lọc tag (3 bạn), **giữ nguyên tab**.<br>2. Release `ai_fixbug_38336`.<br>3. **Không reload**, thao tác tiếp trên tab cũ: chuyển trang, rồi chạy thao tác gắn tag hàng loạt.<br>4. Query DB đếm số bạn bị tác động.<br>5. Kiểm log request xem payload có bị lỗi định dạng không. | Bộ lọc tag khớp 3 bạn / tổng ≥ 20 bạn. | Thao tác hoặc **hoàn tất đúng 3 bạn**, hoặc **báo lỗi rõ ràng** yêu cầu tải lại trang. **Tuyệt đối không**: exception 500, lưu nửa vời, hay tác động lên toàn bộ 20 bạn. | Chưa test | | STAGING | | | | Spec không ghi | Bổ sung theo review — lấp **GAP-6**, cover **BUG + F3**. Khác `DEPLOY-ASSET-001`: đây là **client cũ gọi server mới**. Evidence: screenshot tab cũ + log request + query DB |
| TC-DATAREF001-01 | DATA-REF-001 | Abnormal | Tag trong điều kiện bàn giao bị XÓA trước khi friend list tiêu thụ khoá | - Tag `TC38336_DEL` gắn cho 3 bạn<br>- Bot có ≥ 20 bạn bè<br>- Mở được 2 tab admin song song | 1. Tab 1: vào タグ管理, bấm số người của tag `TC38336_DEL` để ghi khoá bàn giao, **đóng tab friend list vừa mở** (chưa tiêu thụ xong).<br>2. Tab 2: **xóa** tag `TC38336_DEL`.<br>3. Tab 1: mở lại 友だちリスト.<br>4. Quan sát 「検索結果：N人」, 「検索条件：」 và thông báo lỗi (nếu có).<br>5. Thử chạy thao tác hàng loạt trên danh sách đang hiển thị, query DB đếm số bạn bị tác động. | Tag `TC38336_DEL` = 3 bạn, bị xóa giữa chừng.<br>Tổng bạn bè ≥ 20. | Màn **không hỏng**: hoặc hiện 0 người kèm thông báo điều kiện không còn hợp lệ, hoặc trở về danh sách mặc định kèm cảnh báo rõ ràng. **Tuyệt đối không** âm thầm hiện toàn bộ 20 bạn rồi để thao tác hàng loạt áp cho tất cả. | Chưa test | | STAGING | | | | Spec không ghi | Bổ sung theo review — lấp **GAP-10**, cover **D2 + T3**. Catalog `MAP-TAG-05`: *tag bị xóa khi đang được điều kiện tham chiếu → đối tượng gửi không được sai* |
| TC-LIST001-02 | LIST-001 | Normal | Danh sách tin gửi hàng loạt — tab 配信予約: bấm cột 配信数 mở đúng danh sách đã lọc | - Bot có ≥ 20 bạn bè<br>- Tag `TC38336_R` gắn cho đúng 4 bạn<br>- 1 broadcast **đã đặt lịch** (status `wait_to_send`) với điều kiện lọc tag `TC38336_R`<br>- localStorage đã xoá sạch | 1. Mở màn 一斉配信, chuyển sang tab **配信予約**.<br>2. Tìm bản ghi đã chuẩn bị, ghi lại giá trị cột **配信数** và cột 配信先絞込み.<br>3. Bấm vào con số ở cột 配信数.<br>4. Ở tab friend list mở ra, đối chiếu 「検索結果：」, vùng 「検索条件：」 và danh sách tên. | Tag `TC38336_R` = 4 bạn / tổng ≥ 20 bạn.<br>Phép tính tay: 配信数 = 4 → 「検索結果：4人」. | Friend list hiển thị **đúng 4 bạn** có tag `TC38336_R`; 「検索結果：4人」 **khớp cột 配信数** ở tab 配信予約; 「検索条件：」 nêu đúng điều kiện tag. Không rơi về toàn bộ 20 bạn. | Chưa test |  | STAGING |  |  |  | Spec không ghi | Bổ sung theo review — lấp **GAP-11 / BLOCKER-8**, cover **F10 + T2**. Tách riêng khỏi tab 下書き vì TC-REGSHARED001-02 dùng chữ "hoặc" nên chỉ chạy 1 trong 2. Evidence: screenshot tab 配信予約 + screenshot friend list |
| TC-LIST001-03 | LIST-001 | Normal | Danh sách tin gửi hàng loạt — tab 下書き: bấm cột 配信数 mở đúng danh sách đã lọc | - Như TC-LIST001-02<br>- 1 broadcast **bản nháp** (status `draft`) với điều kiện lọc tag `TC38336_R` | 1. Mở màn 一斉配信, chuyển sang tab **下書き**.<br>2. Tìm bản ghi nháp, ghi lại cột **配信数**.<br>3. Bấm vào con số ở cột 配信数.<br>4. Đối chiếu 「検索結果：」, 「検索条件：」 và danh sách tên ở friend list. | Tag `TC38336_R` = 4 bạn / tổng ≥ 20 bạn. | Friend list hiển thị **đúng 4 bạn**; 「検索結果：4人」 khớp cột 配信数 ở tab 下書き; 「検索条件：」 đúng điều kiện tag. | Chưa test |  | STAGING |  |  |  | Spec không ghi | Bổ sung theo review — lấp **GAP-11 / BLOCKER-8**, cover **F10 + T2**. Evidence: screenshot tab 下書き + friend list |
| TC-LIST001-04 | LIST-001 | Abnormal | Danh sách tin gửi hàng loạt — tab 配信履歴 (đã gửi): bấm cột 配信数 của broadcast đã gửi | - Như TC-LIST001-02<br>- 1 broadcast **đã gửi xong** (status `delivered`) với điều kiện lọc tag `TC38336_R` tại thời điểm gửi<br>- Sau khi gửi, **thêm 2 bạn mới** vào tag `TC38336_R` để số hiện tại khác số lúc gửi | 1. Mở màn 一斉配信, chuyển sang tab **配信履歴**.<br>2. Tìm bản ghi đã gửi, ghi lại cột **配信数** và cột 配信先絞込み.<br>3. Xác nhận con số đó có **bấm được** không. Nếu KHÔNG phải link → chụp màn hình, ghi kết quả `N/A` kèm lý do, **không tự dựng request thay thế**.<br>4. Nếu bấm được: mở friend list và đối chiếu 「検索結果：」, 「検索条件：」, danh sách tên.<br>5. So sánh 3 số: 配信数 hiển thị / số bạn khớp tag **hiện tại** (6) / số thực nhận lúc gửi (4). | Lúc gửi: tag `TC38336_R` = 4 bạn.<br>Sau khi gửi: tag = 6 bạn.<br>Tổng bạn bè ≥ 20. | Ghi nhận rõ **配信数 ở tab 配信履歴 đang là số nào**: `send_count` (4 — số thực đã gửi) hay `filter_number` (số khớp filter). Nếu bấm được, friend list phải hiển thị nhóm khớp **điều kiện đã lưu**, **tuyệt đối không** rơi về toàn bộ 20 bạn. Nếu số hiển thị và danh sách mở ra **mâu thuẫn nhau** → raise ticket kèm cả 3 số. | Chưa test |  | STAGING |  |  |  | Đã hỏi leader | Bổ sung theo review — lấp **GAP-11 / BLOCKER-8**, cover **F10 + T2**. `db-mapping.md` dòng 184 ghi 配信数 map `send_count / filter_number` → **phải xác định rõ**. Broadcast `delivered` có filter **read-only** (`preview_filter_broadcast="全員"`). Evidence: screenshot 3 số + friend list |
| TC-FUNC001-08 | FUNC-001 | Normal | modal.orderBy: màn SỬA broadcast — bấm 配信数 mở đúng danh sách, filter cascade sang broadcast con | - Bot có ≥ 20 bạn bè<br>- Tag `TC38336_R` = 4 bạn, tag `TC38336_S` = 2 bạn<br>- 1 broadcast cha đã lưu (status `draft`) có **broadcast con** (multi-schedule, `parent_id`) | 1. Mở màn **sửa** broadcast đã lưu (không phải màn tạo).<br>2. Bấm 「絞り込み」, **đổi** điều kiện từ tag `TC38336_R` sang tag `TC38336_S`, áp dụng.<br>3. Ghi lại 配信数 hiển thị dạng 「N人(予定)」.<br>4. Bấm vào số người → đối chiếu 「検索結果：」, 「検索条件：」 ở friend list.<br>5. Lưu broadcast, mở **broadcast con** và bấm 配信数 của nó. | Tag `TC38336_R` = 4 bạn → đổi sang tag `TC38336_S` = 2 bạn.<br>Phép tính tay: sau khi đổi, 配信数 = 2. | Sau khi đổi điều kiện, 配信数 = **2** và friend list mở ra đúng **2 bạn** của tag `TC38336_S` (không còn 4 bạn của điều kiện cũ). Broadcast **con** sau khi lưu cũng bấm ra đúng **2 bạn** — filter đã cascade đúng. | Chưa test |  | STAGING |  |  |  | Spec không ghi | Bổ sung theo review — lấp **GAP-13 / BLOCKER-8**, cover **F1 + F10 + T2**. TC-FUNC001-02 chỉ mở màn **tạo**. Logic cascade: copy filter của cha sang mỗi broadcast con. Evidence: screenshot trước/sau khi đổi điều kiện + friend list của cả cha và con |
| TC-DATAREF001-02 | DATA-REF-001 | Abnormal | COPY broadcast: filter được clone — bấm 配信数 ở bản copy mở đúng danh sách, không dính bản gốc | - Bot có ≥ 20 bạn bè<br>- Tag `TC38336_R` = 4 bạn, tag `TC38336_S` = 2 bạn<br>- 1 broadcast gốc đã lưu với điều kiện lọc tag `TC38336_R` | 1. Ở màn 一斉配信, **sao chép** broadcast gốc (EP-16 `/ajax/copy-broadcast-v2`).<br>2. Xác nhận bản copy xuất hiện ở tab 下書き với status `draft`.<br>3. Ghi lại cột 配信数 của **bản copy**, bấm vào → đối chiếu friend list.<br>4. Mở bản copy, **đổi** điều kiện sang tag `TC38336_S`, lưu.<br>5. Quay lại **bản gốc**, bấm 配信数 của bản gốc → đối chiếu friend list. | Bản gốc: tag `TC38336_R` = 4 bạn.<br>Bản copy sau khi sửa: tag `TC38336_S` = 2 bạn.<br>Tổng ≥ 20 bạn. | Bản copy giữ nguyên điều kiện gốc: 配信数 = **4**, friend list mở ra đúng **4** bạn (**không** rơi về toàn bộ 20, **không** rỗng). Sau khi sửa bản copy thành tag `TC38336_S`, **bản gốc vẫn = 4 bạn** — sửa bản copy không đụng bản gốc. | Chưa test |  | STAGING |  |  |  | Spec không ghi | Bổ sung theo review — lấp **GAP-12 / BLOCKER-8**, cover **F10 + T2**. Quan điểm **`MSG-001` nêu đích danh rủi ro "filter bị mất sau copy/sort"**; spec ghi khi copy thì broadcast, templates, actions, **filters**, child broadcasts đều được clone (`FilterV2::cloneFilters()`). Evidence: screenshot friend list của cả bản gốc và bản copy |
| TC-REGSHARED001-14 | REG-SHARED-001 | Normal | サロン予約 — コースの絞り込み表示: bấm số người mở đúng danh sách đã lọc (`calendar_salon_courses.filter_number`) | - Salon đang bật `use_course = true`, có ≥ 1 コース<br>- Bot có ≥ 20 bạn bè<br>- Tag `TC38336_SC` gắn cho đúng 3 bạn<br>- localStorage đã xoá sạch | 1. Mở サロン予約 > chọn salon > màn cài đặt **コース** > sửa 1 コース.<br>2. Tìm mục 「絞り込み表示」 của コース. **Nếu mục này không tồn tại** → chụp màn hình, ghi `N/A` + báo Leader, dừng TC.<br>3. Mở modal lọc, đặt điều kiện tag `TC38336_SC`, áp dụng.<br>4. Ghi lại số người hiển thị.<br>5. Xác nhận số đó **bấm được**; nếu không → ghi `N/A` kèm screenshot.<br>6. Bấm số người → đối chiếu 「検索結果：」, 「検索条件：」 và danh sách tên ở friend list. | Tag `TC38336_SC` = 3 bạn / tổng ≥ 20 bạn.<br>Phép tính tay: số người = 3 → 「検索結果：3人」. | Friend list hiển thị **đúng 3 bạn** có tag `TC38336_SC`; 「検索結果：3人」 khớp số người ở màn cài đặt コース; 「検索条件：」 nêu đúng điều kiện. **Không** rơi về toàn bộ 20 bạn. | Chưa test |  | STAGING |  |  |  | Spec không ghi | Bổ sung theo review (**Leader chỉ định**) — lấp **GAP-14**, cover **F1**. `parent_type=calendar-salon-course-setting-status-send-after-booking` → cột `filter_id` + `filter_number`, **khác** lesson (`filter_id_send_after_booking`) nên là **nhánh code riêng**. Evidence: screenshot màn コース + friend list |
| TC-REGSHARED001-15 | REG-SHARED-001 | Normal | サロン予約 — スタッフ詳細の絞り込み表示: bấm số người mở đúng danh sách đã lọc (`calendar_salon_staffs.filter_number`) | - Salon đang bật `use_staff = true`, có ≥ 1 スタッフ<br>- Bot có ≥ 20 bạn bè<br>- Tag `TC38336_SS` gắn cho đúng 5 bạn<br>- localStorage đã xoá sạch | 1. Mở サロン予約 > chọn salon > màn **スタッフ** > mở **スタッフ詳細** của 1 nhân viên.<br>2. Tìm mục 「絞り込み表示」. **Nếu không tồn tại** → chụp màn hình, ghi `N/A` + báo Leader, dừng TC.<br>3. Mở modal lọc, đặt điều kiện tag `TC38336_SS`, áp dụng.<br>4. Ghi lại số người hiển thị.<br>5. Bấm số người → đối chiếu 「検索結果：」, 「検索条件：」 và danh sách tên.<br>6. Ghi lại giá trị `is_all_course` / danh sách コース của nhân viên này để đối chiếu về sau. | Tag `TC38336_SS` = 5 bạn / tổng ≥ 20 bạn.<br>Phép tính tay: số người = 5 → 「検索結果：5人」. | Friend list hiển thị **đúng 5 bạn** có tag `TC38336_SS`; 「検索結果：5人」 khớp số người ở màn スタッフ詳細; 「検索条件：」 đúng điều kiện. **Không** rơi về toàn bộ 20 bạn. | Chưa test |  | STAGING |  |  |  | Spec không ghi | Bổ sung theo review (**Leader chỉ định**) — lấp **GAP-15**, cover **F1**. `parent_type=calendar-salon-staff-setting-status-send-after-booking` → `calendar_salon_staffs.filter_id` + `filter_number`. Evidence: screenshot スタッフ詳細 + friend list |
| TC-REGSHARED001-16 | REG-SHARED-001 | Abnormal | サロン予約 — スタッフ詳細の絞り込み表示 với điều kiện khớp 0 người | - Như TC-REGSHARED001-15<br>- Tag `TC38336_SS_EMPTY` **chưa gắn cho ai** | 1. Mở スタッフ詳細 của 1 nhân viên, vào 「絞り込み表示」.<br>2. Đặt điều kiện tag `TC38336_SS_EMPTY`, áp dụng.<br>3. Ghi lại số người hiển thị (kỳ vọng 0).<br>4. Nếu số 0 bấm được → mở friend list và quan sát 「検索結果：」 + bảng.<br>5. Nếu giao diện **không cho bấm khi số người = 0** → ghi `N/A` kèm lý do và screenshot. | Tag `TC38336_SS_EMPTY` = 0 bạn / tổng ≥ 20 bạn. | Số người hiển thị = **0**. Nếu bấm được, friend list phải ra 「検索結果：0人」 với bảng rỗng và 「検索条件：」 nêu tag `TC38336_SS_EMPTY` — **tuyệt đối không** hiện toàn bộ 20 bạn. | Chưa test |  | STAGING |  |  |  | Spec không ghi | Bổ sung theo review — lấp **GAP-15**, cover **F1**. Biên 0 người **chính là chỗ TC-FUNC004-03 đang FAIL (#40060)** ở màn tag → phải kiểm cả ở nhánh salon staff |
| TC-REGSHARED001-17 | REG-SHARED-001 | Normal | レッスン予約 — コースの絞り込み表示: bấm số người mở đúng danh sách đã lọc | - 1 lesson calendar đang bật `enable_use_calendar`, có ≥ 1 コース<br>- Bot có ≥ 20 bạn bè<br>- Tag `TC38336_LC` gắn cho đúng 4 bạn<br>- localStorage đã xoá sạch | 1. Mở レッスン予約 > chọn calendar > màn cài đặt **コース** > sửa 1 コース.<br>2. Tìm mục 「絞り込み表示」 của コース — **lưu ý phân biệt** với mục 「対象人数」 của phần *tin nhắn gửi sau khi đặt lịch* (đã có TC-REGSHARED001-11 ở file 04). **Nếu mục 「絞り込み表示」 không tồn tại** → chụp màn hình, ghi `N/A` + báo Leader.<br>3. Mở modal lọc, đặt điều kiện tag `TC38336_LC`, áp dụng.<br>4. Ghi lại số người hiển thị.<br>5. Bấm số người → đối chiếu 「検索結果：」, 「検索条件：」 và danh sách tên ở friend list. | Tag `TC38336_LC` = 4 bạn / tổng ≥ 20 bạn.<br>Phép tính tay: số người = 4 → 「検索結果：4人」. | Friend list hiển thị **đúng 4 bạn** có tag `TC38336_LC`; 「検索結果：4人」 khớp số người ở mục 「絞り込み表示」 của コース; 「検索条件：」 nêu đúng điều kiện. **Không** rơi về toàn bộ 20 bạn. | Chưa test |  | STAGING |  |  |  | Spec không ghi | Bổ sung theo review (**Leader chỉ định**) — lấp **GAP-18**, cover **F1**. ⚠️ Spec `friend-filter` mới ghi `calendar_courses.filter_id_send_after_booking` (mục 対象人数 của tin sau đặt lịch) — **chưa ghi** `parent_type`/cột cho 「絞り込み表示」 của コース → **hỏi Dev xác nhận** trước khi chạy. Đây là **cặp đối xứng** với TC-REGSHARED001-14 (salon course). Evidence: screenshot màn コース + friend list |
| TC-REGSHARED001-18 | REG-SHARED-001 | Normal | レッスン予約 — cài đặt 予約ページの非表示: bấm số người mở đúng danh sách đã lọc | - 1 lesson calendar đang bật `enable_use_calendar`<br>- Bot có ≥ 20 bạn bè<br>- Tag `TC38336_LH` gắn cho đúng 3 bạn<br>- localStorage đã xoá sạch | 1. Mở レッスン予約 > chọn calendar > phần cài đặt **「予約ページの非表示」**.<br>2. Mở modal lọc chọn đối tượng bị ẩn trang đặt lịch. **Nếu mục này không tồn tại** → chụp màn hình, ghi `N/A` + báo Leader.<br>3. Đặt điều kiện tag `TC38336_LH`, áp dụng.<br>4. Ghi lại số người hiển thị.<br>5. Bấm số người → đối chiếu 「検索結果：」, 「検索条件：」 và danh sách tên ở friend list. | Tag `TC38336_LH` = 3 bạn / tổng ≥ 20 bạn.<br>Phép tính tay: số người = 3 → 「検索結果：3人」. | Friend list hiển thị **đúng 3 bạn** có tag `TC38336_LH`; 「検索結果：3人」 khớp số người ở màn cài đặt 「予約ページの非表示」; 「検索条件：」 đúng điều kiện. **Không** rơi về toàn bộ 20 bạn. | Chưa test |  | STAGING |  |  |  | Spec không ghi | Bổ sung theo review (**Leader chỉ định**) — lấp **GAP-17**, cover **F1**. Khớp `parent_type=calendar-setting-show-booking-form` → `calendar_managements.filter_number_show_booking` + `filter_id_show_booking`. Evidence: screenshot màn cài đặt + friend list |
| TC-REGSHARED001-19 | REG-SHARED-001 | Normal | サロン予約 — cài đặt 予約ページの非表示: bấm số người mở đúng danh sách đã lọc | - 1 salon đang bật `enable_use_calendar`<br>- Bot có ≥ 20 bạn bè<br>- Tag `TC38336_SH` gắn cho đúng 2 bạn<br>- localStorage đã xoá sạch | 1. Mở サロン予約 > chọn salon > phần cài đặt **「予約ページの非表示」**.<br>2. Mở modal lọc chọn đối tượng bị ẩn trang đặt lịch. **Nếu mục này không tồn tại** → chụp màn hình, ghi `N/A` + báo Leader.<br>3. Đặt điều kiện tag `TC38336_SH`, áp dụng.<br>4. Ghi lại số người hiển thị.<br>5. Bấm số người → đối chiếu 「検索結果：」, 「検索条件：」 và danh sách tên ở friend list.<br>6. Ghi lại `parent_type` quan sát được (qua DevTools > Network, request lưu filter) để phân định với TC-REGSHARED001-12. | Tag `TC38336_SH` = 2 bạn / tổng ≥ 20 bạn.<br>Phép tính tay: số người = 2 → 「検索結果：2人」. | Friend list hiển thị **đúng 2 bạn** có tag `TC38336_SH`; 「検索結果：2人」 khớp số người ở màn cài đặt 「予約ページの非表示」; 「検索条件：」 đúng điều kiện. **Không** rơi về toàn bộ 20 bạn. | Chưa test |  | STAGING |  |  |  | Spec không ghi | Bổ sung theo review (**Leader chỉ định**) — lấp **GAP-19**, cover **F1**. Ứng viên `parent_type=filter-calendar-salon-booking` → `calendar_salons.filter_calendar_salon_ids` + `number_filter_salon`; bước 6 giúp **gỡ luôn mâu thuẫn map của TC-REGSHARED001-12**. Evidence: screenshot màn cài đặt + friend list + ảnh request lưu filter |

---

## 6. Spec update needed

- [ ] Không cần update spec
- [x] **Cần update spec** — chi tiết:
  - **Section**: `LME-SYSTEM-SPEC` — FA-013 Friend List (+ tham chiếu chéo FA-004 Rich Menu, FA-008 Broadcast, FA-012 Tag, FA-014 CSV, FA-016 Action Schedule).
  - **Nội dung cần update**:
    1. **Chưa có spec cho cơ chế "bấm số người → mở friend list đã lọc"** — cả 49 TC đều để trống `Trạng thái đánh giá spec`, và Dev tự mô tả hành vi sau fix là *"hành vi đúng theo thiết kế"* mà không dẫn được mục spec nào. Cần ghi rõ: màn nguồn nào bàn giao bộ lọc, bàn giao qua **localStorage** hay **URL param**, khoá dùng chung giữa những màn nào, và **quy tắc tiêu thụ một lần**.
    2. **Ghi rõ hành vi khi không có / có nhiều bộ lọc bàn giao**: không bàn giao → danh sách mặc định; hai màn ghi chung 1 khoá → lần bấm sau ghi đè; vừa có khoá tồn đọng vừa có URL param → **kết hợp (phần giao)**, theo REQ-002/REQ-011 của Studio.
    3. **Ghi rõ hành vi ở biên 0 người** — đây đúng là chỗ TC-FUNC004-03 đang FAIL (#40060): tag chưa gắn cho ai thì phải ra `0人`, **không** được hiện toàn bộ bạn bè.
    4. **Ghi rõ phạm vi cách ly theo bot** của khoá bàn giao trong localStorage (liên quan BLOCKER-3 / `PERM-003`).
  - **Người chịu trách nhiệm update**: `<PM / Leader điền>`

---

## 7. Checklist đã chạy

- [x] **A. Coverage** — A.1 ⚠️ (TC tái hiện bug gốc đang `skip`) · A.2 ⚠️ (F7 GAP, F8 thiếu nhánh cũ) · A.3 ⚠️ (D1 không verify DB, không test bản ghi tạo trước fix) · A.4 ✓ (T1–T10 đều có TC) · A.5 ⚠️ (1 ORPHAN) · A.6 ✓ (fix-shape §3.5)
- [x] **B. Chất lượng từng TC** — B.1 ✓ (precondition + expected đo lường được, có phép tính tay) · B.2 ✓ · B.3 ⚠️ (8 cặp trùng gây nhập nhằng) · B.4 ✓ (data test đặt tên theo ticket `TC38336_*`, không dùng `test`/`abc`)
- [x] **C. Chất lượng bộ TC** — tỷ lệ Normal/Abnormal/Boundary = **28/13/8** (57/27/16%) — lệch về Normal so với gợi ý 40/35/25, hợp lý một phần vì task là triển khai ngang nhiều màn, nhưng `BULK-001` thiếu hẳn Abnormal + Boundary (xem §4.2). ⚠️ Phân bố quan điểm dồn: `REG-SHARED-001` chiếm 13/49 TC. ⚠️ Không có TC phân quyền (role/staff), không có TC responsive/đa thiết bị.
- [x] **D. Spec alignment** — ⚠️ không có `02-spec-reference.md`; 49/49 TC trống `Trạng thái đánh giá spec` → xem §6.
- [x] **E. Hành chính** — ⚠️ TC No. do `/new-task` sinh lại (không phải ID gốc Studio); ⚠️ "Tester viết TCs" là **AI**, chưa có human ký tên; ✓ file lưu đúng folder review.
- [x] **F. Base quan điểm test LME**
  - [x] F.1 Quan điểm (tầng 1) — bảng dưới
  - [x] F.2 Catalog (tầng 2) — đã tra **C.3 Tag** (`MAP-TAG-05`) · **C.10 Phân quyền** (`MAP-PERM-01/02/03`) · **D** (`ENV-JOB`, `ENV-LB`, `ENV-ASSET`) · **D2** (`JOB-02`, `JOB-04`). Không áp dụng: A (fix không thêm ô nhập), E (không chạm media).
  - [x] F.3 RULE quy trình — RULE-01 ✗ (`BULK-001`) · RULE-02 ✗ (evidence trống) · RULE-03 n/a (Studio không có cột ×) · RULE-06 ✗ (`MSG-001`) · RULE-07 ✗ (không verify DB) · RULE-08 ✗ (0 TC production) · RULE-09 ✗ (không test nhánh cũ) · RULE-11 ✗ (86% TC không có kết luận) · RULE-12 ✓ (Dev có cung cấp danh sách vùng ảnh hưởng)

### F.1 — Bảng quan điểm đối chiếu

| Mã quan điểm | Ưu tiên | Trigger khớp task? | TC cover (suy luận) | Kết luận |
|---|---|---|---|---|
| `FUNC-001` | **Cao** | ◯ luôn bắt buộc | TC-FUNC001-01→07 (7 TC) | **OK** — nhưng 5/7 đang `skip` |
| `FUNC-004` | **Cao** | ◯ biên 200 người, biên 0 người | TC-FUNC004-01→05 (5 TC, đều Boundary) | **RISK** — 1 TC đang **FAIL** (#40060) |
| `FUNC-SEQ-001` | Trung bình | ◯ thao tác liên tiếp + reload trên cùng danh sách | TC-FUNCSEQ001-01 | OK |
| `CONC-003` | Trung bình → **Cao** (màn có phân trang + filter) | ◯ | TC-CONC003-01 | **RISK** — 1 TC, chưa test đa tab (xem GAP-9) |
| `DATA-001` | **Cao** | ◯ dữ liệu lọc phản ánh ở nhiều màn | Gián tiếp qua 12 TC màn nguồn | OK |
| `DATA-COUNT-001` | **Cao** | ◯ **BẮT BUỘC** — màn có 「検索結果：N人」 | Đối chiếu 2/4 nguồn | **RISK** → [MAJOR] |
| `DATA-DB-001` | **Cao** | ◯ **BẮT BUỘC** — có UPDATE hàng loạt | — | **GAP** → **[BLOCKER]** |
| `DATA-CACHE-001` | Trung bình → **Cao** | ◯ release đổi JS | TC-DEPLOYASSET001-01/02 | RISK — cả 2 đang `skip` |
| `DATA-REF-001` | **Cao** | ◯ tag trong điều kiện có thể bị xóa/đổi tên | — | **GAP** → [MAJOR] |
| `DATA-ID-001` | Trung bình → Cao | ◯ (nhẹ) màn chọn đối tượng để thao tác | — | GAP → [NIT] |
| `LIST-001` | Trung bình | ◯ **BẮT BUỘC** — màn danh sách có filter/pagination | TC-LIST001-01 (1/4 góc) | **RISK** → [MAJOR] |
| `BULK-001` | **Cao** | ◯ **BẮT BUỘC** — filter + thao tác hàng loạt | TC-BULK001-01/02/03 (3 TC, **đều Normal**) | **RISK** → [MAJOR] **RULE-01** |
| `MSG-001` | **Cao** | ◯ **BẮT BUỘC** — gửi tin có điều kiện lọc | TC-MSG001-01/02 | **RISK** → [MAJOR] **RULE-06** (không verify LINE app thật) |
| `MSG-004` | **Cao** | **×** — nội dung tin **không** bị bản sửa chạm, chỉ tập người nhận đổi | — | × có lý do (phần "nhận thật trên LINE" đã gộp vào `MSG-001`) |
| `STATE-001` | **Cao** | ◯ bàn giao + URL param kết hợp | TC-STATE001-01 | **RISK** — TC **chưa từng chạy** |
| `REG-SHARED-001` | **Cao** | ◯ **BẮT BUỘC** — sửa file dùng chung | 13 TC | **OK** — Dev có cung cấp danh sách (mục 3, 11 mục) |
| `REG-RUN-001` | **Cao** | **×** — **Leader quyết định (2026-08-21)** không đưa vào phạm vi test đợt này | — (đã gỡ TC-REGRUN001-01/02/03) | × có lý do — Leader duyệt (**RULE-03**) |
| `PERM-003` | **Cao** | ◯ **BẮT BUỘC** — có change bot, localStorage không gắn bot | — | **GAP** → **[BLOCKER]** |
| `SEC-ISO-001` | **Cao** | ◯ nhiều tab cùng ghi khoá bàn giao | TC-CONC003-01 (chỉ 1 tab) | **RISK** → [MAJOR] |
| `ENV-003` | **Cao** | ◯ **BẮT BUỘC** — job nền + asset cache | — (0 TC production) | **GAP** → **[BLOCKER]** **RULE-08** |
| `JOB-001` | **Cao** | ◯ job nền chạy lịch tự sinh | TC-JOB002-01/02 (mã `JOB-002` không tồn tại trong checklist) | **RISK** — chạy `local`, thiếu retry/backoff/đếm bản ghi (Catalog D2) |
| `DEPLOY-ASSET-001` | **Cao** | ◯ **BẮT BUỘC** — sửa JS, **KHÔNG tăng version** | TC-DEPLOYASSET001-01/02 | **RISK** — cả 2 `skip`, chưa chạy production |
| `DEPLOY-LIVE-001` | **Cao** | ◯ release không lock maintain | — | **GAP** → [MAJOR] |
| `COMPAT-LEGACY-001` | **Cao** | ◯ — **thu hẹp còn nhánh "bản ghi tạo trước version-up"**; Leader bỏ 2 nhánh `tag/index.js` ⇄ `index_v2.js` và richmenu cũ ⇄ v2 | TC-COMPATLEGACY001-02 (đề xuất) | **GAP một phần** → [MAJOR] **RULE-09** |
| `PERF-LARGE-001` | Trung bình → **Cao** (bulk/gửi tin) | ◯ | Tối đa 201 bạn | **RISK** → [MAJOR] |
| `UI-003` | Trung bình → **Cao** (rủi ro false success) | ◯ danh sách rỗng | TC-UI003-01 | OK |
| `DATA-AUDIT-001` | **Cao** | **×** — bản sửa **không chạm** logic ghi lịch sử thao tác (chỉ sửa 1 file JS tầng client) | — | × có lý do |
| `PERM-001` / `PERM-002` | **Cao** | **×** — không chạm lưới phân quyền hay API kiểm quyền | — | × có lý do |
| `INTG-*` (LINE / webhook / Sheet / Calendar) | **Cao** | **×** — không chạm tích hợp bên thứ 3 | — | × có lý do |
| `PAY-*` | **Cao** | **×** — không chạm luồng tiền / gói cước | — | × có lý do |
| `MEDIA-*` | Trung bình→Cao | **×** — không chạm file/ảnh | — | × có lý do |
| `FRIEND-001` | **Cao** | **×** — không chạm friend info theo TYPE, chỉ chạm bộ lọc danh sách | — | × có lý do |
| `SEC-001` / `SEC-002` | **Cao** | **×** — không đổi đường truy cập PII, không lộ token | — | × có lý do |
| `ADM-01` (§4 checklist) | — | ◯ về mặt hiện tượng (*bộ lọc phải đúng ngay lần đầu*) | — | **[NIT] only** — **RULE-11**, §4 chưa đủ bằng chứng, không flag BLOCKER/MAJOR |

**Tổng kết F.1** *(cập nhật 2026-08-21 sau quyết định thu hẹp phạm vi của Leader)*: **3 quan điểm ưu tiên Cao có trigger khớp task nhưng GAP hoàn toàn** → `DATA-DB-001` · `PERM-003` · `ENV-003` — đều là **[BLOCKER]**. `COMPAT-LEGACY-001` còn **GAP một phần** (chỉ nhánh bản ghi cũ) ở mức [MAJOR]. `REG-RUN-001` được Leader đánh **×** có lý do. Thêm `DEPLOY-LIVE-001` và `DATA-REF-001` GAP ở mức [MAJOR]. 11 quan điểm được đánh × **đều có lý do** ghi rõ (thoả RULE-03).

---

## 8. Ký duyệt

| Người | Tên | Ngày |
|---|---|---|
| Reviewer (Leader) | | |
| Tester | (đã đọc & hiểu feedback) | |

<!-- Draft sinh bởi /review-tc ngày 2026-08-20 từ 01-bug-task.md + 03-dev-impact.md + 04-tc-list.md (49 TC từ MCP LME TEST STUDIO task #71). Không có 02-spec-reference.md → fallback LME-SYSTEM-SPEC tổng. Đây là DRAFT cho Leader verify, không phải final. -->
