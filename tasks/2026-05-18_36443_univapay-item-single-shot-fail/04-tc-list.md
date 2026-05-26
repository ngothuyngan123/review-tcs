<!-- sync-target: https://docs.google.com/spreadsheets/d/1Uwdi0PvJE9l1rCYudLhopn52jjO0zbZ9VrqcTwX-XIM/edit?gid=1072366690#gid=1072366690 -->
# 04 — TC List (fetched từ Sheet master)

> File này được auto-fetch từ Google Sheet master tại tab "Improve bill tiền univapay", range A292:J311 (1 header row + 19 TC rows).
> **KHÔNG sửa TCs này nếu chưa confirm với Leader.** Đây là TC team đã viết — giữ nguyên để `/review-tc` tham chiếu.

## Thông tin

| Trường | Giá trị |
|---|---|
| Tester viết TCs | `<member điền sau khi review>` |
| Ngày submit | `<member điền sau khi review>` |
| Version TCs | v1 |
| Link TC gốc | https://docs.google.com/spreadsheets/d/1Uwdi0PvJE9l1rCYudLhopn52jjO0zbZ9VrqcTwX-XIM/edit?gid=1072366690#gid=1072366690 |

---

## TC List

> **Lưu ý**: Sheet master tab "Improve bill tiền univapay" dùng schema dạng outline lồng nhau (function group → item group → sub-item/precondition → step → expected → status). KHÔNG khớp 100% với schema chuẩn 10-cột (TC ID / Title / Type / Priority / Precondition / Steps / Expected / Output note / Assignee / Status). Dưới đây paste **NGUYÊN VĂN** dữ liệu cell từ sheet — preserve cấu trúc gốc để Leader review đúng những gì member đã ghi.

### Row 292 — Bug header + Dev evaluation (không phải TC)

**Row 292 (col A):**
```
Bug KH #36443: [15-05-2026][10926][App + API app] 商品決済 — sau khi hiển thị 「処理完了まで2～3分かかる場合があります。」 thì màn hình tự quay lại trước khi bấm nút mua → không thanh toán được
1. Nguyên nhân
   - Khi bấm nút mua, gặp lỗi từ univapay nhưng chưa hiển thị message lỗi cho user
2. Cách fix
   - Set error message return về cho frontend để hiển thị
3. Đã check và sửa các function sử dụng đến function/data vừa sửa
4. Đánh giá ảnh hưởng
        4.1 List function
            - paymentCreditCardItemV2Univapay (app/Http/Controllers/Basic/SalesManagementV2Controller.php)
        4.2 List những data bị update khi fix bug
            - k có
        4.3 Dựa vào 2 mục trên list những tính năng sẽ ảnh hưởng
            - bấm nút mua item, case có webhook
```

### Rows 293-311 — TCs (paste nguyên văn, giữ cột gốc)

