# Kho TCs tổng hợp — dự án LME

Gộp toàn bộ TCs rời rạc trong [folder TCs trên Drive](https://drive.google.com/drive/folders/1eWgC1GnG6n8JvYGcBcbyPZLfDRiJLIKG)
(57 file × ~700 tab) thành **một bộ TCs chuẩn: mỗi tính năng = 1 tab**.

**Google Sheet đích**: 1 file, tab `_README` + `_Nguồn & phạm vi` + `_Mâu thuẫn cần quyết`
+ 1 tab / tính năng.

## Tên tab

```
<Mã màn hình> <Tên tiếng Việt> (<Tên màn hình tiếng Nhật>)
```

VD `FA-001 Chat 1:1 (1:1チャット)` · `FA-012 Quản lý thẻ (タグ管理)`.

Khai báo bằng 3 khoá `code` / `vi` / `jp` trong `FEATURES` ở [build.py](build.py); `tab_title()`
ghép lại. Tên tiếng Việt là tên user gõ khi chạy `/collect-tcs`; tên tiếng Nhật tra ở bảng feature
trong [templates/LME-SYSTEM-SPEC.md](../templates/LME-SYSTEM-SPEC.md).
Đổi tên một tính năng đã gộp → `to_sheet()` **rename** tab cũ theo `code` nên `gid` không đổi.

## Format 12 cột

> ⚠️ **KHÁC** 16 cột canonical của [`/write-tc`](../.claude/commands/write-tc.md) và
> [`/review-tc`](../.claude/commands/review-tc.md). Đây là format riêng của kho.

| # | Cột | Giá trị |
|---|---|---|
| 1 | `ID` | `TC-<PREFIX>-<nn>` — tuần tự theo thứ tự màn hình/chức năng |
| 2 | `Nhóm` | `UI` / `API` / `Data` — tầng kiểm chứng, suy tự động từ mã quan điểm |
| 3 | `Mã quan điểm` | mã trong [framework/checklist-lme.md](../framework/checklist-lme.md) |
| 4 | `Màn hình/chức năng` | nhóm chức năng trong màn (tham số `sec` của `tc()`) |
| 5 | `Loại case` | `Normal` / `Abnormal` / `Boundary` |
| 6 | `Tên case` | tiêu đề TC (không còn prefix `[<nhóm>]`) |
| 7 | `Tiền điều kiện` | |
| 8 | `Các bước thực hiện` | |
| 9 | `Dữ liệu nhập` | |
| 10 | `Kết quả mong đợi` | |
| 11 | `Kết quả thực thi` | **luôn để trống** — người test tự điền |
| 12 | `Ghi chú` | nguồn `r<dòng>` · `MT-xx` · kèm `Môi trường: PRODUCTION` / `Đánh giá spec: ...` |

- **Dòng 1 của mỗi tab tính năng là dòng tiêu đề cột.** Không còn khối mô tả phía trên bảng —
  nguồn đã gộp / đã loại / spec đối chiếu của **tất cả** màn hình nằm ở tab `_Nguồn & phạm vi`.
- Cột `Nhóm` suy từ bảng `GROUP_MAP` trong [data/_common.py](data/_common.py) (khớp tiền tố mã
  quan điểm dài nhất trước). Suy sai chỗ nào thì ghi đè từng TC bằng `group="API"` trong `tc()`.
  Mã quan điểm mới không khớp tiền tố nào → mặc định `UI`, nhớ bổ sung vào bảng.
- `env=` và `spec=` của `tc()` **giữ nguyên** trong file data; build tự ghép vào đầu cột `Ghi chú`
  nên không mất RULE-08 (media · domain · job · loadbalance · bill tiền · race · performance
  bắt buộc chạy PRODUCTION).
- Bản markdown trong thư mục này vẫn giữ khối `Nguồn đã gộp` / `Đã loại` / thống kê để review và
  diff bằng git. Tên file: `<mã màn hình>-<tên tiếng Việt>-<tên tiếng Nhật>.md`,
  VD `fa001-chat11-11チャット.md` · `fa012-quanlythe-タグ管理.md`. Tên VN bỏ dấu + viết liền,
  tên JP giữ nguyên (chỉ bỏ khoảng trắng + ký tự Windows cấm đặt tên file, VD `1:1` → `11`).
  Đổi `vi`/`jp` trong `FEATURES` → đổi luôn tên file; build in ra danh sách file cũ để xoá tay.

## Định dạng chuẩn của tab tính năng

Lấy tab **`FA-012 Quản lý thẻ (タグ管理)`** làm chuẩn — áp cho **mọi tab tính năng**, kể cả tab
tạo mới sau này. Khai báo ở đầu [build.py](build.py); sửa ở đó là đổi cho tất cả:

| Hằng số | Giá trị |
|---|---|
| `TAB_FROZEN_ROWS` | `1` — đóng băng dòng tiêu đề |
| `TAB_FROZEN_COLS` | `4` — đóng băng `ID` · `Nhóm` · `Mã quan điểm` · `Màn hình/chức năng` |
| `TAB_WIDTHS` | `[80, 64, 64, 80, 73, 244, 244, 244, 200, 244, 80, 300]` (px, theo đúng 12 cột) |

```bash
python kho-tcs/build.py format   # chỉ đồng bộ ĐỊNH DẠNG, KHÔNG ghi đè dữ liệu trong tab
python kho-tcs/build.py sheet    # build lại nội dung — cũng tự áp định dạng chuẩn
```

Dùng `format` khi chỉ cần chỉnh lại độ rộng cột / đóng băng mà không muốn build lại nội dung
(giữ nguyên các ô Leader đã điền tay, ví dụ cột `QUYẾT ĐỊNH CỦA LEADER` ở tab `_Mâu thuẫn cần quyết`).

3 tab meta (`_README` · `_Nguồn & phạm vi` · `_Mâu thuẫn cần quyết`) có số cột khác 12 nên giữ
định dạng riêng (`META_WIDTHS` trong `build.py`, đóng băng 1 dòng / 1 cột).

## Nguyên tắc gộp

| # | Quy tắc |
|---|---|
| 1 | **Loại trùng** — TC cùng đường dẫn chức năng + cùng kết quả mong đợi → giữ 1 |
| 2 | **Conflict** — cùng chức năng, kết quả mong đợi khác nhau → **ưu tiên TC mới nhất** (ngày ở tab `Info` của file gốc + tab master còn được cập nhật) |
| 3 | **Logic cũ** — TC thuộc luồng đã bị đợt improve mới thay thế → bỏ; nếu ảnh hưởng hành vi thì ghi vào tab `_Mâu thuẫn` |
| 4 | **Truy vết** — cột `Ghi chú` của mỗi TC ghi nguồn dạng `r<số dòng>` ở tab gốc |
| 5 | **Đối chiếu spec** — so với `spec-features/`; mọi điểm lệch đưa vào tab `_Mâu thuẫn cần quyết`, **không tự chọn bên nào** |

## Quy trình chạy 1 tính năng

Dùng slash command **[`/collect-tcs <tính năng>`](../.claude/commands/collect-tcs.md)** —
skill này mô tả đầy đủ 8 bước. Tóm tắt phần chạy lệnh:

```bash
# 1. Tìm nguồn (tự retry 503, lọc tab không phải TC, khớp theo ranh giới từ)
python scripts/list_tc_sources.py tag

# 2. Lấy grid ĐÃ BUNG MERGED CELL của các tab nguồn
python scripts/fetch_grid.py <spreadsheet_id> <out.json> "<tab 1>" "<tab 2>"

# 3. Viết TCs vào kho-tcs/data/<feature>_s*.py + <feature>_conflicts.py
# 4. Đăng ký feature trong FEATURES ở kho-tcs/build.py
# 5. Sinh output
python kho-tcs/build.py md       # markdown trong kho-tcs/ (review + diff bằng git)
python kho-tcs/build.py sheet    # đẩy lên Google Sheet
```

> ⚠️ **Merged cell**: các file TCs cũ dùng cấu trúc cây `Main Function / Sub1..Sub5 / Expect Result`
> với ô gộp. Đọc bằng `values.get` thuần sẽ **sai phân cấp** (ô gộp trả về rỗng).
> Luôn dùng `scripts/fetch_grid.py` — script này lấy `sheets.merges` từ API và bung ô gộp ra từng dòng.

## Về Google Sheet đích

Service account **không tạo được file mới** (Google đã bỏ Drive storage cho service account).
Sheet phải được tạo bằng tài khoản người dùng, share quyền **Editor** cho
`mcp-shhets@snappy-run-490703-k8.iam.gserviceaccount.com`, rồi lưu `spreadsheetId`
vào `kho-tcs/.sheet-id` (đã gitignore).

## Tiến độ

> Bảng này được **sinh tự động** vào tab `_README` của Google Sheet (hàm `progress_rows()` ở
> [build.py](build.py)). Trạng thái tính từ 2 nguồn: cột `Trạng thái` của bảng mâu thuẫn
> (`✅ ĐÃ CHỐT` / `⏳ CHỜ QUYẾT ĐỊNH`) và khoá **`applied`** trong `FEATURES` — ngày đã ÁP quyết định
> của Leader vào TCs. **Sau khi sửa TCs theo quyết định, nhớ điền `applied`**, nếu không màn hình đó
> vẫn bị xếp vào nhóm "chưa cập nhật TC".

| Trạng thái | Nghĩa |
|---|---|
| ✅ XONG | Đã chốt 100% mâu thuẫn **và** đã cập nhật TCs theo quyết định |
| 🔄 ĐÃ ÁP QUYẾT ĐỊNH | TCs đã sửa theo các quyết định đã có, nhưng **vẫn còn mâu thuẫn chưa chốt** |
| 🟠 CHƯA CẬP NHẬT TC | Mâu thuẫn đã chốt nhưng **TCs chưa được sửa** theo quyết định |
| 🔴 CHỜ QUYẾT ĐỊNH | Đã gom TCs, **chưa mâu thuẫn nào được chốt** |
| ⬜ CHƯA COLLECT | Chưa chạy `/collect-tcs` cho màn hình này |

**17 / 41 màn hình đã gom TCs** (danh mục 41 màn lấy từ `ALL_SCREENS` trong `build.py`,
trích từ [templates/LME-SYSTEM-SPEC.md](../templates/LME-SYSTEM-SPEC.md)).

| Mã | Màn hình | Spec đối chiếu | Số TC | Mâu thuẫn (chốt/tổng) | Trạng thái |
|---|---|---|---|---|---|
| FA-001 | Chat 1:1 (1:1チャット) | `admin/chat-11/` | 430 | 0 / 20 | 🔴 CHỜ QUYẾT ĐỊNH |
| FA-003 | Tự động trả lời (自動応答) | `admin/auto-reply/` | 285 | 0 / 25 | 🔴 CHỜ QUYẾT ĐỊNH |
| FA-004 | Rich Menu (リッチメニュー) | `admin/rich-menu/` | 488 | 26 / 27 | 🔄 ĐÃ ÁP QUYẾT ĐỊNH (2026-08-22) |
| FA-007 | Setting add friend (あいさつメッセージ) | `admin/setting-add-friend/` | 171 | 0 / 18 | 🔴 CHỜ QUYẾT ĐỊNH |
| FA-008 | Broadcast (メッセージ配信) | `admin/message-send-all/` | 345 | 0 / 22 | 🔴 CHỜ QUYẾT ĐỊNH |
| FA-009 | Phát hành theo bước (ステップ配信) | `admin/scenario/` | 409 | 0 / 41 | 🔴 CHỜ QUYẾT ĐỊNH |
| FA-010 | Mẫu tin nhắn (テンプレート) | `admin/message-template/` | 394 | 0 / 49 | 🔴 CHỜ QUYẾT ĐỊNH |
| FA-011 | Tạo biểu mẫu (フォーム作成) | `admin/form-answer/` | 481 | 22 / 23 | 🔄 ĐÃ ÁP QUYẾT ĐỊNH (2026-08-19 + 08-22) |
| FA-012 | Quản lý thẻ (タグ管理) | `admin/tag-management/` | 266 | 14 / 14 | ✅ XONG (2026-08-19) |
| FA-013 | Friend list (友だちリスト) | `admin/friend-list/` | 154 | 0 / 14 | 🔴 CHỜ QUYẾT ĐỊNH |
| FA-015 | Quản lý thông tin bạn bè (友だち情報管理) | `admin/friend-information/` | 339 | 0 / 18 | 🔴 CHỜ QUYẾT ĐỊNH |
| FA-019 | Đặt lịch bài học (レッスン予約) | `admin/lesson-booking/` | 632 | 0 / 65 | 🔴 CHỜ QUYẾT ĐỊNH |
| FA-020 | Đặt lịch salon (サロン・面談予約) | `admin/salon-booking/` | 498 | 0 / 42 | 🔴 CHỜ QUYẾT ĐỊNH |
| FA-021 | Event booking (イベント予約) | `admin/event-booking/` | 375 | 0 / 35 | 🔴 CHỜ QUYẾT ĐỊNH |
| FA-026 | Bill tiền item (商品販売) | `admin/bill-item/` | 381 | 0 / 40 | 🔴 CHỜ QUYẾT ĐỊNH |
| FA-031 | Bill tiền tool (契約プラン・決済情報) | `admin/billing-plan/` | 398 | 0 / 46 | 🔴 CHỜ QUYẾT ĐỊNH |
| FA-033 | Backup (データコピー) | `admin/backup/` | 359 | 0 / 31 | 🔴 CHỜ QUYẾT ĐỊNH |

**24 màn hình ⬜ CHƯA COLLECT**: FA-002 · FA-005 · FA-006 · FA-014 ·
FA-016 · FA-017 · FA-018 · FA-022 · FA-023 · FA-024 · FA-025 · FA-027 · FA-028 · FA-029 · FA-030 ·
FA-032 · FA-034 · FA-035 · FA-036 · FA-037 · FA-038 · FA-039 · FA-040 · FA-041.

**Thứ tự tab trên Sheet** = 3 tab meta rồi đến các tab tính năng **sắp theo mã màn hình tăng dần**
(`FEATURES.sort(key=code)` trong `build.py`) — thứ tự khai báo trong `FEATURES` không còn ảnh hưởng.

> **FA-020 — trạng thái (2026-08-25):**
> - 498 TC gộp từ **16 tab** của `11.1 TCsLine_SalonCalendar` (corpus gốc **13.482 TC lá**, lớn nhất
>   trong các feature đã gom). Tab master lớn nhất là「Quản lý calendar」(6.179 dòng, 4.097 TC lá,
>   07/2024 → 07/2026); khối MỚI NHẤT là tab「#38520」(07/2026, format phẳng AI).
> - **Đã loại 4 phiên bản cũ của bộ ma trận 受付上限** (`Test limit booking` V1 → V4_11/2025,
>   ~4.100 TC lá) vì đã bị `Test limit booking_V4_2` (02/2026) thay thế — cần user xác nhận.
> - Phủ **79/80 quan điểm** của `checklist-lme.md` (chỉ `FUNC-UNIQ-001` không áp dụng —
>   salon không có ràng buộc unique nào: 2 staff/course trùng tên đều hợp lệ).
> - 42 mâu thuẫn, trong đó **12 mức CAO**. Nặng nhất: MT-22 (spec chỉ mô tả 2/4 tuỳ chọn 受付上限),
>   MT-20 (tính năng スタッフ自動割り当て không có trong spec), MT-03 (xóa ca có xóa booking không),
>   MT-29 (remind khi course/staff OFF), MT-35 (phân quyền staff CHƯA từng test được).

> **FA-033 — trạng thái (2026-08-25):**
> - 359 TC gộp từ 7 tab của `TCsLine_BackUp` + tab「Improve backup media」của `TCsLine_Improve chung`.
>   Corpus đọc vào ~1.170 dòng, trong đó 2 tab master còn sống là「Backup 1.0」(03/2023 → 07/2026)
>   và「Backup (job)」(05/2023 → 05/2026).
> - **31/31 mâu thuẫn đang CHỜ QUYẾT ĐỊNH** — 17 mức CAO. **`MT-00` và `MT-01` phải chốt TRƯỚC** vì
>   ảnh hưởng ~100 TC nhóm màn hình:
>   `MT-00` — spec (chốt 2026-03-30) tả GIAO DIỆN CŨ 1 màn / 3 endpoint, còn 3 tab `[AI]`/`[MN]` (2026)
>   tả GIAO DIỆN MỚI 7 màn (SCR-01…SCR-07) / 5 endpoint (thêm `EP-04 backup-status` polling và
>   `EP-05 reissue-transfer-code`) + phân trang lịch sử.
>   `MT-01` — **chiều copy bị đảo**: spec nói người thao tác là LOA NGUỒN (ô nhập là「データ受信コード」của
>   LOA đích), corpus mới nói ô nhập là「コピー元アカウントのコピーコード」⇒ người thao tác là LOA ĐÍCH.
>   Đảo chiều làm đổi ý nghĩa cả 3 cột `backup_history` và đổi phía bị khoá thao tác.
> - Các mâu thuẫn CAO còn lại: `MT-03` (status=3 hiển thị「エラー」nền đỏ hay「処理完了済」giống thành công —
>   spec §9.3 tự nhận người dùng KHÔNG phân biệt được), `MT-06` (2 LOA nguồn cùng copy vào 1 LOA đích —
>   3 TC gốc tự phủ định nhau, rủi ro trộn/nhân đôi dữ liệu), `MT-08` (khoá thao tác chỉ LOA đích theo spec
>   nhưng UI cảnh báo khoá cả 2 phía trong「khoảng 1 giờ」— mốc này không có căn cứ), `MT-13` (filter chứa
>   điều kiện QR / affiliate: bỏ riêng điều kiện hay bỏ cả filter — bỏ riêng làm filter LỎNG hơn ⇒ gửi sai
>   đối tượng), `MT-14` (ai tính lại 対象人数 của CSV sau copy — corpus khẳng định có job, spec không biết
>   job đó tồn tại).
> - **4 lỗi cũ chưa rõ đã fix hay chưa** — ghi chú lỗi có ở tab cũ「Backup 1.0」nhưng biến mất ở tab mới
>   「Backup (job)」mà không có bằng chứng fix: `MT-16` (action リマインド còn trỏ id bot gốc — lỗi rò rỉ
>   dữ liệu chéo bot, lặp ở 4 chỗ), `MT-17` (conversion backup sai folder), `MT-18` (友だち情報 duplicate
>   folder + mất setting giờ của info kiểu ngày), `MT-20` (folder event duplicate + không liên kết được
>   friend info mặc định). Các TC tương ứng đã đánh dấu **DỰ KIẾN FAIL**.
> - TCs **lấp được Gap** spec tự nhận: `BK-Q07` (phân trang bảng lịch sử — `MT-07`),
>   `BK-Q08` (phân quyền Staff ở tầng máy chủ — `MT-25`), `BK-Q09` (dữ liệu LOA nguồn không bị đổi),
>   `BK-Q10` (nhiều LOA nguồn → 1 LOA đích — `MT-06`).
> - **Vùng mù 2 chiều** (`MT-29`): spec §9.3 mục 4 tự nhận chưa rõ Spring Boot đọc `backup_config` hay
>   `backup_config_dung`, corpus KHÔNG có TC nào. Kho đã viết 2 TC thuần theo spec, cần Leader duyệt.
> - **Vùng mù chưa ai chạm**: copy vào LOA **đã có sẵn dữ liệu** (cộng dồn hay ghi đè?) và copy **2 lần
>   liên tiếp** cùng cặp bot (dữ liệu có nhân đôi không) — corpus chỉ giả định LOA đích trống.
>   Xem `TC-BK-345`, `TC-BK-346`.
> - **11 TC đánh dấu `DỰ KIẾN FAIL`** — chạy xong phải raise bug nếu tái hiện: `TC-BK-62` (không phân biệt
>   được thất bại với thành công) · `TC-BK-107` / `TC-BK-126` / `TC-BK-194` / `TC-BK-231` (action リマインド
>   trỏ id bot gốc) · `TC-BK-216` / `TC-BK-221` (友だち情報 duplicate folder / mất setting giờ) ·
>   `TC-BK-234` (event không liên kết được friend info mặc định) · `TC-BK-240` (message của remind không
>   copy được) · `TC-BK-244` (conversion sai folder) · `TC-BK-321` (thumbnail video nhánh dữ liệu cũ).
> - **38 TC có kết quả mong đợi do AI suy luận / bổ sung** (corpus không có, spec không ghi) — đã ghi rõ ở
>   cột `Ghi chú` là「Suy luận của AI ... cần Leader xác nhận」. Cột `Trạng thái đánh giá spec`:
>   `Đã hỏi leader` = 116 TC · `Spec không ghi` = 5 TC · `Spec ghi rõ` = 238 TC.
> - 152/359 TC đặt `Môi trường test = PRODUCTION` theo **RULE-08** (media · job nền · đăng ký richmenu lên
>   LINE · race condition · plan tính tiền · tệp xuất ra).
> - Nhóm TC nguồn **> 2 năm tuổi** đã đánh dấu CẦN VERIFY LẠI:「Backup 1.0」khối gốc (03/2023),
>   「Backup (job)」khối gốc (05/2023),「Improve backup media」(01/2024),「Backup image」(≤2024).
>   `TC-BK-357` là TC điều phối để Leader giao thành 1 đợt rà soát riêng.
> - `MT-30` — corpus TỰ TRÙNG MÃ TC: `TC-BK-034…039` tồn tại ở CẢ「[AI]UI TCs」và「[AI]API TCs」với nội dung
>   khác hẳn nhau;「[MN]Job TCs」nhảy từ 067 sang 075. Kho đã đánh số lại nên không còn trùng.
> - Đã LOẠI khỏi phạm vi (cần user xác nhận): 4 tab hạ tầng media của `TCsLine_Improve chung` ·
>   `TCsLine_ChangeBot` + `TCsLine_AddBot` · `TCsLine_MCP` · 28 dòng TC popup (popup đã bị tắt khỏi
>   phạm vi copy — xem `MT-22`).

> **FA-031 — trạng thái (2026-08-24):**
> - 398 TC gộp từ 9 tab của `TCsLine_Bill tiền_Improve2025` (tab master「Quản lý hợp đồng」1731 dòng /
>   1506 TC lá) + 12 tab của `TCsLine_Bill tiền`. Tổng corpus đọc vào ~3.400 TC lá.
> - **46/46 mâu thuẫn đang CHỜ QUYẾT ĐỊNH** — 3 mục PHẠM VI (`MT-00`, `MT-00b`, `MT-00c`) phải chốt TRƯỚC
>   vì ảnh hưởng ~250 TC: `feature-spec.md:26` ghi rõ 「**Không bao gồm: tạo hợp đồng mới**」 trong khi
>   corpus có 531 + 347 TC cho đúng luồng mua/upgrade.
> - 17 mâu thuẫn mức CAO. Nặng nhất: `MT-02` (mốc 7 ngày khi hủy chuyển khoản — cùng 1 tab viết ngược nhau,
>   rủi ro hủy hợp đồng còn hạn), `MT-04` (lịch retry bill lỗi: corpus đếm 7 ngày vs `BR-03` đếm 5 lần trải
>   ~14 ngày), `MT-06` (công thức `expired_date` với ngày 29/30/31 — bảng giá trị không suy ra được công thức,
>   chính là gốc Bug KH #26511 và #35467), `MT-11` (vào detail bằng URL + nhập thẻ lỗi + back → **XÓA HẲN**
>   hợp đồng), `MT-13` (callback UnivaPay muộn / 2 charge transfer song song — corpus liệt kê đủ 6 tổ hợp
>   nhưng **bỏ trống kết quả mong đợi**).
> - TCs **lấp được Gap `[M1]`** spec tự nhận (thiếu 4 endpoint): corpus xác nhận 8 URL màn thao tác hợp đồng
>   có thật (`change-bill-type`, `change-payment-method`, `extend-contract`, `re-contract`, `change-card`,
>   `sub-card-setting`, `detail-contract`, `.../cancel`) — xem `MT-15`.
> - **Vùng mù 2 chiều**: (a) spec có / TCs không có → màn 接続解除履歴 (SCR-BLP-04), job `RecoverUpdateInfoUnivapay`,
>   job `CheckStatusWebhook`, hiệu năng màn list (`MT-22` — kho đã viết 6 TC thuần theo spec, cần Leader duyệt);
>   (b) **cả 2 đều trống** → **coupon code** (`MT-23`): UI production có nút 「クーポンコードを入力する」và có log
>   sự kiện thật, nhưng spec `[M2]` không tìm ra bảng/endpoint và corpus KHÔNG có TC nào.
> - 8 cột DB corpus dùng để verify nhưng **db-mapping KHÔNG có** (`MT-18`): `bill_type_old`,
>   `payment_method_old`, `datetime_first_payment`, `release_date_transfer`, `bank_branch_code`,
>   `bank_account_holder_name`, `payment_histories.last_four_card`, `payment_histories.remain_day_upgrade`.
> - 97/398 TC đặt `Môi trường test = PRODUCTION` theo **RULE-08** (bill tiền · job · 3D Secure · race condition ·
>   performance). Giá plan trên dev/staging KHÁC PRODUCTION (`MT-30`).
> - Nhóm TC > 2 năm tuổi đã đánh dấu CẦN VERIFY LẠI: 「Cố định ngày bill tiền」(07/2023),
>   「Estimation」(09/2023 — giá plan đã lỗi thời), 「Logic refund」+「Refund update 1.0」(04-05/2023),
>   「Change bill tiền theo năm」+「Task nhỏ」(12/2023).
> - Đã LOẠI khỏi phạm vi (cần user xác nhận): 5 tab add bot / change bot → `spec-features/admin/bot-add-v2/`;
>   tab「Bill tiền/ phân bổ/ TOP」→ admin portal nội bộ; phần Tutorial onboarding của tab「Campaign + Tutorial」.

> **FA-009 — trạng thái (2026-08-21):**
> - 409 TC gộp từ 6 tab của `04. TCsLine_Scenario` + 7 tab lẻ của `TCsLine_Improve chung`.
> - **41/41 mâu thuẫn đang CHỜ QUYẾT ĐỊNH** — 12 mức CAO. Nặng nhất: `MT-01` (mapping `is_following` 0/2 ↔
>   `count_stop`/`count_unfinish` — 3 nguồn spec nói ngược nhau và corpus tự mâu thuẫn trong cùng 1 tab),
>   `MT-21` (`delay_type=2` lưu giờ:phút hay phút:giây — `logic-spec` sai ở 3 chỗ), `MT-40` (edit step đã gửi có
>   thêm bản ghi `scenario_step_time` không — corpus tự phủ định trong cùng 1 ô, rủi ro gửi trùng),
>   `MT-41` (job scenario và job callback ở 2 server → bộ đếm chống lặp đếm riêng), `MT-24` (copy step trùng time
>   GHI ĐÈ tên step + profile — mất dữ liệu im lặng).
> - TCs **lấp được 2 Gap** spec tự nhận: Gap #5 (quyền Staff) và Gap #6 (UI `afterScenarioId1..5` của next scenario);
>   Gap #8 (`option_add_template` link/copy) được lấp ở tầng hành vi.
> - **Giới hạn 72 giờ** của `経過時間で指定` (Feature #30571, 07/2025) và **cửa sổ 5 phút** của job quét
>   `step_message.is_new` KHÔNG có trong spec ở bất kỳ đâu (`MT-22`, `MT-04`).
> - 3 nhóm TC nguồn **> 2 năm tuổi** đã đánh dấu CẦN VERIFY LẠI: Phân quyền (11/2023), bộ đếm friend khi bot block
>   friend (12/2023 + 2024), order_number (11/2023).
> - `tag_filter_method` / `delivery_tag` / `skip_tag` (spec Gap #7) — **corpus KHÔNG có TC nào**, vẫn là vùng mù.
> - Màn 「ステップ配信設定」 (SCR-SCE-05, auto-subscribe khi kết bạn) **đã loại khỏi phạm vi** — thuộc
>   `spec-features/admin/setting-add-friend/`, cần chạy `/collect-tcs` riêng.

> **FA-015 — trạng thái (2026-08-20):**
> - 339 TC gộp từ 5 tab của `10.2 TCsLine_friend_information` + 4 tab lẻ của `TCsLine_Improve chung`
>   + `TCsLine_ModalAction` + `TCsLine_Modal Filter`.
> - **18/18 mâu thuẫn đang CHỜ QUYẾT ĐỊNH** — 4 mức CAO: `MT-01` (kiểu 画像/PDF tạo được nhưng spec
>   nói bị loại khỏi danh sách theo folder — spec tự mâu thuẫn giữa UI và query), `MT-02` (xóa trắng
>   都道府県名 có giảm 回答人数 không — spec cho d_6 không có bước giảm bộ đếm), `MT-03` (phạm vi quy tắc
>   "xóa trắng = xóa hẳn dòng" — fix #38591 chỉ đụng 1 trong ≥ 7 lối ghi), `MT-04` (cascade đổi text
>   option ở nhánh salon — corpus đang đánh **NG**).
> - TCs **lấp được 4 Gap** spec tự nhận: Gap #2 (phân quyền staff), Gap #4 (giao diện ngưỡng điểm),
>   Gap #5 (phân trang), Gap #9 (format CSV export).
> - **16 TC「RV-01…RV-16」trong corpus chỉ có tiêu đề + các bước, KHÔNG có kết quả mong đợi** — kết quả
>   mong đợi do AI viết ở tầng quan sát UI, đã ghi rõ ở cột `Ghi chú`, cần Leader xác nhận.
> - 3 nhóm TC nguồn **> 2 năm tuổi** đã đánh dấu CẦN VERIFY LẠI: filter friend info (07/2023),
>   random điểm ở modal action (11/2023), filter point & date (10/2023).
> - File `TCsLine_Detail_Friend` (FA-014 màn 友だち詳細) **đã loại khỏi phạm vi** — cần chạy `/collect-tcs` riêng.

> **FA-004 — trạng thái sau khi Leader chốt (2026-08-22):**
> - 488 TC (thêm 4 TC so với bản draft) gộp từ 7 tab của `06. TCsLine_Richmenu` + tab「Improve richmenu」của `TCsLine_Improve chung`.
> - **26/27 mâu thuẫn đã chốt** và đã áp vào TCs. Còn **1 mục chờ**: `MT-23` (BR-03 — chặn thao tác khi backup
>   đang chạy; Leader chưa điền). `TC-RM-478` chưa nên giao member chạy.
> - **4 TC MỚI** sinh ra từ quyết định: `TC-RM-199` (900 ký tự latinh — nhánh hở của MT-01),
>   `TC-RM-408` (job lỗi → status = 5, theo yêu cầu ở MT-11), `TC-RM-447` + `TC-RM-448`
>   (chặn ở tầng API, theo yêu cầu ở MT-24).
> - **7 TC đánh dấu `DỰ KIẾN FAIL`** — quyết định của Leader khác TC gốc, chạy xong phải raise bug:
>   `TC-RM-03` / `TC-RM-325` (message trùng tên), `TC-RM-89` (message sai định dạng ảnh),
>   `TC-RM-99` (🔴 PNG trong suốt thành nền trắng — Leader xác nhận là BUG THẬT trên PRODUCTION),
>   `TC-RM-197` (chặn nhập vs báo lỗi khi lưu), `TC-RM-233` (chỉ chọn action stop có lưu được không),
>   `TC-RM-294` (Step 1/2/3 có nút Save xanh lá hay không).
> - **8 TC đổi nhãn nút** từ「保存して次へ」sang「次へ」theo MT-04; **6 TC nhóm Lưu & điều hướng + Copy**
>   viết lại bỏ khái niệm "nút Save màu xanh lá" theo MT-18.
> - TCs **lấp được 2 Gap** spec tự nhận: `D-1` (`detail_click_richmenu`) và `#7` (tối đa 20 area);
>   MT-20 đóng thêm **Gap J-1** (job `HandleCheckTimeDisplayRichMenuTask` đang chạy trên PRODUCTION).
> - ⚠️ **5 nhánh Leader chưa phủ hết**, TC để `Đã hỏi leader` kèm câu hỏi: MT-01 (900 ký tự latinh vs
>   varchar(255)), MT-06 (text hướng dẫn thiếu .jpeg), MT-08 (2 message bắt buộc nhập chưa thống nhất),
>   MT-20 (hành vi job (a)/(b) + tên cột `end_time_display` vs `close_date`), MT-21 (khi nào còn thấy
>   trạng thái「アクション未設定」).
> - 🔴 **Việc phải sửa spec sau quyết định**: bỏ BR-04 + EP-32/EP-33 (MT-25) · sửa template_type 1→12 (MT-03) ·
>   bỏ INSERT ở EP-08 quick-create (MT-05) · bổ sung job xóa 90 ngày + đủ 5 giá trị status (MT-11) ·
>   bổ sung BR giới hạn switch theo plan (MT-09) · sửa ý nghĩa `show_rich_menu_action` (MT-10) ·
>   sửa `detail_click_rich_menu` → `detail_click_richmenu` (MT-26).
> - Tab「Image richmenu」đã **loại khỏi phạm vi** — thuộc FA-005 リッチメニュー画像作成, cần chạy `/collect-tcs` riêng.

> **FA-011 — trạng thái sau khi Leader chốt (2026-08-19):**
> - Spec đã được bổ sung tại `spec-features/admin/form-answer/` (MT-00 ✅). ⚠️ Còn phải cập nhật
>   `spec-features/admin/index.md` dòng 21 — FA-011 vẫn đang ghi `CHƯA` ở cả 6 cột.
> - **22/23 mâu thuẫn đã chốt** và đã áp vào TCs (đợt 2026-08-19: MT-00→MT-19; đợt 2026-08-22:
>   MT-20, MT-21, MT-22). Còn **1 mục chờ**: `MT-09` — sửa text option của item rẽ nhánh làm mất
>   setting next page (ô quyết định vẫn để trống).
> - **3 mục bắt buộc phải sửa spec** sau khi chốt — xem cột "Việc phải làm tiếp":
>   `MT-20` viết lại **BR-03** (GUI có 2 setting giới hạn độc lập, không phải 1 trường `reply_kind` 3 giá trị) ·
>   `MT-21` bổ sung **`next_page_type = 1`** vào BR-10 ·
>   `MT-22` viết lại **BR-08** + đóng **Gap #11** theo cơ chế sync batch mô tả trong 32 TC nhóm Sync.
> - **9 TC được đánh dấu `DỰ KIẾN FAIL`** — quyết định của Leader khác hiện trạng, chạy xong phải raise bug.
> - Cột `Trạng thái đánh giá spec`: `Đã hỏi leader` = TC gắn với 1 mục MT (43 TC) ·
>   `Spec không ghi` = kết quả mong đợi do AI viết, cần xác nhận (14 TC) · `Spec ghi rõ` = còn lại (424 TC).

## Đánh số & thứ tự TC

- **TC No.**: `TC-<PREFIX>-01`, `TC-<PREFIX>-02`, … (`TAG` cho FA-012, `FORM` cho FA-011, `RM` cho FA-004) — đánh số **tuần tự theo thứ tự nhóm chức năng**, không đánh lại theo mã quan điểm. Prefix khai báo ở khoá `prefix` của feature trong `build.py`.
- **Tiêu đề**: luôn bắt đầu bằng prefix `[<nhóm chức năng>]`, VD `[Tạo folder]`, `[Edit tag]`, `[Action gắn tag]`.
- **Thứ tự nhóm** (định nghĩa ở `SECTIONS_TAG` / `SECTIONS_FORM` trong [data/_common.py](data/_common.py)):

| # | Nhóm | File |
|---|---|---|
| 1-4 | Tạo folder · Sửa folder · Xóa folder · Sắp xếp folder | `tag_s1_folder.py` |
| 5 | Tạo tag (modal 新規作成 1 tag / nhiều tag · CSV一括追加 · popup trong modal Action) | `tag_s2_create.py` |
| 6-7 | Edit tag (7 field editable) · Copy tag | `tag_s3_edit.py` |
| 8-13 | Xóa tag · Sort tag · Count người gắn tag · Chuyển folder · Màn list tag · Màn tag đã xóa | `tag_s4_delete_list.py` |
| 14-16 | Action gắn tag (24 điểm) · Phân quyền · Môi trường & Legacy | `tag_s5_action.py` |

**FA-004 Rich Menu** — 27 nhóm (`SECTIONS_RICHMENU`):

| # | Nhóm | File |
|---|---|---|
| 1-4 | Folder richmenu · Sort & ẩn folder · Màn list richmenu · Tìm kiếm & sắp xếp richmenu | `rm_s1_list_folder.py` |
| 5-8 | Tạo richmenu (modal) · Step 1 Ảnh · Step 2 Layout vùng tap · Step 2 Vùng tap thủ công | `rm_s2_create_step12.py` |
| 9-14 | Step 3: Action エルメ · Action 友だち · Đổi richmenu · Stop richmenu · LINE URL scheme · Copy action giữa area | `rm_s3_action.py` |
| 15-19 | Step 4 Chi tiết · Lưu & điều hướng 4 step · Copy richmenu · Xóa & khôi phục richmenu · Preview action | `rm_s4_step4_save.py` |
| 20-23 | Setting hiển thị · Setting stop · Lịch sử hiển thị/stop · Job hiển thị/stop | `rm_s5_display_job.py` |
| 24-27 | Thống kê tap · Backup & đổi bot · Phân quyền & staff · Richmenu cũ & recover | `rm_s6_stats_env.py` |

**FA-009 ステップ配信** — 30 nhóm (`SECTIONS_SCE`):

| # | Nhóm | File |
|---|---|---|
| 1-4 | Folder scenario · Sắp xếp folder · Màn list scenario · Tìm kiếm & phân trang list | `sce_s1_folder_list.py` |
| 5-9 | Tạo · Sửa · Copy · Xóa scenario · Chuyển folder | `sce_s1_folder_list.py` |
| 10-12 | Màn list step & phân trang · Filter phân nhánh 配信対象 · 配信タイミング thêm & sửa | `sce_s2_step_filter.py` |
| 13-19 | Tên quản lý step · Message trong step · Template từ thư viện · Action エルメ · Profile người gửi · Copy message & action · 一括操作 | `sce_s3_message_action.py` |
| 20-21 | Preview & send test step · Send test 一括テスト | `sce_s4_preview_test.py` |
| 22-24 | Next scenario · Bộ đếm friend · Màn list friend theo scenario | `sce_s5_next_count.py` |
| 25-30 | Job gửi step & is_last_step · Job khi edit step đang chạy · Chống lặp vô hạn · Trùng line_user · Backup & đổi bot · Phân quyền & môi trường | `sce_s6_job_env.py` |

**FA-011 Form** — 37 nhóm (`SECTIONS_FORM`):

| # | Nhóm | File |
|---|---|---|
| 1-7 | Màn list form · Folder · Sort&search · Tạo form · Copy form · Xóa&khôi phục · Public&URL | `form_s1_list.py` |
| 8-18 | Màn edit form · Item hiển thị · Item câu hỏi chung · ngày giờ · radio&dropdown · checkbox · upload file · remind · chẩn đoán · thường dùng · Liên kết friend info&tag | `form_s2_items.py` |
| 19-27 | Form rẽ nhánh (page · setting rẽ nhánh) · Setting chung của page · action · remind · chẩn đoán · Setting chung của form · Countdown · Preview | `form_s3_page_setting.py` |
| 28-31 | Màn kết quả trả lời · Export CSV · Liên kết Google Sheet · Sync Google Sheet & job | `form_s4_result_sync.py` |
| 32-37 | LINE user (mở form · nhập&submit) · Backup&Recover · Form cũ&tương thích · Giới hạn&hiệu năng · Phân quyền&môi trường | `form_s5_lineuser.py` |

**FA-033 データコピー (Backup)** — 28 nhóm (`SECTIONS_BK`):

| # | Nhóm | File |
|---|---|---|
| 1-8 | Màn データコピー · Mã copy & phát hành lại · Xác nhận mã & card · Modal xác nhận & bắt đầu · Màn processing & polling · Modal hoàn tất · Tab lịch sử · Phân quyền & plan | `bk_s1_screen.py` |
| 9-10 | Job BackupBotTask & state machine · Backup đồng thời & liên tiếp | `bk_s2_job.py` |
| 11-15 | Copy 自動応答 · リッチメニュー · ステップ配信 · テンプレート · フォーム作成 | `bk_s3_copy_msg.py` |
| 16-21 | Copy タグ · 友だち情報 · イベント予約&リマインド · コンバージョン・URL・対応ステータス · 友だち追加時設定 · アクションスケジュール | `bk_s4_copy_data.py` |
| 22-24 | Copy フィルタ · クロス分析 · CSV管理 | `bk_s5_copy_analytics.py` |
| 25-28 | Media & ảnh khi copy · Dữ liệu KHÔNG được copy · Hồi quy sau copy · Môi trường & Legacy | `bk_s6_media_env.py` |

**FA-020 サロン・面談予約 (Đặt lịch salon)** — 52 nhóm (`SECTIONS_SLN`):

| # | Nhóm | File |
|---|---|---|
| 1-3 | Màn list calendar · Tạo calendar wizard · Giới hạn theo plan | `sln_s1_list_create.py` |
| 4-15 | Tab 本日/新着 · Calendar ngày/tuần/tháng/list · Modal filter · リクエスト一括操作 · Admin thêm booking · Modal lý do · Detail booking · Booking đã xóa · Hoàn tiền | `sln_s2_booking_mgmt.py` |
| 16-19 | Ca làm việc: thêm&ghi đè · sửa&xóa · qua ngày&biên 00:00 · CSV | `sln_s3_shift.py` |
| 20-24 | コース (list&menu · CRUD) · スタッフ · Hiển thị コース・スタッフ · スタッフ自動割り当て | `sln_s4_course_staff.py` |
| 25-38 | 受付上限 · 前後の空き時間 · メッセージ&アクション · 開始・締切 · 1人あたりの上限 · 質問項目 · リマインド (cài đặt & job) · 空き枠通知 · トップ・店舗情報・利用規約 · システムワード&表示設定 · 予約ページの非表示 · 予約システムの削除 | `sln_s5_setting.py` |
| 39-40 | Googleカレンダー連携 · Googleスプレッドシート連携 | `sln_s6_google.py` |
| 41-43 | 決済連携 cài đặt · 決済 thẻ&3D Secure · 現地決済 | `sln_s7_payment.py` |
| 44-52 | LINE user (entry · chọn コース/スタッフ · chọn slot · form&xác nhận · lịch sử&copy · hủy) · Đồng thời&verify API · Job nền&monitor · App mobile · Phân quyền&môi trường · Dữ liệu cũ&hồi quy | `sln_s8_lineuser.py` |

Thêm nhóm mới hoặc đổi thứ tự: sửa `SECTIONS_TAG` / `SECTIONS_FORM` / `SECTIONS_RICHMENU` / `SECTIONS_SCE` /
`SECTIONS_BK` / `SECTIONS_SLN` trong `data/_common.py`.

> ⚠️ **Thứ tự nhóm khi tên nhóm trùng giữa các feature**: mặc định `build()` sắp xếp theo bảng thứ tự GỘP của tất cả
> feature, nên nhóm nào trùng tên với feature khai báo trước (vd `Sắp xếp folder` có ở cả TAG, FRI và SCE) sẽ bị kéo
> về vị trí của lần khai báo đầu tiên → **sai thứ tự**. Feature khai báo thêm khoá `"sections": "SECTIONS_<X>"` trong
> `FEATURES` sẽ dùng thứ tự nhóm RIÊNG của mình. Hiện **FA-009**, **FA-001** và **FA-033** khai báo khoá này;
> **FA-015 đang bị lệch thứ tự
> nhóm** vì lý do trên (4 nhóm folder bị kéo lên đầu, `Export CSV` và `Phân quyền & môi trường` nhảy lên vị trí 5-6)
> — chưa sửa vì sẽ đánh số lại toàn bộ `TC-FRI-xx` mà Leader đang review.

## Nguyên tắc tách TC

**Mỗi kết quả mong đợi khác nhau = 1 TC riêng.**

Giữ chung 1 TC khi:
- Nhiều input khác nhau nhưng **cùng 1 kết quả mong đợi** (VD: tên latinh / tiếng Nhật full-width / half-width đều lưu thành công)
- Các bước là **1 chuỗi thao tác liên tiếp** không tách rời được (race condition, `FUNC-SEQ-*`)
- Verify **3 tầng** (DB + màn hình + output) của **cùng 1 hành động** — đây là RULE-07, không phải nhiều state

Ví dụ đã áp dụng:
- Cột 人数制限 có 3 state hiển thị khác nhau → tách thành 3 TC (`TC-UIFIELD001-03/-04/-05`)
- Ma trận 14 điểm gắn tag có kết quả **khác nhau** (8 điểm có action, 6 điểm không) → tách 14 TC
- Ma trận 14 điểm gắn tag khi tag đã đầy limit đều **cùng** kết quả (không gắn được) → giữ 1 TC

## Việc còn phải làm sau khi Leader chốt mâu thuẫn

Các quyết định ngày 2026-08-19 kéo theo việc **sửa spec** — xem cột "Việc phải làm tiếp" ở tab `_Mâu thuẫn cần quyết`:

| Mục | Việc |
|---|---|
| MT-01 | Sửa §SCR-TAG-02 + Validation Rules: EP-13 skip tên trùng, KHÔNG reject batch |
| MT-02 | Sửa pseudo-code EP-13 thêm scope `bot_id` cho khớp BR-01 |
| MT-04 | Bổ sung §5: folder name bắt buộc, max 15 ký tự, không unique |
| MT-05 | Bổ sung: chế độ `copy_tag` validate limit theo count = 0 |
| MT-03 | Bổ sung field #13/#17 + BR-09: 3 lối vào có 3 cơ chế khác nhau (báo lỗi / tự cắt / chặn nhập) — là cố ý |
| MT-06 | Sửa **cả EP-10 và EP-15** trong api-spec/logic-spec: mặc định 15 → 100 |
| MT-08 | Bổ sung 3 BR: trim space, unique không phân biệt hoa/thường, min số limit |
| MT-09 | Bổ sung bảng ngoại lệ vào BR-07 (6 điểm không gửi action) |
| MT-10 | Bổ sung hành vi tag đã xoá trong form answer (FA-012 + spec Form Answer) |
| MT-11 | Đóng Gap G-01, nâng confidence BR-08, bổ sung §7 job auto-purge |
| MT-12 | Đóng Gap G-05, ghi rõ default `is_2th_apply` = 0 ở field #19 |
| MT-13 | Ghi rõ EP-31 không sendAction + bổ sung option action ở spec Quản lý CSV |

> **FA-019 — trạng thái (2026-08-26):**
> - **632 TC** gộp từ **16 tab** của `11.2 TCsLine_LessonCalendar` + tab「add link salon và lesson」của
>   `TCsLine_Improve chung`. Corpus đọc vào **3.172 TC lá** / 4.480 dòng. Tab lớn nhất là
>   「Setting calendar」(1.610 dòng, 1.130 TC lá, 23 cột ticket, 05/2024 → 05/2026).
> - **22 TC cuối (TC-LSN-611…632) là TC LẤP GAP do AI viết**, KHÔNG có trong corpus — bổ sung cho
>   20 quan điểm test chưa được phủ. Phủ **77/80 quan điểm** của `checklist-lme.md`; 3 quan điểm còn
>   lại không áp dụng: `INTG-CAL-001` (FA-019 **KHÔNG có** tích hợp Google Calendar — spec §1.2),
>   `PAY-CONFIRM-001` (không có bước tạm tính), `UI-004` (mức Thấp, chờ Leader quyết).
> - 🔴 **Phải chốt TRƯỚC 4 mâu thuẫn nền tảng**: `MT-11` (tab「Quản lý calendar」hay「_new」là nguồn
>   sự thật — 2 tab song song, 12 điểm kết quả trái ngược), `MT-63` (6 lỗ hổng **Nghiêm trọng** của
>   spec **chưa từng có TC nào**), `MT-15` (import CSV ngày quá khứ: bỏ qua im lặng hay báo lỗi),
>   `MT-05` (giới hạn calendar theo gói lệch spec ở 3 gói).
> - 65 mâu thuẫn: **21 mức CAO** · 27 TRUNG BÌNH · 17 THẤP. Trong đó **14 mâu thuẫn là TC gốc TỰ
>   MÂU THUẪN hoặc BỎ TRỐNG kết quả mong đợi** (MT-02/03/08/13/17/21/24/27/28/30/31/32/34/57).
> - **11 TC đánh dấu DỰ KIẾN FAIL** — chạy xong phải raise bug nếu tái hiện: 6 TC verify API của
>   `MT-63` · `TC` modal 削除済み予約 (B-2 + B-1 đảo handler) · `updateReception` trả success giả (B-4) ·
>   `NEW-10` arbiter bỏ qua ADMIN_BOOK · hạ gói pro→free vẫn thu tiền (BR-P21) ·
>   rò rỉ token/mã xóa trong response (A-05/A-07).
> - **312/632 TC đặt `Môi trường test = PRODUCTION`** theo **RULE-08** (bill tiền · media · job nền ·
>   race condition · webhook · email · output LINE app).
> - Cột `Trạng thái đánh giá spec`: `Spec ghi rõ` = 550 · `Spec không ghi` = 51 · `Đã hỏi leader` = 31.
> - **Nguồn đã LOẠI, cần user xác nhận**: toàn bộ file `TCsLine_Booking Calendar` (hệ 予約管理 thế hệ
>   cũ, đã gỡ khỏi tool 07/2025) và tab「18. Lesson」của `TCsLine_MCP` (test tầng MCP tool, đề xuất
>   tách sheet riêng『MCP』).
