# 04 — TC List (do member viết)

> Nguồn: Google Sheet `Improve form 01/2025 Line user` rows 1550-1577. Sheet format gốc của team LME (cột Main / Sub1..Sub5 / Expected). KHÔNG có cột TC ID / Type / Priority / Precondition / Steps / Assignee / Status như template 04 chuẩn — TC ID dưới đây do reviewer đánh số lại để dễ tham chiếu.

## Block 0 — Tái hiện case khách hàng

> Member ghi nhận: **"Tái hiện case KH: chưa tái hiện được"** — không có TC reproduce.

## Block A — Check form rẽ nhánh, Form có 1 page

| TC | Main | Sub1 | Sub2 | Sub3 | Sub4 | Expected |
|---|---|---|---|---|---|---|
| TC-01 | Check form rẽ nhánh | Form có 1 page | check khi user trả lời số item trong page khác với admin setting | user trả lời số item bị **thừa** với item admin setting | cách test: user đang trả lời / admin thực hiện thêm/xóa item | hiển thị msg: `フォームの質問数が変更されました。画面を再読み込みしてから再度ご回答ください` |
| TC-02 | ↑ | ↑ | ↑ | user trả lời số item bị **thiếu** với item admin setting | (↑) | (↑ msg) |
| TC-03 | ↑ | ↑ | ↑ | admin **thay đổi vị trí thứ tự** item trong page | (↑) | (↑ msg) |
| TC-04 | ↑ | ↑ | form có 1-3 item | — | — | user trả lời form thành công; hiển thị đúng câu trả lời theo item; ở màn submit hiển thị đúng số item có trong 1 page; hiển thị đúng thứ tự item |
| TC-05 | ↑ | ↑ | form có 3-6 item | — | — | (↑) |
| TC-06 | ↑ | ↑ | check sau khi user submit | check ở **gg sheet** | — | ghi nhận đúng câu trả lời của user theo page; ghi nhận đúng số page theo form |
| TC-07 | ↑ | ↑ | ↑ | check ở **form result** | — | ghi nhận đúng câu trả lời của user theo page |

## Block B — Check form rẽ nhánh, Form có nhiều page

| TC | Sub1 | Sub2 | Sub3 | Sub4 | Sub5 | Expected |
|---|---|---|---|---|---|---|
| TC-08 | Form có nhiều page | check khi user trả lời số item trong page khác với admin setting | user trả lời số item bị **thừa** với item admin setting | cách test: user đang trả lời / admin thêm/xóa item | — | msg JP |
| TC-09 | ↑ | ↑ | user trả lời số item bị **thiếu** với item admin setting | (↑) | — | msg JP |
| TC-10 | ↑ | ↑ | admin **thay đổi vị trí thứ tự item** trong page | (↑) | — | msg JP |
| TC-11 | ↑ | ↑ | check khi admin **thêm/xóa page** | user trả lời số item bị **thừa** với page admin setting | — | msg JP |
| TC-12 | ↑ | ↑ | ↑ | user trả lời số item bị **thiếu** với page admin setting | — | msg JP |
| TC-13 | ↑ | ↑ | ↑ | admin **thay đổi vị trí thứ tự page** | page 1 xuống page cuối | msg JP |
| TC-14 | ↑ | ↑ | ↑ | ↑ | page cuối lên page đầu | msg JP |
| TC-15 | ↑ | ↑ | ↑ | ↑ | page đầu ra giữa | msg JP |
| TC-16 | ↑ | form có 1-3 item | — | — | — | happy path (như TC-04) |
| TC-17 | ↑ | form có 3-6 item | — | — | — | (↑) |
| TC-18 | ↑ | check sau khi user submit | check ở **gg sheet** | — | — | ghi nhận đúng câu trả lời user theo page; đúng số page theo form |
| TC-19 | ↑ | ↑ | check ở **form result** | — | — | ghi nhận đúng câu trả lời user theo page |

## Block C — Check form basic

| TC | Main | Sub1 | Sub2 | Sub3 | Sub4 | Expected |
|---|---|---|---|---|---|---|
| TC-20 | Check form basic | check khi user trả lời số item trong page khác với admin setting | user trả lời số item bị **thừa** với item admin setting | cách test: user đang trả lời / admin thêm/xóa item | — | msg JP |
| TC-21 | ↑ | ↑ | user trả lời số item bị **thiếu** | (↑) | — | msg JP |
| TC-22 | ↑ | ↑ | admin **thay đổi vị trí thứ tự item** trong page | (↑) | — | msg JP |
| TC-23 | ↑ | form có 1-3 item | — | — | — | happy path |
| TC-24 | ↑ | form có 3-6 item | — | — | — | (↑) |
| TC-25 | ↑ | check sau khi user submit | check ở **gg sheet** | — | — | ghi nhận đúng câu trả lời user theo page; đúng số page theo form |
| TC-26 | ↑ | ↑ | check ở **form result** | — | — | ghi nhận đúng câu trả lời user theo page |

---

**Tổng**: 26 TCs.
- Negative msg JP (thừa/thiếu/đổi thứ tự): TC-01,02,03,08,09,10,11,12,13,14,15,20,21,22 = **14 TCs**
- Happy path (số item 1-3 / 3-6): TC-04,05,16,17,23,24 = **6 TCs**
- Verify data sau submit (gg sheet + form result): TC-06,07,18,19,25,26 = **6 TCs**