| Row | A — Function group | B — Item group | C — Sub-item / Precondition | D — Test step | G — Expected | H — Status |
|---|---|---|---|---|---|---|
| 293 | Check liên kết bill tiền **không sử dụng webhook** | Mua item bill 1 lần | Số tiền bill max của account test là 500,000 | mua item có set số tiền bill = 499,999 | Mua item success, redirect về màn talklist của line | Not test |
| 294 | | | | mua item có set số tiền bill = 500,000 | | Not test |
| 295 | | | | mua item có set số tiền bill = 500,001 | Bill tiền fail, hiển thị message lỗi cho user | Not test |
| 296 | | Mua item bill chu kỳ | Số tiền bill max của account test là 500,000 | mua item có set số tiền bill = 499,999 | Mua item success, redirect về màn talklist của line | Not test |
| 297 | | | | mua item có set số tiền bill = 500,000 | | Not test |
| 298 | | | | mua item có set số tiền bill = 500,001 | Bill tiền fail, hiển thị message lỗi cho user | Not test |
| 299 | | check double click button mua | | | | Not test |
| 300 | Check liên kết bill tiền **có sử dụng webhook** | Mua item bill 1 lần | Số tiền bill max của account test là 500,000 | mua item có set số tiền bill = 499,999 | Mua item success, redirect về màn talklist của line | **OK** |
| 301 | | | | mua item có set số tiền bill = 500,000 | | Not test |
| 302 | | | | mua item có set số tiền bill = 500,001 | Bill tiền fail, hiển thị message lỗi cho user | Not test |
| 303 | | | | Check case bill tiền chưa get được kết quả bill ngay | Hiện màn thông báo theo design mới<br>https://xd.adobe.com/view/6d6b04be-0175-4ffe-a980-d57cf80ef7a9-3838/specs | Not test |
| 304 | | Mua item bill chu kỳ | Số tiền bill max của account test là 500,000 | mua item có set số tiền bill = 499,999 | Mua item success, redirect về màn talklist của line | Not test |
| 305 | | | | mua item có set số tiền bill = 500,000 | | Not test |
| 306 | | | | mua item có set số tiền bill = 500,001 | Bill tiền fail, hiển thị message lỗi cho user | Not test |
| 307 | | | | Check case bill tiền chưa get được kết quả bill ngay | Hiện màn thông báo theo design mới<br>https://xd.adobe.com/view/6d6b04be-0175-4ffe-a980-d57cf80ef7a9-3838/specs | Not test |
| 308 | | check double click button mua | | | | Not test |
| 309 | Check cover bill tiền **stripe** | item có số tiền bill < số tiền bill max của stripe | user nhấn nút mua item | | Mua item success, redirect về màn talklist của line | Not test |
| 310 | | item có số tiền bill = số tiền bill max của stripe | | | | Not test |
| 311 | | item có số tiền bill > số tiền bill max của stripe | | | Bill tiền fail, hiển thị message lỗi cho user | Not test |

> **Ghi chú đọc bảng**: cell trống ở cột A/B/C tức là kế thừa giá trị từ row gần nhất phía trên có giá trị (Sheet outline convention). Vd row 294 thuộc nhóm "Check liên kết bill tiền không sử dụng webhook" → "Mua item bill 1 lần" → precondition "Số tiền bill max của account test là 500,000", step "mua item có set số tiền bill = 500,000".

---

## Member tự check trước khi submit

### Coverage check
- [ ] Đã đọc kỹ `01-bug-task.md`
- [ ] Đã đọc kỹ `02-spec-reference.md` (nếu có)
- [ ] Đã đọc kỹ `03-dev-impact.md`, hiểu 4 mục
- [ ] **Mỗi impact** trong 4.1 / 4.2 / 4.3 có **ít nhất 1 TC** verify
- [ ] Có **ít nhất 1 TC** verify trực tiếp bug fix (reproduce flow KH: số tiền > max Univapay → message lỗi hiển thị)
- [ ] Có **ít nhất 1 TC regression** cho mỗi tính năng trong 4.3
- [ ] Có **ít nhất 1 negative + 1 boundary** cho mỗi data quan trọng trong 4.2
- [ ] Mọi TC đều có steps rõ ràng, expected đo lường được
- [ ] Title TC chứa **keyword** giúp Leader nhận ra impact TC đó cover

### Base checklist LME
Xem [framework/checklist-lme.md](../../framework/checklist-lme.md). Mark các mục đã áp dụng (chỉ những mục **liên quan** đến task này):

**§A Checklist web**:
- [ ] A.1 Function checklist — rà CL1-CL22 (chọn mục liên quan task)
- [ ] A.2 Non-function: URLs đo lường / Regression / Security / Compatibility

**§B Checklist job**:
- [ ] B.1 Job callback (nếu chạm callback) — **liên quan: webhook Univapay**
- [ ] B.2 Job sync Java — CLJ01 (nếu chạm Google sync)

**§C Các tính năng chung** (chọn feature mà task chạm đến):
- [x] C.1 Bill tiền — **flow chính của task**
- [ ] C.2 Send message
- [ ] C.3 Friend info
- [ ] C.4 Tag
- [ ] C.5 Google sheet
- [ ] C.6 Google calendar
- [ ] C.7 Plan limits
- [ ] C.8 Sort

<!-- Source: fetched từ Redmine #36443 Link TCs, range A292:J311 tab "Improve bill tiền univapay" lúc 2026-05-18. KHÔNG sửa TCs này nếu chưa confirm với Leader. -->
