# 03 — Đánh giá ảnh hưởng từ Dev

⚠️ **INPUT THIẾU: Redmine #43235 chưa có "Đánh giá ảnh hưởng phía dev"** — ticket chỉ có mô tả yêu cầu test (domain callback phụ `cb-2.lmes.jp` + DB backup Contabo + forward bên thứ 3), KHÔNG có section Đánh giá ảnh hưởng (nguyên nhân / cách fix / caller đã check / 4.1-4.2-4.3). `/write-tc` và `/review-tc` sẽ không có cơ sở map coverage `F*/D*/T*` nếu chạy với input này. Yêu cầu Dev bổ sung trực tiếp trên Redmine #43235 trước khi tiếp tục, hoặc paste tay vào file này.

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `<chưa rõ>` |
| Commit / Pull Request | `<chưa có>` |
| Branch | `<chưa rõ>` |
| Ngày submit đánh giá | `<chưa rõ>` |
| Auto-filled | 2026-10-15 by /new-task |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

`<Input thiếu — Dev chưa cung cấp>`

## 2. Cách fix

`<Input thiếu — Dev chưa cung cấp>`

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `<Input thiếu>` | | |
| 2 | | | |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `<Input thiếu>` | | Direct / Indirect | |
| F2 | | | | |
| F3 | | | | |

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | `<Input thiếu>` | CREATE / UPDATE / DELETE / MIGRATE | |
| D2 | | | |
| D3 | | | |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | `<Input thiếu>` | F1, D1 | High / Medium / Low |
| T2 | | | |
| T3 | | | |

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
