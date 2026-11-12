# 03 — Đánh giá ảnh hưởng từ Dev

> ⚠️ **INPUT KHÔNG CHUẨN FORMAT**: Redmine #45620 **không có** section "Đánh giá ảnh hưởng" với 4 mục con chuẩn (1. Nguyên nhân / 2. Cách fix / 3. Function caller đã check / 4.1-4.2-4.3) trong `description`. Nội dung dưới đây được **gộp lại nguyên văn từ 3 Journal** (#153599, #153630, #153670 — cùng nội dung root cause, viết lại 3 lần qua các bước xử lý khác nhau: Dev người → Dev Studio → Dev handoff cuối). Tester **BẮT BUỘC** đọc lại journal gốc trên Redmine trước khi tick checkbox verify.

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | Thanh Duy Nguyen (phân tích root cause) → "Dev Studio" (agent, theo Journal #153630/#153670). `assigned_to` trên Redmine đang để trống (`-`). |
| Commit / Pull Request | `<chưa có — Journal chỉ ghi tên file đã sửa, không có link PR/commit>` |
| Branch | `ai_studio_fixbug_45620` (Journal #153670; khớp `branch` của Studio task #569) |
| Ngày submit đánh giá | 2026-11-10 (Journal #153599) → cập nhật 2026-11-11 (Journal #153630, #153670) |
| Auto-filled | 2026-11-11 by /new-task |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — ⚠️ KHÔNG tick cho tới khi đã đọc lại Journal #153599 / #153630 / #153670 trên Redmine (nội dung không theo format 4 mục chuẩn — xem cảnh báo đầu file).

---

## 1. Nguyên nhân

Query so khớp keyword của auto-reply (`AutoReplyKeywordRepository.matchingKeyword`) dùng `LOCATE(keyword.keyword collate 'utf8mb4_bin', val)` cho kiểu 部分一致 (khớp từng phần).

- Trên **MySQL 8**, `LOCATE` **không còn áp `COLLATE utf8mb4_bin` ở đối số keyword** — nó so theo collation của tin nhắn `val`, tức `utf8mb4_unicode_ci` của connection job.
- `utf8mb4_unicode_ci` coi **mọi emoji 4-byte là bằng nhau**. Tin nhắn có `😊` vì thế match cả keyword `🫶` lẫn `🌈`.
- Trên **MySQL 5.7**, `COLLATE utf8mb4_bin` vẫn có tác dụng → không lỗi. Đây là lý do fix collate năm 2023 chạy đúng cho tới đợt **upgrade DB lên MySQL 8.0.46 (20/10/2026)** — code không đổi từ 12/2023, lỗi phát sinh thuần từ hành vi MySQL 8.
- Nhánh **完全一致** (khớp hoàn toàn — `val = keyword collate 'utf8mb4_bin'`) **không bị ảnh hưởng** (Dev xác nhận chưa ghi nhận lỗi ở nhánh này).

Bằng chứng (chạy cùng input, session `utf8mb4_unicode_ci`):

| DB | `LOCATE('🌈' COLLATE utf8mb4_bin, tin_nhắn)` | So theo byte (bản fix) |
|---|---|---|
| Dev, MySQL 5.7.42 | 0 | 0 |
| Staging, MySQL 8.0.46 | **11** (vị trí của 😊) | 0 |
| Prod, MySQL 8.0.46 | **11** | 0 |

## 2. Cách fix

Trong `AutoReplyKeywordRepository.matchingKeyword`, nhánh 部分一致 chuyển sang so khớp **theo byte**, không còn phụ thuộc collation:

```sql
-- Cũ
CASE WHEN keyword.logical = 1 THEN LOCATE(keyword.keyword collate 'utf8mb4_bin', val) ...
-- Mới
CASE WHEN keyword.logical = 1 THEN LOCATE(CAST(keyword.keyword AS BINARY), CAST(val AS BINARY)) ...
```

- UTF-8 tự đồng bộ (self-synchronizing), nên tìm chuỗi con theo byte cho kết quả giống tìm theo ký tự. Phân biệt hoa/thường, hiragana/katakana và toàn/nửa độ rộng vẫn giữ như `utf8mb4_bin` trước đây.
- Nhánh 完全一致 giữ nguyên, không sửa.
- **Không cần migrate / sửa dữ liệu** đã có.
- File đã sửa (java-job): `.../sns/line/models/linedb/repository/AutoReplyKeywordRepository.java` — **1 file, 1 dòng** (`1 insertion(+), 1 deletion(-)`).

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

> ⚠️ Dev **không liệt kê** rõ các caller khác của `matchingKeyword` theo format bảng — chỉ ghi 1 dòng đánh giá ảnh hưởng tổng quát ở mục 4 bên dưới ("Mọi auto-reply keyword 部分一致 của mọi bot, kể cả keyword chữ, vì cùng dùng một query so khớp"). Leader/Tester cần tự hỏi Dev xem còn nơi nào khác gọi `AutoReplyKeywordRepository.matchingKeyword` ngoài job xử lý tin nhắn text của friend (vd: callback test gửi thử trên UI, preview trong màn cấu hình auto-reply).

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `AutoReplyKeywordRepository.matchingKeyword` (java-job) | Nhánh 部分一致: `LOCATE` theo byte (`CAST(... AS BINARY)`) thay vì `COLLATE utf8mb4_bin` | Root cause — collation của `LOCATE` đổi hành vi trên MySQL 8 |
| 2 | `<chưa rõ — caller khác chưa được Dev liệt kê>` | | |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `AutoReplyKeywordRepository.matchingKeyword` — nhánh 部分一致 (`logical = 1`) | `.../sns/line/models/linedb/repository/AutoReplyKeywordRepository.java` | Direct | Job xử lý tin nhắn text của friend, auto-reply loại キーワード指定. Áp dụng cho **mọi bot**, keyword chữ hay emoji đều dùng chung query này |

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| — | Không có | — | Dev xác nhận **"Không cần sửa dữ liệu"** — chỉ đổi logic so khớp SQL, không có migration/data fix |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Tự động trả lời (自動応答) — auto-reply kiểu キーワード指定, so khớp **部分一致** (khớp từng phần), mọi bot | F1 | **Low** (theo Dev) — chỉ đổi 1 dòng SQL ở 1 nhánh, tham số bind không đổi; hành vi trở lại đúng như trước khi nâng MySQL 8 và đúng spec (phân biệt emoji/hoa-thường/hiragana-katakana/độ rộng) |
| T2 | Tự động trả lời kiểu **完全一致** (khớp hoàn toàn) — KHÔNG đổi code, nhưng chạy trên cùng bản deploy | — | Low/regression — cần ít nhất 1 TC verify nhánh này **không bị ảnh hưởng** sau fix (Dev khẳng định nhưng chưa có TC xác nhận riêng) |

**Phạm vi ảnh hưởng (theo Dev, Journal #153599/#153630):** mọi bot có auto-reply với keyword kiểu 部分一致 — **kể cả keyword chữ thường** (không chỉ emoji), vì dùng chung 1 query `matchingKeyword`. Lỗi biểu hiện rõ nhất với keyword emoji 4-byte vì `utf8mb4_unicode_ci` coi mọi emoji 4-byte là bằng nhau; với keyword chữ thường collation này so sánh theo ngữ nghĩa ngôn ngữ (vd không phân biệt hoa/thường, hiragana/katakana, toàn/nửa độ rộng) — **cần verify thêm case keyword chữ** (vd `ニジ` katakana có match nhầm `にじ` hiragana không) vì Dev chỉ mô tả cơ chế chung, chưa có TC riêng cho trường hợp này.

**Cách test Dev đề xuất** (Journal #153599): Tạo 2 auto-reply, keyword `🫶` và `🌈`, 部分一致, 何度でも, không filter và không giới hạn thời gian:
1. Gửi `ありがとうございます😊 … 進めています😭`: **không** có auto-reply nào kích hoạt.
2. Gửi riêng `🫶`: chỉ nhận reply của `🫶`.
3. Gửi riêng `🌈`: chỉ nhận reply của `🌈`.

⚠️ **Môi trường test phải dùng MySQL 8 (staging/prd)** — Dev (MySQL 5.7) **không tái hiện được lỗi**. RULE-08 cũng áp dụng vì đây là job nền (job trả lời tự động) — không kết luận từ dev/local nếu DB ở env đó không phải MySQL 8.

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót) — ⚠️ **hiện CHƯA đủ, cần hỏi Dev** các caller khác của `matchingKeyword`
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng — ⚠️ cần thêm case keyword **chữ thường** (không chỉ emoji) để verify phạm vi "mọi bot, kể cả keyword chữ" Dev nêu
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
