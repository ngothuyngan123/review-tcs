<!-- sync-tcs: url=https://docs.google.com/spreadsheets/d/1QKxXc0pbfX07gqzCmlXDVsRgnAUoPUweev78qxAx82g/edit?gid=412698763#gid=412698763 | sheet=Improve 01/07/2026 | anchor=Main Function -->

# 04 — TC List (do member viết) — v2 (đã sửa cơ chế auto-save)

## Thông tin

| Trường | Giá trị |
|---|---|
| Tester viết TCs | `<member điền>` |
| Ngày submit | `2026-07-01` |
| Version TCs | `v2` (rewrite sau review Round 1 — sửa cơ chế auto-save + tách trạng thái key lỗi/hợp lệ) |
| Link TC gốc | https://docs.google.com/spreadsheets/d/1QKxXc0pbfX07gqzCmlXDVsRgnAUoPUweev78qxAx82g/edit?gid=412698763#gid=412698763 (tab "Improve 01/07/2026", range A4:G25) |

---

## TC List (dạng decision-table phân cấp — giữ nguyên format Sheet human)

> Cấu trúc: **Main Function** → **Điều kiện (Sub1)** → **Thao tác (Sub2)** → **Biến thể (Sub3/Sub4)** → **Expected**. Đây là format anchored của Sheet human, KHÔNG phải 10 cột chuẩn.

| No. | Main Function | Điều kiện (Sub1) | Thao tác (Sub2) | Biến thể (Sub3/4) | Expected result |
|---|---|---|---|---|---|
| 1 | **Check change tên BOT** | Bot có channel secret **bị lỗi** | Mở 表示設定 → Change tên | — | Change thành công tên; Lưu và hiển thị lịch sử change name |
| 2 | | (bị lỗi) | Mở 表示設定 → Xóa tên | — | Message lỗi 「アカウント名を入力してください」; KHÔNG lưu; hiển thị lịch sử change name |
| 3 | | Bot có channel secret **hợp lệ** | Mở 表示設定 → Change tên | — | Change thành công tên; Lưu và hiển thị lịch sử change name |
| 4 | | (hợp lệ) | Mở 表示設定 → Xóa tên | — | Message lỗi 「アカウント名を入力してください」; KHÔNG lưu; hiển thị lịch sử change name |
| 5 | **Check change ảnh profile** | Bot có channel secret **bị lỗi** | Mở 表示設定 → Change ảnh | Ảnh hợp lệ | Change thành công ảnh; Lưu và hiển thị lịch sử change ảnh |
| 6 | | (bị lỗi) | Change ảnh | Ảnh không hợp lệ — không đúng định dạng | Báo message lỗi |
| 7 | | (bị lỗi) | Change ảnh | Ảnh không hợp lệ — >10MB | Báo message lỗi |
| 8 | | (bị lỗi) | Mở 表示設定 → Xóa ảnh | — | Xóa thành công ảnh; Lưu và hiển thị lịch sử xóa ảnh |
| 9 | | Bot có channel secret **hợp lệ** | Change ảnh | Ảnh hợp lệ | Change thành công ảnh; Lưu và hiển thị lịch sử change ảnh |
| 10 | | (hợp lệ) | Change ảnh | Ảnh không hợp lệ — không đúng định dạng | Báo message lỗi |
| 11 | | (hợp lệ) | Change ảnh | Ảnh không hợp lệ — >10MB | Báo message lỗi |
| 12 | | (hợp lệ) | Xóa ảnh | — | Xóa thành công ảnh; Lưu và hiển thị lịch sử xóa ảnh |
| 13 | **Check change LINE developers 接続情報** | Change Messaging API - **Channel Secret** | Nhập giá trị hợp lệ | — | Lưu thành công; Lưu và hiển thị lịch sử change |
| 14 | | Messaging API - Channel Secret | Nhập giá trị không hợp lệ | — | Báo mess: `入力した情報が間違っています。WEBブラウザの自動翻訳機能が原因の可能性がございますので、自動翻訳を無効にした状態でお試しください` |
| 15 | | Messaging API - Channel Secret | Xóa => để trống | — | Báo mess: `Channel Secretを入力してください。` |
| 16 | | Change **LINEログイン - Channel ID** | Nhập giá trị hợp lệ | — | Lưu thành công; Lưu và hiển thị lịch sử change |
| 17 | | LINEログイン - Channel ID | Nhập giá trị không hợp lệ | — | Báo mess: `入力した情報が間違っています。...自動翻訳を無効にした状態でお試しください` |
| 18 | | LINEログイン - Channel ID | Xóa => để trống | — | Báo mess: `入力した情報が間違っています。...自動翻訳を無効にした状態でお試しください` |
| 19 | | Change Messaging API - **Channel Secret** ⚠️(trùng nhãn với #13-15) | Nhập giá trị hợp lệ | — | Lưu thành công; Lưu và hiển thị lịch sử change |
| 20 | | Messaging API - Channel Secret ⚠️ | Nhập giá trị không hợp lệ | — | Báo mess: `入力した情報が間違っています。...` |
| 21 | | Messaging API - Channel Secret ⚠️ | Xóa => để trống | — | Báo mess: `入力した情報が間違っています。...` ⚠️(mâu thuẫn với #15) |
| 22 | **[CL1] Account staff** (row cũ, format 10 cột) | Regression / Medium | 1. Staff CÓ quyền → đổi ảnh/tên → lưu. 2. Staff KHÔNG quyền → truy cập màn 表示設定. | Precondition: 1 staff có quyền + 1 staff không quyền | Staff có quyền: lưu OK như account chính. Staff không quyền: không access được màn. |

---

## Ghi chú cấu trúc (reviewer)

- **Điểm mới v2**: tách rõ **Điều kiện "channel secret bị lỗi" vs "hợp lệ"** — đây chính là điều kiện reproduce bug (broken key + auto-save tên/ảnh → vẫn Change thành công). Đã sửa đúng cơ chế **auto-save** (không còn bước "bấm nút Lưu").
- **Điểm mới**: thêm assertion "**hiển thị lịch sử change name/ảnh**" (change history) + section **LINEログイン - Channel ID**.
- ⚠️ **No.19-21 trùng nhãn** với No.13-15 ("Messaging API - Channel Secret") — nghi copy-paste, và No.21 (empty) expected `入力した情報が間違っています` **mâu thuẫn** No.15 (empty) expected `Channel Secretを入力してください。`. Cần member xác nhận No.19-21 thực chất là field nào (vd LINEログイン - Channel Secret?).

<!-- Source: fetched từ Sheet "Improve 01/07/2026" range A4:G25 lúc 2026-07-01 (bản v2 human update sau review Round 1). Format hierarchical decision-table, giữ nguyên giá trị cell. -->
