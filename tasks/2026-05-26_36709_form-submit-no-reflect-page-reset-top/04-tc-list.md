<!-- sync-target: https://docs.google.com/spreadsheets/d/1pT_Z-NZOVYZrTreUdn6mQJI0c_vOPAiwjRf8v-4jg-4/edit?gid=1515885666 -->

# 04 — TC List (fetched from master sheet)

> File này được **fetch từ Google Sheet master** bởi `/new-task` (extension), không phải member viết tay.
> TCs gốc nằm trong sheet "Improve form 01/2025" tab, range A1132:K1176, column J "Bug Report #36709".
> **KHÔNG sửa Title / Expected của TC cũ** — đây là read-only snapshot. Nếu cần TC mới: tạo riêng ở table phụ bên dưới.

## Thông tin

| Trường | Giá trị |
|---|---|
| Tester viết TCs | `<member điền sau khi review>` (TCs gốc do team Form QA, retest cho Bug #36709) |
| Ngày submit | 2026-05-26 (fetched từ master sheet) |
| Version TCs | v1 (snapshot từ master) |
| Link TC gốc (nếu có) | https://docs.google.com/spreadsheets/d/1pT_Z-NZOVYZrTreUdn6mQJI0c_vOPAiwjRf8v-4jg-4/edit?gid=1515885666 |

---

## Bối cảnh từ master sheet

Source sheet "Improve form 01/2025" có cấu trúc khác template 10-cột chuẩn (header: `Assign / Main Function / Sub1 / Sub2 / Sub3 / Sub 4 / Sub 5 / Expect Result / Actual Result / Bug Report #36709 / Bug KH #36428`). TCs trong range A1132:K1176 được mapping sang format 10-cột bằng cách:
- **Title** = leaf-level (Sub sâu nhất có giá trị trong row đó)
- **Precondition** = Main Function (carry-forward) + breadcrumb các Sub level trên leaf
- **Steps** = giữ nguyên giá trị cell leaf
- **Expected result** = cột H "Expect Result" (raw)
- **Status** = cột J "Bug Report #36709" (raw — "Test bug" nghĩa là TC cần retest cho bug #36709)

Master sheet có 1 section header ở row 1147 (paste bug description vào column B) — không phải TC, chỉ phân tách block "regression check" (TC001–TC015) khỏi block "bug reproduction" (TC016–TC028).

Block layout trong range:
- **TC001–TC015** (row 1132–1146): regression checklist cho `Setting rẽ nhánh (26 - 28)` — UI hiển thị + xóa page + sort page.
- **TC016–TC028** (row 1148–1160): reproduction direct cho Bug #36709 — flow add/copy/delete page rồi save / reload-save.
- **TC029–TC042** (row 1161–1174): regression `Check form có nhiều page` — tạo/copy/xóa/sort page với form đa page.
- **TC043** (row 1175): `Check form basic khi save form không bị ảnh hưởng` — sanity save form.
- **TC044** (row 1176): `Check account staff thao tác` — permission staff.

---

## TC List

| TC ID | Title | Type | Priority | Precondition | Steps | Expected result | Output note | Assignee | Status |
|---|---|---|---|---|---|---|---|---|---|
| TC001 | case chưa add thêm page khác | | | Setting rẽ nhánh (26 - 28) > Check hiển thị next page > default > check start page スタートページ | case chưa add thêm page khác | default chọn kết thúc => hiện text 回答完了ページ<br>=> disable không cho edit | row 1132 | | Test bug |
| TC002 | Khi add thêm page mới | | | Setting rẽ nhánh (26 - 28) > Check hiển thị next page > default > check start page スタートページ | Khi add thêm page mới | khi add thêm 1 page mới thì check setting của page cuối cùng trước đó:<br>- nếu page setting là kết thúc form thì change sang thành next sang page bên canh<br>- nếu page setting rẽ nhánh thì giữ nguyên setting rẽ nhánh<br>- page mới add thì default chọn kết thúc form | row 1133 | | Test bug |
| TC003 | Check chọn vào page khác page cuối cùng | | | Setting rẽ nhánh (26 - 28) > Check hiển thị next page > Check chọn next sang page tiếp theo bên phải | Check chọn vào page khác page cuối cùng | có hiện setting này | row 1134 | | Test bug |
| TC004 | check chọn vào page cuối cùng | | | Setting rẽ nhánh (26 - 28) > Check hiển thị next page > Check chọn next sang page tiếp theo bên phải | check chọn vào page cuối cùng | không hiện selection này | row 1135 | | Test bug |
| TC005 | Check copy page | | | Setting rẽ nhánh (26 - 28) > Check hiển thị next page > Check chọn next sang page tiếp theo bên phải | Check copy page | khi copy thì tạo thêm 1 page ở cuối cùng<br>- page mới tạo default là kết thúc form<br>- page trước đó là page cuối cùng (nếu trước đó setting là kết thúc form) thì change sang thành next sang page bên cạnh | row 1136 | | Test bug |
| TC006 | Check có ít nhất 1 chỗ setting rẽ nhánh chọn next tới page này | | | Setting rẽ nhánh (26 - 28) > Check hiển thị next page > Check chọn next sang page tiếp theo bên phải > Check xóa page > khi nhấn nút xóa page | Check có ít nhất 1 chỗ setting rẽ nhánh chọn next tới page này | Khi nhấn xóa page thì hiển thị message comfirm:<br>このページは他のページの遷移先ページとして設定されています。削除した場合、遷移先ページの設定は自動的に「回答完了ページ」に変更されます。このページを削除してよろしいですか？<br>- OK => xóa page, các chỗ có setting next tới page bị xóa thì update thành kết thúc form<br>- Cancel => không xóa page | row 1137 | | Test bug |
| TC007 | Check không có setting rẽ nhánh của page nào chọn next sang page này | | | Setting rẽ nhánh (26 - 28) > Check hiển thị next page > Check chọn next sang page tiếp theo bên phải > Check xóa page > khi nhấn nút xóa page | Check không có setting rẽ nhánh của page nào chọn next sang page này | hiện message comfirm xóa như cũ | row 1138 | | Test bug |
| TC008 | check page ở bên trái của page bị xóa, trước đó setting next sang page bên cạnh | | | Setting rẽ nhánh (26 - 28) > Check hiển thị next page > Check chọn next sang page tiếp theo bên phải > Check xóa page > Check setting rẽ nhánh sau khi xóa page | check page ở bên trái của page bị xóa, trước đó setting next sang page bên cạnh | change setting của page đó thành kết thúc form | row 1139 | | Test bug |
| TC009 | Check các page khác có setting item rẽ nhánh có chọn next sang page bị xóa | | | Setting rẽ nhánh (26 - 28) > Check hiển thị next page > Check chọn next sang page tiếp theo bên phải > Check xóa page > Check setting rẽ nhánh sau khi xóa page | Check các page khác có setting item rẽ nhánh có chọn next sang page bị xóa | toàn bộ các chỗ trước đó chọn next sang page bị xóa thì change thành kết thúc form | row 1140 | | Test bug |
| TC010 | Check chọn kết thúc form | | | Setting rẽ nhánh (26 - 28) > Check hiển thị next page | Check chọn kết thúc form | _(empty in source)_ | row 1141 | | Test bug |
| TC011 | Check chọn setting rẽ nhánh | | | Setting rẽ nhánh (26 - 28) > Check hiển thị next page | Check chọn setting rẽ nhánh | Chọn thì hiện chỗ chọn item để phán đoán việc rẽ nhánh | row 1142 | | Test bug |
| TC012 | sort 2 page cạnh nhau (trong đó có 1 page là page cuối cùng) | | | Setting rẽ nhánh (26 - 28) > Check hiển thị next page > Check khi di chuyển các page | sort 2 page cạnh nhau (trong đó có 1 page là page cuối cùng) | - page được sort thành page cuối cùng thì change setting của page thành kết thúc form<br>- page còn lại change setting thành next sang page bên cạnh | row 1143 | | Test bug |
| TC013 | case 2 page đều setting next sang page bên cạnh | | | Setting rẽ nhánh (26 - 28) > Check hiển thị next page > Check khi di chuyển các page > sort 2 page cạnh nhau (2 page k có page nào là page cuối cùng) | case 2 page đều setting next sang page bên cạnh | change setting của 2 page để hiển thị đúng page được next đến là page bên phải của page đó | row 1144 | | Test bug |
| TC014 | case page setting kết thúc form | | | Setting rẽ nhánh (26 - 28) > Check hiển thị next page > Check khi di chuyển các page > sort 2 page cạnh nhau (2 page k có page nào là page cuối cùng) | case page setting kết thúc form | giữ nguyên setting | row 1145 | | Test bug |
| TC015 | case page setting item rẽ nhánh | | | Setting rẽ nhánh (26 - 28) > Check hiển thị next page > Check khi di chuyển các page > sort 2 page cạnh nhau (2 page k có page nào là page cuối cùng) | case page setting item rẽ nhánh | giữ nguyên setting | row 1146 | | Test bug |
| _Section divider_ | _Row 1147 — paste mô tả Bug #36709 (xem [03-dev-impact.md](03-dev-impact.md))_ | | | | | | | | |
| TC016 | Nhấn add thêm page mới B -> save | | | Form có 1 page A => page A setting là kết thúc form | Nhấn add thêm page mới B -> save | 1. Màn setting form:<br>- Setting rẽ nhánh ở các page hiển thị đúng data được set, page không bị hiện next đến chính nó<br><br>2. User submit form:<br>- user vào trả lời form next được các page đúng theo setting<br>- user submit được form, không bị hiện tượng scroll về đầu page | row 1148 — Expected dùng chung cho block TC016–TC028 | | Test bug |
| TC017 | Nhấn add thêm page mới B -> không nhấn save -> reload lại màn hình -> save | | | Form có 1 page A => page A setting là kết thúc form | Nhấn add thêm page mới B -> không nhấn save -> reload lại màn hình -> save | _(inherit từ TC016)_ | row 1149 | | Test bug |
| TC018 | Nhấn copy page A -> save | | | Form có 1 page A => page A setting là kết thúc form | Nhấn copy page A -> save | _(inherit từ TC016)_ | row 1150 | | Test bug |
| TC019 | Nhấn copy page A -> reload lại màn hình -> save | | | Form có 1 page A => page A setting là kết thúc form | Nhấn copy page A -> reload lại màn hình -> save | _(inherit từ TC016)_ | row 1151 | | Test bug |
| TC020 | add page B -> add thêm page C -> save | | | Form có 1 page A => page A setting là kết thúc form | add page B -> add thêm page C -> save | _(inherit từ TC016)_ | row 1152 | | Test bug |
| TC021 | Nhấn add thêm page B -> delete page B -> nhấn save | | | Form có 1 page A => page A setting là kết thúc form | Nhấn add thêm page mới B -> delete page B -> nhấn save | _(inherit từ TC016)_ | row 1153 | | Test bug |
| TC022 | Nhấn add thêm page B -> delete page B -> reload màn hình -> nhấn save | | | Form có 1 page A => page A setting là kết thúc form | Nhấn add thêm page B -> delete page B -> reload màn hình -> nhấn save | _(inherit từ TC016)_ — **đây là flow KH tái hiện (Redmine journal #119442)** | row 1154 — direct repro Bug #36709 | | Test bug |
| TC023 | Nhấn add thêm page B -> delete page A -> nhấn save | | | Form có 1 page A => page A setting là kết thúc form | Nhấn add thêm page B -> delete page A -> nhấn save | _(inherit từ TC016)_ | row 1155 | | Test bug |
| TC024 | Add page B -> Xóa page B -> Add thêm page C -> save | | | Form có 1 page A => page A setting là kết thúc form | Add page B -> Xóa page B -> Add thêm page C -> save | _(inherit từ TC016)_ | row 1156 | | Test bug |
| TC025 | add page B,C -> xóa cả 2 page -> reload màn hình -> save | | | Form có 1 page A => page A setting là kết thúc form | add page B,C -> xóa cả 2 page -> reload màn hình -> save | _(inherit từ TC016)_ | row 1157 | | Test bug |
| TC026 | Copy page A -> Xóa page vừa copy -> save | | | Form có 1 page A => page A setting là kết thúc form | Copy page A -> Xóa page vừa copy -> save | _(inherit từ TC016)_ | row 1158 | | Test bug |
| TC027 | Copy page A -> Xóa page vừa copy -> reload màn hình -> save | | | Form có 1 page A => page A setting là kết thúc form | Copy page A -> Xóa page vừa copy -> reload màn hình -> save | _(inherit từ TC016)_ | row 1159 | | Test bug |
| TC028 | copy page A nhiều lần liên tiếp -> reload màn hình | | | Form có 1 page A => page A setting là kết thúc form | copy page A nhiều lần liên tiếp -> reload màn hình | _(inherit từ TC016)_ | row 1160 | | Test bug |
| TC029 | tạo 1 page mới | | | Check form có nhiều page > Add thêm page mới | tạo 1 page mới | _(empty in source)_ | row 1161 | | Test bug |
| TC030 | tạo liên tiếp nhiều page mới | | | Check form có nhiều page > Add thêm page mới | tạo liên tiếp nhiều page mới | _(empty in source)_ | row 1162 | | Test bug |
| TC031 | copy page 1 | | | Check form có nhiều page > copy page | copy page 1 | _(empty in source)_ | row 1163 | | Test bug |
| TC032 | copy page ở giữa | | | Check form có nhiều page > copy page | copy page ở giữa | _(empty in source)_ | row 1164 | | Test bug |
| TC033 | copy page cuối | | | Check form có nhiều page > copy page | copy page cuối | _(empty in source)_ | row 1165 | | Test bug |
| TC034 | copy liên tiếp nhiều page | | | Check form có nhiều page > copy page | copy liên tiếp nhiều page | _(empty in source)_ | row 1166 | | Test bug |
| TC035 | Xóa page 1 | | | Check form có nhiều page > Xóa page | Xóa page 1 | _(empty in source)_ | row 1167 | | Test bug |
| TC036 | xóa page ở giữa | | | Check form có nhiều page > Xóa page | xóa page ở giữa | _(empty in source)_ | row 1168 | | Test bug |
| TC037 | xóa page cuối | | | Check form có nhiều page > Xóa page | xóa page cuối | _(empty in source)_ | row 1169 | | Test bug |
| TC038 | xóa liên tiếp nhiều page | | | Check form có nhiều page > Xóa page | xóa liên tiếp nhiều page | _(empty in source)_ | row 1170 | | Test bug |
| TC039 | sort đổi chỗ 2 page -> reload lại màn hình -> nhấn save | | | Check form có nhiều page > Check sort page | sort đổi chỗ 2 page -> reload lại màn hình -> nhấn save | _(empty in source)_ | row 1171 | | Test bug |
| TC040 | sort đổi chỗ 2 page -> nhấn save | | | Check form có nhiều page > Check sort page | sort đổi chỗ 2 page -> nhấn save | _(empty in source)_ | row 1172 | | Test bug |
| TC041 | sort đổi chỗ 2 page -> nhấn xóa 1 page -> save | | | Check form có nhiều page > Check sort page | sort đổi chỗ 2 page -> nhấn xóa 1 page -> save | _(empty in source)_ | row 1173 | | Test bug |
| TC042 | sort đổi chỗ 2 page -> nhấn xóa 1 page -> reload màn hình -> save | | | Check form có nhiều page > Check sort page | sort đổi chỗ 2 page -> nhấn xóa 1 page -> reload màn hình -> save | _(empty in source)_ | row 1174 | | Test bug |
| TC043 | user edit form -> nhấn save | | | Check form basic khi save form không bị ảnh hưởng | user edit form -> nhấn save | Save được form success, user submit form bình thường | row 1175 | | Test bug |
| TC044 | Check account staff thao tác | | | Check account staff thao tác | _(empty in source — main function only)_ | _(empty in source)_ | row 1176 | | Test bug |

### Chú thích cột

- **Type** / **Priority**: cột trống vì source sheet không có 2 trường này. Member/Leader fill khi review.
- **Status** = `Test bug` (raw từ cột J master sheet) — mapping sang dropdown chuẩn `OK / NG / Not test / NG -> Đã fix` khi `/sync-tc` push back: `Test bug` ≈ `Not test` (pending retest).
- **Output note** ghi row number gốc để trace ngược lên master sheet.
- **Expected inherited**: TC017–TC028 dùng chung Expected của TC016 (block bug reproduction) vì master sheet không repeat. KHÔNG sửa khi review.

### Environment (note)

Mặc định test trên **Staging** (`staging.lme.jp`). Bug Report #36709 cần retest ít nhất 1 lần trên **Production** (`step.lme.jp`) với T CLINIC form `1Mアンケート` sau khi deploy.

---

## Member tự check trước khi submit

### Coverage check
- [ ] Đã đọc kỹ [01-bug-task.md](01-bug-task.md)
- [ ] Đã đọc kỹ `02-spec-reference.md` (nếu có)
- [ ] Đã đọc kỹ [03-dev-impact.md](03-dev-impact.md), hiểu 4 mục
- [ ] **Mỗi impact** trong 4.1 / 4.2 / 4.3 có **ít nhất 1 TC** verify (Title / Steps đủ rõ để Leader nhận ra TC nào cover impact nào)
- [ ] Có **ít nhất 1 TC** verify trực tiếp bug fix (reproduce flow KH) — _TC022 match flow Redmine journal #119442_
- [ ] Có **ít nhất 1 TC regression** cho mỗi tính năng trong 4.3
- [ ] Có **ít nhất 1 negative + 1 boundary** cho mỗi data quan trọng trong 4.2 — _check D1 (next_page_type) + D2 (next_page_setting)_
- [ ] Mọi TC đều có steps rõ ràng, expected đo lường được — _block TC017–TC028 và TC029–TC042 nhiều TC Expected để trống, cần Leader confirm có chấp nhận inherit từ Title không_
- [ ] Title TC chứa **keyword** giúp Leader nhận ra impact TC đó cover (tên function / table / màn hình)

### Base checklist LME
Xem [framework/checklist-lme.md](../../framework/checklist-lme.md). Mark các mục đã áp dụng (chỉ những mục **liên quan** đến task này):

**§A Checklist web**:
- [ ] A.1 Function checklist — rà CL1-CL22 (chọn mục liên quan task)
- [ ] A.2 Non-function: URLs đo lường / Regression / Security / Compatibility

**§B Checklist job**:
- [ ] B.1 Job callback (không áp dụng — task không chạm callback)
- [ ] B.2 Job sync Java — CLJ01 (không áp dụng — task không chạm Google sync)

**§C Các tính năng chung** (chọn feature mà task chạm đến):
- [ ] C.1 Bill tiền (không áp dụng)
- [ ] C.2 Send message (không áp dụng)
- [ ] C.3 Friend info (không áp dụng)
- [ ] C.4 Tag (không áp dụng)
- [ ] C.5 Google sheet (không áp dụng)
- [ ] C.6 Google calendar (không áp dụng)
- [ ] C.7 Plan limits (không áp dụng — task chỉ chạm logic page setting nội bộ form)
- [ ] C.8 Sort (✓ áp dụng — TC039–TC042 cover sort page)

<!-- Source: fetched từ Redmine #36709 "Link TCs" → Sheet "1pT_Z-NZOVYZrTreUdn6mQJI0c_vOPAiwjRf8v-4jg-4" tab "Improve form 01/2025" range A1132:K1176 (column J "Bug Report #36709") lúc 2026-05-26. Master sheet có structure hierarchical 11-cột — đã mapping sang 10-cột template (Title=leaf, Precondition=breadcrumb, Status=cột J). KHÔNG sửa Title / Expected của TC cũ. -->
