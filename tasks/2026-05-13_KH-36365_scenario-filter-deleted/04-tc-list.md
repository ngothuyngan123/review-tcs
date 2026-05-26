# 04 — TC List (do member viết)

> File này được chuyển đổi từ Google Sheet `Testcase` rows 967-972 (gid 1564570326). Format sheet là **nested checklist** (Main / Sub1-5 / Expected / Note), tôi suy luận map sang 10-column TC list.

## Thông tin

| Trường | Giá trị |
|---|---|
| Tester viết TCs | _<chưa rõ — sheet không có cột Assignee>_ |
| Ngày submit | _<chưa rõ — suy luận ≥ 2026-05-11 sau khi bug được báo>_ |
| Version TCs | v1 |
| Link TC gốc | [Sheet — Testcase rows 965-972](https://docs.google.com/spreadsheets/d/1E1ZaqHfbb0mxvLIwgu7WEixMJ3oj4AtX2phsSRAyY4M/edit?gid=1564570326#gid=1564570326&range=965:972) |

---

## TC List

> ⚠️ Sheet không có cột Precondition + Steps tách bạch. Sheet inherit (merge visual) — TC-02 đến TC-06 thừa kế Expected từ TC-01 (cell rỗng). Note cột cuối ghi "bug#36365" → "bug#36370" — không rõ là TC ID hay là bug ID khác liên quan.

| TC ID | Title | Type | Priority | Precondition | Steps | Expected result | Output note | Assignee | Status |
|---|---|---|---|---|---|---|---|---|---|
| TC-01 | [Tạo 1 filter] Tab 1 xóa filter → Tab 2 tạo step **send ngay** | Negative | High | Tạo 1 filter mới + mở 2 tab cùng scenario | 1) Tab 1: xóa filter<br>2) Tab 2: tạo step "send ngay" với filter đó | (a) Tạo step **thất bại**<br>(b) Hiển thị msg JP: `フィルターが削除されたため、画面を再読み込みしてください`<br>(c) Check LINE user: KHÔNG có msg step được gửi đến<br>(d) Check DB: bảng `filter_manage` _<chưa rõ verify gì>_ | Note "bug#36365" | | OK |
| TC-02 | [Tạo 1 filter] Tab 1 xóa filter → Tab 2 tạo step **send sau XX ngày** | Negative | High | _<thừa kế TC-01>_ | _<thừa kế TC-01, chỉ đổi loại step>_ | _<thừa kế TC-01>_ | Note "bug#36366" | | OK |
| TC-03 | [Tạo 1 filter] Tab 1 xóa filter → Tab 2 tạo step **send sau XX giờ** (= flow KH) | Negative | High | _<thừa kế TC-01>_ | _<thừa kế TC-01>_ | _<thừa kế TC-01>_ | Note "bug#36367" — đây là flow KH gốc | | OK |
| TC-04 | [Tạo 2 filter] Màn 1 xóa filter → Màn 2 tạo step **send ngay** | Negative | High | Tạo 2 filter + 2 tab/màn hình | 1) Màn 1: xóa 1 filter<br>2) Màn 2: tạo step "send ngay" với filter đã xóa | (a)(b)(c)(d) tương tự TC-01 | Note "bug#36368" | | OK |
| TC-05 | [Tạo 2 filter] Màn 1 xóa filter → Màn 2 tạo step **send sau XX ngày** | Negative | High | _<thừa kế TC-04>_ | _<thừa kế TC-04>_ | _<thừa kế TC-04>_ | Note "bug#36369" | | OK |
| TC-06 | [Tạo 2 filter] Màn 1 xóa filter → Màn 2 tạo step **send sau XX giờ** | Negative | High | _<thừa kế TC-04>_ | _<thừa kế TC-04>_ | _<thừa kế TC-04>_ | Note "bug#36370" | | OK |
| TC-07 | "Check account staff" (row 973) | _<empty>_ | _<empty>_ | _<empty>_ | _<empty>_ | _<empty>_ | Row 973 chỉ có "Check account staff", không có Sub/Step/Expected | | _<empty>_ |

### Chú thích Note column "bug#xxxxx"

- TC-01 Note = "bug#36365" → đúng bug KH gốc
- TC-02 → TC-06 Note = "bug#36366" → "bug#36370" → **không rõ nghĩa**: là TC ID, hay là bug IDs Redmine liên quan? Cần Leader verify với member. Nếu là bug ID Redmine thì 5 bug này có liên quan tới fix không?

---

## Member tự check trước khi submit

### Coverage check
- [ ] Đã đọc kỹ `01-bug-task.md` — _<chưa verify Redmine>_
- [ ] Đã đọc kỹ `02-spec-reference.md` — N/A
- [ ] Đã đọc kỹ `03-dev-impact.md` — partial (F1, T1 simple, không miss)
- [ ] **Mỗi impact** có **ít nhất 1 TC** verify — OK F1, T1
- [ ] Có **ít nhất 1 TC** verify trực tiếp bug fix (reproduce flow KH) — **OK** TC-03 (1 filter + send sau XX giờ) = scenario KH
- [ ] Có **ít nhất 1 TC regression** cho T1 — _<chưa có regression dedicated, chỉ có negative>_
- [ ] Negative + boundary cho data quan trọng — N/A (không có data update)
- [ ] Mọi TC đều có steps rõ ràng, expected đo lường được — _<FAIL — sheet cell rỗng cho TC-02 → TC-06>_
- [ ] Title TC chứa keyword giúp Leader map impact — _<partial: chứa scenario step type nhưng không có function name `createScenarioStep`>_

### Base checklist LME

> Member không tick — sheet chỉ có TC list raw.

**§A Checklist web**:
- [ ] **A.1 Function checklist** — chưa rà
  - CL5 Double click (button "Tạo step") — chưa cover
  - CL18 Load UI + submit sau — chưa cover dedicated (multi-tab có ngầm cover nhưng cần test reload behavior)
  - CL11 CRUD đúng account — chưa cover (filter của staff khác)
  - CL2 Reload sau save — chưa cover
- [ ] A.2 Non-function — chưa rà

**§B Checklist job**: N/A — task không chạm job

**§C Các tính năng chung**:
- [ ] **C.2 Send message** — task gốc là send duplicate, T1 chạm flow send. Cần verify send lifecycle (sau khi step bị block, không có message gửi). **Member skip**.
- [ ] C.3 Friend info — N/A
- [ ] Còn lại — N/A
