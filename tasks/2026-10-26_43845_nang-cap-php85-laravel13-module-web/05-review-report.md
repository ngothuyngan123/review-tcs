<!-- Report review TC task #43845 (Studio #507). Do quy mô 1537 TC, review CHIA 12 BATCH (xem scratchpad REVIEW-PLAN-43845.md). Mỗi batch là 1 khối `## BATCH Bx` độc lập, có đủ §0–§8. -->

# 05 — Review report: Nâng cấp PHP 8.5 + Laravel 13 (#43845 / Studio #507)

---

# BATCH B3b — Richmenu + Popup + QR/Landing + Media

## 0. Nguồn TC
- **Nguồn đã dùng**: MCP LME TEST STUDIO — task_id=507, ticket 43845 (subset B3b lọc theo `screen`/`viewpoint`: Richmenu·Popup·QR/Landing·Media).
- **Tổng số TC review**: 142 (Media 25 · QR/Landing 45 · Richmenu 40 · Popup 32).

## 1. Coverage — dev-impact + diff code

- **dev-impact: 3/4 nhóm ảnh hưởng B3b có TC — CHƯA ĐỦ.** F10 (Intervention Image v3 — ảnh/video/音声/image map/rich menu image/QR poster) có nhiều TC Normal+Abnormal+Boundary; F6/T4 (LINE SDK → richmenu tạo/gán/gỡ/xoá) có TC. **Nhưng** cả nhóm media/richmenu-image **chưa có TC nào chạy trên production** (RULE-08) và phần lớn TC media ở trạng thái `error`/`skip` (xem §5) → coverage **chưa được xác nhận**.
- **diff code: CHƯA ĐỦ.** Các `requirement_keys` của diff (REQ-T14 QR/media, REQ-T15 Intervention v3, REQ-T16/T22 richmenu, REQ-T23 popup) đều có TC. **Thiếu 1 điểm‑vào của diff**: `qr-landing/feature-spec.md` (dòng 53 + SCR-QRL-36) khai 4 trang LINE-user gồm `/open-external-browser/{type}/{id}` và `/landing-qr/{liffId}?uLand={code}&device=pc` — bộ TC **không có ô "trình duyệt ngoài / PC"** (xem §2).

| Mã | Chiều | Vùng ảnh hưởng | TC hiện có | Status | Ghi chú |
|---|---|---|---|---|---|
| G1 | diff code | Điểm‑vào QR landing: **trình duyệt ngoài** (`/open-external-browser/`) + **PC** (`device=pc`) — kết bạn CHƯA/ĐÃ bạn | NEW-2/3/4/5/653 chỉ quét QR trong **app LINE** (in-app LIFF); NEW-564/565/566 mở trên điện thoại (in-app) | **GAP** | LIFF-ENTRY-001 (Cao). Ô "trình duyệt ngoài" KHÔNG được coi là cover bởi TC in-app (bài học #42437). → §7 G1 |
| G2 | diff code | Kết bạn QR landing **KHÔNG qua LIFF** (spec dòng 305: không có bản ghi `action=1` trong 24h → rơi về `add_friend_setting` chung, bỏ nhánh QR) | NEW-928 chỉ cover kết bạn **qua** LIFF (in-app) | **GAP** | Nhánh fallback của chính diff QR — → §7 G2 |
| R1 | diff code | Media/ảnh/QR/richmenu-image chạy **production** (p.lmes.jp / media server thật) | NEW-888 (ENV-003, prod) = `skip` env=dev; mọi TC media khác env=dev/local | **RISK** | RULE-08: không kết luận media/domain từ dev/local. Không đẻ TC mới — TC đã có, cần **chạy lại trên prd** (§5) |
| G5 | diff code | Rich menu Step1 **PNG nền trong suốt (alpha)** — Intervention v3 đổi cách flatten alpha nền | NEW-172 chỉ test PNG mờ → JPEG (không phải nền trong suốt); kho có TC-RM-99 | **GAP** | F10 Intervention v3. Alpha flatten khác giữa v2/v3; oracle = production (bug #31953, nền trắng, giữ như cũ theo F-6). → **§8-5 (không đẻ TC — gỡ TC-MEDIAIMG001-01 2026-10-27; #31953 lỗi có sẵn giữ theo F-6)** |
| G6 | diff code | Rich menu Step1 **ảnh sai định dạng / không phải ảnh** (.gif/.webp/.svg/file đổi đuôi/file hỏng) | NEW-174 chỉ test sai kích thước + >10MB; kho có TC-RM-88/89 | **GAP** | Diff chạm `app/Rules/Base64ImageType.php`·`Base64IsImage.php`·`Base64ImageSize.php` (A4 validation). → §7 G6 |
| G7 | diff code | **URL分析 tỉ lệ click khi 0 lượt gửi / 0 click / kỳ rỗng** (A3 number_format + A4 chia 0) | NEW-289/461/463 chỉ test URL CÓ dữ liệu; không có TC cho mẫu số = 0 / kỳ không click | **GAP** | Feature cross-cutting (diff `URLController` + `DetailUrlClick`); rate = click/配信 → PHP8 chia 0 / float→int. → §7 G7 |

**Kết luận §1**: 5 GAP (G1, G2, G5, G6, G7) · 1 RISK (R1, do môi trường thực thi). Mọi nhóm đều có TC thiết kế, nhưng coverage **chưa được xác nhận bằng exec** (27% pass — §5). _(G5/G6 bổ sung 2026-10-27 khi rà riêng cụm Rich menu theo 10 maincase — xem §7.)_

> **Đã áp thêm [framework/php-upgrade-checklist.md](../../framework/php-upgrade-checklist.md)** (task nâng version Laravel 5.5→13 / PHP 7.2→8.5). Kết quả rải vào §2 (A1 sort · lib), §5 (C APP_KEY · 3 surface), §8. Các mục A2/A4/A5 đã cover tốt trong B3b (NEW-291 date JST · NEW-799/1318/1330 null/id không 500 · NEW-964 encoding JP · NEW-1186 emoji) — không ghi ra.

## 2. Thiếu so với quan điểm test

**Kết luận**: quét theo màn (richmenu / qr-landing / popup / template-media) — thiếu đúng nhóm **điểm‑vào LINE user** của QR landing.

| Mã | Quan điểm | Ưu tiên | Thiếu gì | Severity |
|---|---|---|---|---|
| Q1 | `LIFF-ENTRY-001` | **Cao** | Ma trận điểm‑vào QR landing chỉ có ô ① in-app LINE. Thiếu ô ② **trình duyệt ngoài** (mở URL `/landing-qr?uLand=` / `/open-external-browser/` bằng Chrome/Safari), ô ④ **PC** (`device=pc`); và trục **kết bạn CHƯA/ĐÃ/đã chặn** chưa bung cho từng ô. Spec `qr-landing` dòng 53 + SCR-QRL-36 khai đủ các trang này | `[BLOCKER]` |
| Q2 | `MSG-*` / media trên LINE thật (RULE-06) | Cao | Nhiều TC media (NEW-7/10/163/172…) có bước "gửi tới user LINE test" nhưng exec=`skip`/`error` → chưa chứng minh output cuối trên LINE. Không thiếu *thiết kế* TC, thiếu *bằng chứng thực thi* → gộp vào §5 RULE-08 | (→ §5) |
| Q3 | `LIST-001` + **A1 (PHP8 sort STABLE)** | Trung bình → Cao | A1 của checklist upgrade: PHP8 đổi `sort` thành **stable**. Chỉ NEW-31 (drag-sort 並び替え tag/folder) khẳng định thứ tự; **thứ tự mặc định của list richmenu / QR action / popup khi nhiều phần tử cùng `sort_position`/khoá** chưa có TC so với bản cũ. Đây là điểm "dễ sai âm thầm" #1 theo Leader | `[MAJOR]` → §7 Q3 |
| Q4 | `FUNC-002` + **A4 (PHP8 null/TypeError)** | **Cao** | Tạo rich menu/folder với **input rỗng/null** (empty 管理名 · chưa upload ảnh · folder name rỗng/toàn space) → không có TC verify validate + không-500. Kho có TC-RM-67/107/05/09; bộ Studio richmenu KHÔNG pickup nhánh này (chỉ NEW-456 cover empty-time của lịch hiển thị) | `[MAJOR]` → §7 Q4 |

> Các viewpoint Studio lạ (`FUNC-RANDOM-001`, `API-ERROR-001`, `REG-SHARED-001`, `TOOL-KNOW-002`, `TOOL-OLDREC-001`, `RULE-TOOL-029`, `STATE-CLEAN-001`, `DATA-BACKUP-001`…) không có trong `checklist-lme.md` → không map coverage, nhưng nội dung TC đọc được vẫn đối chiếu theo màn ở trên (không liệt kê thành issue).

## 3. TC trùng lặp

Đã rà 142 TC. Cụm **popup đồng ý điều khoản 「利用規約」** (NEW-953…966, 954, 957 — 14 TC) có quan hệ tập con:

| Nhóm trùng | TC giữ lại | TC đề nghị gộp/xóa | Loại | 4 yếu tố trùng | Severity |
|---|---|---|---|---|---|
| Tiêu đề popup 利用規約 | NEW-964 (kiểm Title+Checkbox+Button+no-banner/tab) | NEW-961 (chỉ kiểm Title) | `DUP-SUBSET` | `I18N/FUNC` × Normal × popup 利用規約 × tiền đề "popup đang hiện" → cùng kiểm tiêu đề | `[MINOR]` |
| Nút enable sau tick | NEW-966 (tick→bấm→đóng, full flow) | NEW-965 (chỉ kiểm nút disabled→enable) | `DUP-SUBSET` | cùng check "nút chỉ bấm được sau khi tick" | `[MINOR]` |

Các TC consent còn lại (NEW-957 đa trình duyệt · NEW-954 đa layout · NEW-959/960 phạm vi chặn · NEW-962 nội dung · NEW-963 cuộn · NEW-958 lưu server-side · NEW-956 iframe) là **atomic khác quan điểm** — không đề nghị gộp. **Không tự xóa** — human quyết trên Studio (`testcase_delete`).

## 4. Mâu thuẫn trong TCs

| Mã | Chỗ A (TC) | Chỗ B (chuẩn) | Mâu thuẫn | 2 khả năng | Ai chốt |
|---|---|---|---|---|---|
| `CONF-SPEC` | NEW-172 (L801): richmenu ảnh > 1MB **sau lưu vẫn có thể > 1MB** (quality 80, "giữ như production PB-T15-1") | `rich-menu/feature-spec.md` **BR-07** (L115/335): "LINE API yêu cầu < 1MB → nén quality −5%/lần đến < 1MB hoặc quality < 50%" | TC chấp nhận file > 1MB; spec BR-07 nói phải ép < 1MB | (A) TC đúng — BR-07 chỉ mô tả nhánh cũ `UserController` (≤1MB q90), nhánh V2 `RichMenuService` q80 không ép < 1MB như production ⇒ **spec cần ghi rõ 2 nhánh**; (B) TC sai — phải ép < 1MB | Dev + Leader |

**CONF-TC**: không phát hiện 2 TC cùng check nhưng expected loại trừ nhau (các điểm chưa chốt của consent popup đưa xuống §8, không phải mâu thuẫn TC-vs-TC).
**CONF-KHO**: phần lớn B3b là TC **pickup trực tiếp từ kho** (PO-*, RM-*, LA-*, SN-*, IRM-*, BA-*, AFS-*…) nên nhất quán với kho theo thiết kế; đã rà `kho-tcs/fa004-richmenu` + `fa010-template` cho nhóm richmenu/media — không phát hiện expected mâu thuẫn kho.
**CONF-IGNORE**: không có. `ignore-features.md` chỉ có IG-01 (Booking Manager cũ `カレンダー予約`) — không thuộc B3b.

## 5. Issues khác

| # | Severity | TC / phạm vi | Vấn đề | Đề xuất |
|---|---|---|---|---|
| 1 | `[BLOCKER]` | Toàn batch B3b | **27% pass thật** (39/142: pass 39 · fail 6 · error 16 · skip 77 · chưa chạy 4). 73% TC **chưa có kết luận test** → coverage media/QR/richmenu/popup *thiết kế có nhưng chưa xác nhận*. Phần lớn `skip` do môi trường runner không có ffmpeg/Dropbox/Google/thiết bị LINE thật/prd (F-14) | Chạy lại batch này trên **QA PHP 8.5 có đủ dịch vụ thật** trước khi kết luận; coi mọi "ĐỦ" ở §1 là `RISK` cho tới khi có pass |
| 2 | `[BLOCKER]` | NEW-832 (Media, `fail`, **bug=[]**) | TC `fail` nhưng **chưa raise ticket bug** (sửa/sao chép/gửi thử template âm thanh mp3) | Raise ticket bug hoặc xác nhận với Dev/QA trước khi review tiếp |
| 3 | `[MAJOR] RULE-08 / ENV-003` | Toàn nhóm media + richmenu-image + QR (env `dev`=123, `local`=15, **prd=0**) | Task chạm **media / domain / ảnh** mà 0 TC chạy production. NEW-888 (TC prod duy nhất) đang `skip` env=dev | Scope `env_scope` phải chứa `prd` và **chạy thật trên prd** cho: template ảnh/video/音声, image map, rich menu image, QR poster, media server `p.lmes.jp` |
| 4 | `[MAJOR]` | 8 TC `error` **bug=[]**: NEW-658, NEW-659, NEW-774, NEW-1215, NEW-1216, NEW-1217, NEW-1218, NEW-1219 | Đang `error` (runner không chạy xong), chưa có kết luận, chưa raise ticket. NEW-1215–1219 là hồi quy modal điều kiện lọc richmenu (#39263) — cần phân biệt "error do môi trường" vs "lỗi thật" | Triage từng TC: nếu error do thiếu service → ghi skipReason; nếu lỗi thật → raise ticket |
| 5 | `[MINOR]` | NEW-1518, NEW-1528, NEW-1529, NEW-1530 (Richmenu) | 4 TC **thiếu mã quan điểm** (`viewpoint`=None) và chưa chạy (`exec`=None) | Gán mã quan điểm (`FUNC-*`/`REG-SHARED-001`/`LIFF-ENTRY`…) để map được coverage |
| 6 | `[MAJOR]` (cross-ref B7) | Toàn bộ richmenu-push + QR LIFF + Google-sheet-link của B3b | **C — APP_KEY / mã hoá (checklist upgrade)**: richmenu đẩy lên LINE (NEW-95/311/312), xoá richmenu phía LINE (NEW-251), kết bạn qua QR LIFF, liên kết Google Sheet (NEW-1293/1295/1301) **đều phụ thuộc giải mã `channel_access_token` / Google token cũ** trên bản mới. **Không có TC B3b nào khẳng định token mã hoá cũ giải mã được** — nó bị coi là tiền đề. Nếu APP_KEY/encryption lệch → mọi thao tác LINE-facing fail âm thầm (giải thích luôn vì sao nhiều TC richmenu/QR không chạy nổi) | TC "token mã hoá cũ giải mã được sau deploy" thuộc **B7 (Auth T10)** — khi review B7 phải có; ở B3b ghi phụ thuộc + **test NGAY sau deploy** |
| 7 | `[NIT]` | Richmenu / QR Code Action trên **app LME (mobile-app)** | **3-surface (checklist upgrade)**: B3b cover web + LINE-user, nhưng chưa thấy TC quản lý richmenu / QR trên **app LME**. Media có (NEW-171 App L Message gửi ảnh) | Xác nhận với Leader app LME có màn richmenu/QR không; có thì bổ sung surface `mobile-app` |

Chất lượng từng TC (nội dung, atomic, dữ liệu): bộ TC viết **rất chi tiết, tự đầy đủ** (tiền đề + steps + data + expected rõ, có oracle = production/base commit). Không phát hiện TC mơ hồ cần flag.

## 6. TCs thừa / ngoài phạm vi task

Đã rà 142 TC — **không có TC nào ngoài phạm vi #43845**. Lưu ý 1 nhóm cần Leader xác nhận quy thuộc:
- Cụm **popup 利用規約 (consent)** 14 TC (NEW-953…966): là feature gộp từ base `787782ba56`, `header.blade.php` bị chạm trong diff → **regression hợp lệ**, giữ lại. Nếu Leader xác định consent popup thuộc ticket base riêng (không phải mảng media/popup của #43845) thì chuyển sang bộ regression chung — nhưng theo diff hiện tại **không flag là thừa**.

## 7. TCs đề xuất bổ sung (14)

Đã đối chiếu 142 TC ở BƯỚC 0 + `kho-tcs/fa004-richmenu` + spec `qr-landing/feature-spec.md` + checklist nâng version (A/B/C) — không TC đề xuất nào trùng (kho chưa có FA QR/landing riêng; đối chiếu theo spec).

> **Bổ sung 2026-10-27 — rà QR Code Action theo 8 maincase** (đối chiếu 55 TC `[ACTION]` + 2 `[ADDFRIEND-QR]` Studio). 6/8 maincase ĐỦ. 3 ô trống đẻ thêm 4 TC: **MC4 friend filter** (G3) · **MC5 button-tin** (mở rộng G1/Q1) · **MC8 JP 管理名 + null field** (G4). Minor chỉ ghi chú cho Leader, không đẻ TC: MC3 action = シナリオ/step trong chuỗi · MC7 drag-reorder QR/folder (BR-41/42) · MC1 free-plan 3 QR limit (BR-04/05, qua compat đếm F13) — Leader cân nhắc có cần không.

> **Bổ sung 2026-10-27 (bis) — rà riêng cụm Rich menu (FA-004) theo 10 maincase** (đối chiếu 73 TC rich-menu-cluster Studio + kho `fa004-richmenu` 488 TC). 7/10 maincase ĐỦ hoặc RISK-do-môi-trường (5 Lịch hiển thị/dừng · 7 List/copy/xoá · 8 Thống kê tap đã đủ nhờ NEW-1530; 1/3/4/10 RISK vì exec `error`/`skip` + 0 prd — không đẻ TC, nằm ở §5-RULE-08). **2 maincase còn thiếu TC** so với kho → 2 TC bên dưới: **G6** ảnh sai định dạng/non-image (maincase 2, diff `Base64Image*`) · **Q4** input rỗng/null (maincase 9, A4), đều có bản kho (TC-RM-88-89 / 67-107-05) → dẫn chiếu ID, không trùng bộ BƯỚC 0. ⚠️ **G5 (PNG nền trong suốt) — gỡ TC 2026-10-27 theo yêu cầu Leader**: #31953 là lỗi có sẵn giữ theo F-6, chỉ hỏi Leader ở §8-5 (không đẻ TC).

> **Bổ sung 2026-10-27 (ter) — rà riêng Popup (ポップアップ /basic/popup-manager, KHÁC popup 利用規約 consent) theo 6 maincase** (NEW-580/623/624/625/626/713/774/775/1199/1200/1205/1206/1208). 4/6 ĐỦ: MC1 CRUD (624/713/580/774/1206/625) · MC2 upload ảnh resize+EXIF (1199 ngang 2048×1024 · 1208 dọc 2048×10000→419×2048, preview admin vs site thật) · MC5 list/sort (580/623 + **TC-LIST001-01** đã phủ popup A1) + copy/xoá (774/1206/580) · MC6 hiển thị với user (626 site thử · 1208 site thật). 2 ô trống → 2 TC: **MC7** A5 JP/emoji/HTML encoding 管理名+text (624 chỉ dùng tên JP; A4 đã có 625) · **MC3** kỳ hiển thị theo 開始/終了日時 A2 — bộ Studio chỉ có "**sau N giây**" (624/626), KHÔNG có TC kỳ-theo-ngày; `spec-features` không có spec popup → **conditional, flag Leader xác nhận feature** (§8).

| ID | Nhóm | Mã quan điểm | Màn hình/chức năng | Loại case | Chạy | Phạm vi ENV | Surface | Tên case | Tiền điều kiện | Các bước thực hiện | Dữ liệu nhập | Kết quả mong đợi | Kết quả thực thi | Ghi chú |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TC-LIFFENTRY001-01 | UI | LIFF-ENTRY-001 | QR Code Action 「QRコードアクション」: mở landing bằng **trình duyệt ngoài** (CHƯA kết bạn) | Normal | manual | dev, local, prd, staging | line-friend | Mở URL QR landing bằng Chrome/Safari ngoài app LINE, tài khoản LINE CHƯA là bạn bot | Bot test gói trả phí có LIFF, 1 QR Code Action `B3b-EXT` đang bật (action gắn tag `B3b-EXT-TAG` + 1 tin chào). Có URL landing dạng `https://<domain>/landing-qr/<liffId>?uLand=<code>`. Tài khoản LINE test F01 CHƯA kết bạn bot. Điện thoại có trình duyệt ngoài + app LINE | 1. Trên điện thoại mở **trình duyệt ngoài** (Chrome/Safari), dán URL landing của `B3b-EXT`, Enter. 2. Quan sát redirect: trang chuyển tới màn kết bạn LINE của bot. 3. Bấm thêm bạn F01. 4. Trên web mở 「友だちリスト」 → chi tiết F01, tab 「タグ管理」; mở 「詳細データ」 của `B3b-EXT` | URL landing `/landing-qr/<liffId>?uLand=<code>`; F01 chưa kết bạn | Trình duyệt ngoài mở landing không 404/500; vì CHƯA bạn → redirect sang màn thêm bạn của bot (giống in-app). Sau khi F01 kết bạn: tag `B3b-EXT-TAG` được gắn, F01 nhận tin chào, 「友だち追加数」 của `B3b-EXT` tăng 1. KHÔNG mất action do vào từ trình duyệt ngoài thay vì in-app | | Lấp G1/Q1 · LIFF-ENTRY ô ② trình duyệt ngoài (bài học #42437) · manual vì cần app LINE thật + trình duyệt ngoài · Đánh giá spec: Spec ghi rõ (qr-landing SCR-QRL-36 `/open-external-browser`, device=pc) |
| TC-LIFFENTRY001-02 | UI | LIFF-ENTRY-001 | QR Code Action: mở landing bằng **trình duyệt ngoài / PC** (ĐÃ kết bạn) | Abnormal | manual | dev, local, prd, staging | line-friend | Mở URL landing bằng trình duyệt ngoài và trên PC khi tài khoản ĐÃ là bạn — hành động chỉ-cho-bạn-mới không chạy lại | QR `B3b-EXT` cấu hình 稼働対象 = `新規友だちのみ`. Tài khoản F02 ĐÃ là bạn bot. Có cả trình duyệt ngoài trên điện thoại và trình duyệt trên PC | 1. Điện thoại: mở URL landing bằng trình duyệt ngoài bằng phiên F02 đã đăng nhập LINE. 2. PC: mở `…/landing-qr/<liffId>?uLand=<code>&device=pc`. 3. Mỗi lần ghi lại trang hiển thị + mã HTTP. 4. Trên web mở 「詳細データ」 đối chiếu số lượt | URL landing + `device=pc`; F02 đã là bạn | Không 404/500 ở cả 2 cách mở. Vì `新規友だちのみ` và F02 đã là bạn → action gắn tag/tin chào **không chạy lại** (giống production); 「URL読み込み人数」 có tăng nhưng 「アクション稼働人数」 không tăng cho F02. Trang PC hiển thị đúng landing/poster | | Lấp G1/Q1 · ô ② trình duyệt ngoài + ô ④ PC × đã-bạn · manual vì cần LINE thật · Đánh giá spec: Spec ghi rõ (qr-landing BR-02/entry pages) |
| TC-LIFFENTRY001-03 | UI | LIFF-ENTRY-001 | QR Code Action: kết bạn **KHÔNG qua LIFF** vẫn nhận add_friend_setting chung | Boundary | manual | dev, local, prd, staging | line-friend | Kết bạn bot bằng cách tìm ID / QR hệ thống (không đi qua landing LIFF) trong 24h | Bot có QR landing `B3b-EXT` + có cấu hình 「あいさつメッセージ」 chung của bot. Tài khoản F03 chưa kết bạn, kết bạn bằng cách **không** mở landing (search LINE ID / QR add-friend của bot) | 1. F03 kết bạn bot qua search ID / QR thêm bạn hệ thống (không mở landing). 2. Trên web mở chi tiết F03 + message hệ thống kết bạn. 3. Kiểm F03 có bị gán tag/tin của `B3b-EXT` không | F03 kết bạn không qua landing | Theo spec qr-landing (dòng 305): không có bản ghi `action=1` trong 24h → **bỏ nhánh QR**, F03 nhận `add_friend_setting` chung của bot (tin chào chung), KHÔNG gán tag/action riêng của `B3b-EXT`; message hệ thống không ghi tên QR landing | | Lấp G2 · regression nhánh fallback của diff QR · dẫn từ qr-landing feature-spec dòng 305 · manual vì cần LINE thật · Đánh giá spec: Spec ghi rõ |
| TC-LIST001-01 | UI | LIST-001 | Danh sách Richmenu / QR action / Popup: thứ tự hiển thị khi nhiều phần tử cùng khoá sort | Normal | auto | dev, local, prd, staging | web | Thứ tự list 3 màn giống hệt bản cũ dù PHP8 đổi sort thành stable | Bot test có ≥4 richmenu, ≥4 QR action, ≥4 popup trong đó có **ít nhất 2 phần tử cùng `sort_position`** (hoặc cùng ngày tạo nếu sort theo ngày). Có mốc thứ tự hiển thị của cùng dữ liệu trên production/bản cũ để so | 1. Mở 「リッチメニュー」 (/basic/rich-menu), ghi thứ tự các dòng. 2. Mở 「QRコードアクション」 (/basic/landing), ghi thứ tự. 3. Mở 「ポップアップ」 (/basic/popup-manager), ghi thứ tự. 4. So từng list với mốc bản cũ | Dữ liệu có ≥2 phần tử trùng khoá sort mỗi màn | Thứ tự hiển thị 3 list **trùng khít** mốc bản cũ, kể cả các phần tử cùng `sort_position` (PHP8 `sort` stable giữ thứ tự chèn — không được đảo so với PHP7.2). Không màn nào đổi thứ tự | | Lấp Q3 · A1 checklist upgrade (sort STABLE) · regression · dẫn từ framework/php-upgrade-checklist A1 · Đánh giá spec: Spec không ghi (quy tắc PHP8, Leader chốt so mốc bản cũ) |
| TC-FUNCMULTI001-01 | UI | FUNC-MULTI-001 | QR Code Action 「QRコードアクション」: hành động có **bộ lọc đối tượng (友だち絞り込み / `filters_v2`)** chỉ chạy cho friend khớp điều kiện | Normal | manual | dev, local, prd, staging | line-friend | QR action có action gắn bộ lọc theo tag — chỉ friend có tag khớp mới được chạy action; friend không khớp bị bỏ qua, giống bản cũ | Bot test gói trả phí có LIFF. 1 QR action `MC4-FILTER`, 稼働対象 = `全ての友だち`, chuỗi action có **1 action gắn tag `MC4-DONE`** nhưng đặt `filters_v2` = "friend CÓ tag `SEG-A`". Có 2 tài khoản LINE test: F-A đã gắn tag `SEG-A`, F-B KHÔNG có tag nào. Cả 2 đã là bạn bot. Có mốc hành vi bản cũ của cùng cấu hình | 1. F-A mở landing `/landing-qr/<liffId>?uLand=<code của MC4-FILTER>` trong app LINE (đã là bạn → chạy nhánh action theo setting). 2. F-B làm y hệt với cùng URL. 3. Trên web mở 「友だちリスト」 → chi tiết F-A và F-B, tab 「タグ管理」. 4. Mở 「詳細データ」 → tab 「分岐詳細」 của `MC4-FILTER` | 2 friend: F-A (tag `SEG-A`), F-B (không tag). QR `MC4-FILTER` action tag `MC4-DONE` lọc `SEG-A` | Chỉ **F-A** được gắn tag `MC4-DONE` (khớp `filters_v2`); **F-B KHÔNG** được gắn (bị lọc) — giống hệt bản cũ. Không friend nào gây 500. Số 「アクション稼働」 ở 詳細データ chỉ +1 (cho F-A). Nối điều kiện lọc (where/orWhere mảng lồng) cho kết quả trùng production | | Lấp G3/MC4 · regression **F2** (query builder where/orWhere mảng lồng) + **F15** (filter dùng chung) · `filters_v2` per-action (BR-16) + BR-43 `action_with_friend` · manual vì cần app LINE thật · Đánh giá spec: Spec ghi rõ (qr-landing BR-16/BR-43) |
| TC-FUNC002-01 | UI | FUNC-002 | QR Code Action: 管理名 ký tự tiếng Nhật/全角/半角ｶﾅ/emoji — lưu · hiển thị · xuất CSV đúng encoding như bản cũ (A5) | Normal | auto | dev, local, prd, staging | web | Tạo QR action với 管理名 nhiều loại ký tự JP đặc biệt → list/edit/CSV đều giữ nguyên, không mojibake, không 500 | Bot test. Chuẩn bị 管理名 = `①テスト㈱ＱＲ🎌半角ｶﾅ` (≤50 ký tự: maru số ①, ㈱, full-width ＱＲ, emoji 🎌, kana nửa độ ﾊﾝｶｸ). Có mốc hiển thị bản cũ (PHP 7.2) của cùng chuỗi | 1. 「新規作成」 nhập 管理名 trên, chọn folder, 稼働対象 `全ての友だち`, Lưu (`POST /basic/create-landing-v2`). 2. Mở lại 「QRコードアクション」 danh sách → kiểm cột 管理名. 3. Vào 編集 V2 → kiểm header 管理名. 4. Mở 「詳細データ」 → xuất CSV tab 1. 5. Mở CSV bằng Excel JP (Shift_JIS) | 管理名 = `①テスト㈱ＱＲ🎌半角ｶﾅ` | Lưu OK không 500. 管理名 hiển thị **đúng từng ký tự** ở list + edit (không `?`/mojibake), DB lưu utf8mb4 nguyên vẹn. CSV xuất Shift_JIS giữ ký tự như production (ký tự ngoài Shift_JIS xử lý y hệt bản cũ — khớp NEW-407). Thứ tự byte/hiển thị trùng mốc PHP 7.2 | | Lấp G4/MC8 (A5 encoding JP) · regression encoding sau nâng PHP8/Laravel13 · auto (chỉ web, không cần LINE thật) · Đánh giá spec: Spec ghi rõ (管理名 ≤50, BR-01) + checklist A5 |
| TC-FUNC002-02 | API | FUNC-002 | QR Code Action: lưu **thiếu/để trống field** (外部連携 head/body/url · tin text rỗng · id rỗng-null) — null-handling giữ như bản cũ, không TypeError/500 (A4 + BR-37/BR-15) | Abnormal | auto | dev, local, staging | api | Lưu QR action mà bỏ trống các field tuỳ chọn → ghi null đúng theo BR-37/BR-15, không lỗi 500 trên PHP8 | QR action `MC8-NULL` đã có sẵn: `head_content`, `body_content`, `url_connect_qrcode_outside` đều có giá trị; có 1 template text nội dung `cũ`. Đăng nhập admin thật (CSRF+session). Có mốc hành vi bản cũ | 1. Gọi `EP-26` (外部連携 save) nhưng **bỏ trống** cả `head_content` + `body_content` + `url_connect_qrcode_outside`. 2. Lưu tin text của QR = **rỗng**. 3. Gửi tới các EP ajax của QR một `id`/param ở các dạng rỗng · null · chuỗi · số âm · quá dài. 4. Kiểm DB + response | head/body/url = rỗng; text template = rỗng; id = ``/`null`/`abc`/`-1`/chuỗi 300 ký tự | Bước 1: 3 cột bị **reset về null** (BR-37 — như production, KHÔNG giữ giá trị cũ). Bước 2: template bị **xoá**, FK về `null` (BR-15). Bước 3: mọi input xấu → JSON lỗi chuẩn (`{status:false,...}`, mã HTTP như production) **không 500 / không TypeError PHP8** (giống NEW-1318/NEW-799). Không record rác | | Lấp G4/MC8 (A4 null PHP8 + BR-37/BR-15) · regression null/TypeError PHP8 · auto · scope không prd (abnormal ảnh hưởng server) · Đánh giá spec: Spec ghi rõ (BR-37/BR-15) |
| TC-LIFFENTRY001-04 | UI | LIFF-ENTRY-001 | QR Code Action: mở landing từ **button trong tin LINE** (in-app + LINE PC) — bổ sung ô còn thiếu của ma trận điểm-vào | Normal | manual | dev, local, prd, staging | line-friend | Friend bấm button/URL landing đặt trong 1 tin LINE (không quét camera) → landing mở, action/đếm chạy đúng như quét QR | Bot test có QR action `MC5-BTN` đang bật (action gắn tag `MC5-BTN-TAG`). Soạn + gửi 1 tin tới friend chứa **button** hoặc link mở URL landing `https://<domain>/landing-qr/<liffId>?uLand=<code của MC5-BTN>`. Có tài khoản F04 (đã là bạn) nhận được tin, có cả LINE điện thoại và LINE PC | 1. F04 mở tin trong app LINE điện thoại, bấm button → landing mở trong in-app browser LINE. 2. Lặp lại: mở cùng tin trên **LINE PC**, bấm button. 3. Mỗi lần ghi trang hiển thị + mã HTTP. 4. Trên web mở 「詳細データ」 của `MC5-BTN` đối chiếu 「URL読み込み人数」 + 「アクション稼働人数」 | URL landing của `MC5-BTN` đặt trong button tin | Button mở landing **không 404/500** ở cả in-app điện thoại và LINE PC; đi qua đúng handler `EP-63/EP-64` như quét camera → `collect_open_landings` ghi lượt, action chạy theo setting (F04 nhận tag/tin), 「URL読み込み人数」 tăng. KHÔNG mất action do vào từ button thay vì quét QR | | Mở rộng G1/Q1 — ô **"button tin"** của ma trận LIFF-ENTRY (CLAUDE.md: in-app · trình duyệt ngoài · button tin · PC) · manual vì cần LINE thật (điện thoại + PC) · Đánh giá spec: Spec ghi rõ (qr-landing SCR-QRL-36 EP-63/64) |
| TC-MEDIAIMG001-01 | UI | MEDIA-IMG-001 | Rich menu 「リッチメニュー」 Step1 — Upload ảnh PNG nền trong suốt (Intervention v3) | Normal | manual | dev, local, prd, staging | web | Upload PNG 2500×1686 nền trong suốt ở Step1 rich menu → đuôi file + cách flatten nền + hiển thị LINE giữ y hệt production | Đăng nhập admin thật (/login-v2), chọn bot test gói trả phí, màn /basic/rich-menu. File PNG 2500×1686 nền TRONG SUỐT (alpha), ~3MB. User LINE test F01 là bạn bot. Có mốc production của đúng file này (production lưu .jpg nền TRẮNG do path cố định .jpg — bug #31953, GIỮ NGUYÊN theo F-6) | 1. Tạo rich menu mới, Step1 upload PNG trong suốt. 2. Đi hết 4 bước, lưu. 3. Mở ảnh đã lưu bằng URL trực tiếp: đọc đuôi file (url_image) và mở bằng công cụ xem ảnh có nền caro. 4. Gán rich menu cho F01, mở app LINE của F01 xem | PNG 2500×1686 nền trong suốt, 3MB | Hành vi khớp production (oracle = bản cũ Intervention v2): đuôi file + cách flatten alpha dưới Intervention v3 GIỮ Y HỆT PHP7.2 — production lưu .jpg nền trắng thì bản mới cũng .jpg nền trắng, KHÔNG được đổi sang nền đen/đổi màu do v3 flatten khác. LINE app F01 hiển thị y như production. Không 500, không lỗi Intervention trong log |  | Lấp G5 · regression Intervention v3 (F10) — alpha flatten đổi giữa v2/v3 · dẫn từ kho TC-RM-99 + bug prod #31953 · manual vì cần app LINE thật + mắt người so nền · Đánh giá spec: Đã hỏi leader (kho MT-07: production nền trắng, giữ như cũ; ứng viên raise ticket riêng → §8-5) |
| TC-MEDIA001-01 | UI | MEDIA-001 | Rich menu 「リッチメニュー」 Step1 — Upload ảnh sai định dạng / không phải ảnh | Abnormal | auto | dev, local, staging | web | Upload .gif/.webp/.svg/file đổi đuôi/file hỏng ở Step1 → báo lỗi định dạng, không 500, không tạo ảnh | Đăng nhập admin thật, bot test, màn /basic/rich-menu tạo mới ở Step1. Chuẩn bị 5 file: a.gif (2500×1686), b.webp, c.svg, d là .txt đổi đuôi thành .jpg, e là .jpg nội dung byte rác (hỏng). Có mốc message production | 1. Ở Step1 lần lượt chọn từng file a→e và bấm nút lưu/sang bước để gửi ảnh lên server. 2. Ghi message hiển thị + mã HTTP mỗi lần. 3. Query rich_menus/url_image xác nhận không tạo record ảnh | a.gif · b.webp · c.svg · d.txt→.jpg · e.jpg hỏng | Mỗi file sai → báo lỗi 「.png、.jpg、.jpegのファイルをアップしてください。」 (hoặc message production tương ứng), không nhận ảnh, không 500, không TypeError PHP8. File d (đổi đuôi) và e (jpg hỏng) cũng bị chặn vì rule kiểm nội dung thật (Base64IsImage/Base64ImageType), không chỉ đuôi. Giống hệt production | | Lấp G6 · regression diff `app/Rules/Base64ImageType.php`·`Base64IsImage.php` (A4 validation) · dẫn từ kho TC-RM-88/89 · auto (chỉ web) · Đánh giá spec: Đã hỏi leader (kho MT-06: hệ thống chấp nhận .jpeg; message chốt TC-RM-89) |
| TC-FUNC002-03 | API | FUNC-002 | Rich menu/folder create — input rỗng/null (管理名 rỗng · chưa upload ảnh · folder name rỗng) | Abnormal | auto | dev, local, staging | api, web | Tạo rich menu/folder với field rỗng/null → validate báo lỗi đúng, không 500/TypeError PHP8, không tạo record rác | Đăng nhập admin thật (CSRF + session), bot test, màn /basic/rich-menu. Có mốc message + hành vi production (FE: nút 次へ disable khi chưa upload ảnh; empty 管理名 → 「管理名を入力してください」; empty folder → 「フォルダ名を入力して下さい」) | 1. Modal tạo mới: để trống 管理名, bấm 「メッセージ登録に進む」 → ghi message + mã HTTP. 2. Step1 chưa upload ảnh → kiểm nút 次へ disable. 3. フォルダ追加 để trống/toàn space tên → lưu → ghi message. 4. Replay POST các EP (create modal / folder add / save) với body rỗng·null·thiếu field → ghi mã HTTP + response. 5. Query rich_menus/category xác nhận không tạo record rác | 管理名=rỗng/null · ảnh=(chưa chọn) · folder name=rỗng/「␣␣␣」 · body EP=rỗng/null/thiếu field | Mỗi nhánh FE → validate message đúng production (「管理名を入力してください」/「フォルダ名を入力して下さい」), KHÔNG tạo record, modal vẫn mở; nút 次へ disable khi chưa ảnh. Replay body rỗng/null/thiếu field → JSON lỗi chuẩn + mã HTTP như production, **không 500, không TypeError/Undefined PHP8**. Không record rác trong rich_menus/category | | Lấp Q4 (A4 null/empty PHP8) · regression validation rich menu create · dẫn từ kho TC-RM-67/107/05/09 · auto · scope không prd (abnormal ảnh hưởng server) · Đánh giá spec: Spec ghi rõ (message validate — kho MT-08) + checklist A4 |
| TC-FUNC002-04 | UI | FUNC-002 | ポップアップ: 管理名 + text ký tự JP/全角/半角ｶﾅ/emoji/HTML (A5) + lưu thiếu field (A4) | Normal | auto | dev, local, prd, staging | web | Tạo/sửa popup với 管理名+text chứa ký tự đặc biệt → lưu/mở lại/preview/site thật giữ nguyên không mojibake/double-escape; field bắt buộc rỗng bị chặn không 500 | Bot test, màn 「ポップアップ」. 管理名 = `①ポップ㈱🎉半角ｶﾅ`; text popup = `A&B <b>tag</b> "quote" 'x' 🎉①`. Có mốc hiển thị bản cũ (PHP7.2) | 1. Tạo popup nhập 管理名 + text trên + ảnh + URL đích, 登録. 2. Mở lại popup (sửa) + xem preview → đối chiếu từng ký tự. 3. Đối chiếu popup THẬT trên trang nhúng. 4. A4: tạo popup khác để trống 管理名/ảnh/URL + replay POST body rỗng/null | 管理名 `①ポップ㈱🎉半角ｶﾅ`; text có `& < " ' 🎉` | 管理名+text hiển thị **đúng nguyên văn** ở edit/preview/site thật (không `&amp;`/`&lt;` nhân đôi, không mất emoji/①㈱, HTML không thực thi). DB utf8mb4 giữ nguyên. A4: field bắt buộc rỗng → message đúng (「管理名を入力してください。」…), body rỗng/null → JSON lỗi chuẩn, **không 500/TypeError PHP8**. Giống production | | Lấp MC7 (A5 encoding JP/emoji/HTML 管理名+text — NEW-624 chỉ dùng tên JP; A4 đã có 625, hoàn thiện thêm null body) · regression A5 htmlspecialchars ENT_QUOTES PHP8 + A4 null · auto · Đánh giá spec: `spec-features` không có spec popup → so mốc bản cũ |
| TC-FUNCDATE001-03 | UI | FUNC-DATE-001 | ポップアップ: kỳ hiển thị theo 開始/終了日時 (A2 JST) — popup chỉ hiện trong khoảng, biên ngày đúng | Boundary | auto | dev, local, prd, staging | web, line-friend | NẾU popup có cấu hình kỳ hiển thị theo ngày (開始日時/終了日時): popup chỉ hiện trong khoảng, mốc biên + JST giống bản cũ (A2 Carbon) | Bot test, màn 「ポップアップ」. Tạo popup P có cấu hình kỳ hiển thị 開始日時/終了日時 (nếu màn có). Mốc kiểm: trước 開始 · trong khoảng · sau 終了 · biên 00:00-09:00 JST · ngày 31/cuối tháng. Có mốc production. ⚠️ Nếu popup CHỈ có "sau N giây" (không có kỳ-theo-ngày) → TC N/A, báo Leader | 1. Cấu hình kỳ hiển thị của P. 2. Mở trang nhúng ở các mốc: trước 開始 (không hiện), trong khoảng (hiện), sau 終了 (không hiện). 3. Kiểm biên 00:00-09:00 JST + ngày cuối tháng không lệch. 4. So với production | 開始/終了日時 + các mốc biên | Popup chỉ hiển thị **trong khoảng [開始, 終了]** đúng JST; trước/sau khoảng không hiện; biên 00:00-09:00 không lệch −1 ngày, ngày 31/cuối tháng đúng (A2 Carbon). Trùng khít bản cũ PHP7.2 | | Lấp MC3 — kỳ hiển thị theo ngày A2 (Studio chỉ có "sau N giây" NEW-624/626) · regression A2 (Carbon/date popup) · auto · ⚠️ **Leader xác nhận popup có kỳ hiển thị theo 開始/終了日時 không** (spec-features không có spec popup) → §8 · Đánh giá spec: Spec không có (hỏi Leader) |
| TC-DATACOUNT001-01 | UI | DATA-COUNT-001 | URL分析 (/basic/url) — Tỉ lệ click khi mẫu số = 0 (0 配信 / 0 click / kỳ rỗng): A3 number_format + A4 không 500 | Abnormal | auto | dev, local, staging | web | Mở URL分析 + 詳細確認 của URL có 0 lượt gửi / 0 click / chọn kỳ không có click → tỉ lệ hiển thị đúng (0% hoặc —), không 500/TypeError, number_format không sai float→int | Bot test (gói trả phí) có: URL-A phát hành nhưng chưa gửi (配信数=0), URL-B đã gửi nhưng 0 click (開封率=0%), URL-C có click. Có mốc production. **URL分析 là feature cross-cutting** (DetailUrlClick — sibling DetailLandingClick, gắn B3b click-tracking) | 1. Mở 「URL分析」, xem dòng URL-A (配信0) + URL-B (click0): cột 開封数/率, ユニーククリック数/率. 2. Bấm 詳細確認 của URL-A và URL-B. 3. Ở URL-C chọn khoảng ngày KHÔNG có click (kỳ rỗng). 4. Ghi HTTP + Console mỗi bước | URL-A 配信=0; URL-B gửi nhưng 0 click; URL-C kỳ rỗng | URL-A (配信0): 開封率/クリック率 hiển thị **0% hoặc 「-」** như production, KHÔNG chia-cho-0 → NaN/Infinity/500. URL-B: 0 click → 率=0%. Kỳ rỗng URL-C: biểu đồ/tổng = 0, không 500. Mọi số qua number_format đúng (không float→int sai). Console không lỗi. Giống production | | Lấp G7 (maincase 6 A4 + maincase 2 A3 — URL分析 rate khi mẫu số 0 / kỳ rỗng) · URL分析 cross-cutting (diff URLController + DetailUrlClick) · NEW-289/461/463 chỉ test URL CÓ dữ liệu · regression A3 number_format + A4 chia-0 PHP8 · auto · Đánh giá spec: Đã hỏi leader (so production) |

## 8. Spec update needed

| # | Điểm cần chốt | Nguồn | Ai chốt |
|---|---|---|---|
| 1 | Rich menu ảnh > 1MB: ép < 1MB (BR-07) hay giữ > 1MB như production (PB-T15-1, nhánh V2 q80)? Spec `rich-menu` BR-07 cần ghi rõ 2 nhánh `UserController`(≤1MB q90) vs `RichMenuService`(q80 không ép) | §4 CONF-SPEC · NEW-172 | Dev + Leader |
| 2 | Popup 利用規約 chặn ở **màn đầu sau đăng nhập** hay **mọi màn**? (QA-spec-004) | NEW-960 (CÂU HỎI CHO LEADER) vs NEW-966 | Leader |
| 3 | Popup 利用規約: nút đồng ý — disabled đến khi tick (QA-spec-005) và không bắt buộc cuộn hết nội dung mới cho tick (QA-spec-007) | NEW-965 / NEW-963 (đều CÂU HỎI CHO LEADER) | Leader + Pháp chế |
| 4 | Popup 利用規約: trạng thái đồng ý chỉ lưu server-side? Hàm ghi mốc localStorage (`header.blade.php:1920`) không nơi nào gọi — code chết hay thiếu chỗ gọi? | NEW-958 (CẦN XÁC NHẬN) | Dev |
| 5 | Rich menu Step1 upload **PNG nền trong suốt → nền trắng** (bug #31953 đã fix ở FA-005 tạo-ảnh nhưng CHƯA fix ở Step1 FA-004, path lưu cố định `.jpg`). Trong sprint nâng cấp: giữ nguyên hành vi theo F-6 rồi gom ticket riêng, hay fix luôn? Lưu ý Intervention v3 có thể đổi màu nền flatten (không còn trắng) → cần chốt oracle | §1 G5 (không đẻ TC) · kho MT-07 / TC-RM-99 | Leader + Dev |
| 6 | **Popup (ポップアップ /basic/popup-manager)**: có cấu hình **kỳ hiển thị theo ngày 開始/終了日時** không, hay chỉ "hiển thị sau N giây"? Quyết định có cần TC-FUNCDATE001-03 (A2 kỳ hiển thị). `spec-features` không có spec popup để tra | §7 MC3 · NEW-624/626 | Leader |

---

# BATCH B1 — Payment / Contract / Sales V2 / Affiliate

## 0. Nguồn TC
- **Nguồn đã dùng**: MCP LME TEST STUDIO — task_id=507, ticket 43845 (subset B1 lọc theo `screen`/`viewpoint`: 決済/契約/商品販売/販売履歴/解約/クーポン/返金/affiliate/月次売上-決済/ARPU/LTV/振込).
- **Tổng số TC review**: 183 (Stripe/UnivaPay pay+3DS, 契約詳細, 販売履歴, 領収書/見積書, 解約一覧, coupon, 返金, affiliate/代理店, System Admin 売上).

> **Đã áp [framework/php-upgrade-checklist.md](../../framework/php-upgrade-checklist.md)** (task nâng version). Nhận xét chung: **đây là bộ TC trưởng thành nhất trong các batch** — checklist A/B/C gần như phủ hết (bảng cuối §2). Vấn đề của B1 **không phải thiếu TC thiết kế** mà là **chưa thực thi** (24.6% pass, 0 prd) — xem §1 + §5.

## 1. Coverage — dev-impact + diff code

- **dev-impact: 3/3 nhóm ảnh hưởng B1 có TC thiết kế — nhưng CHƯA ĐỦ (chưa xác nhận).** F5 (Stripe v22/UnivaPay 3DS) · tiền decimal (F-11) · T2 (payment/sales/contract/affiliate) đều có TC Normal+Abnormal+Boundary dày. **Nhưng** chỉ 45/183 (24.6%) pass thật và **0 TC chạy production** → với bill tiền, coverage **chưa được xác nhận** (§5).
- **diff code: CHƯA ĐỦ (chưa xác nhận).** `requirement_keys` của diff (REQ-T11 payment, REQ-T20 sales, REQ-T22 contract/plan, REQ-T6 month-split, REQ-T13 CSV) đều có TC. Không phát hiện điểm sửa nào thiếu TC thiết kế.

| Mã | Chiều | Vùng ảnh hưởng | TC hiện có | Status | Ghi chú |
|---|---|---|---|---|---|
| R1 | dev-impact + diff | **Bill tiền / Stripe / UnivaPay chạy production** (A3 tiền — sai 1 yên = BLOCKER) | NEW-325/326/327/330/331/332-336 (pay/3DS/refund) · NEW-481/482/638 (tiền/thuế) đều env=dev/local | **RISK** | RULE-08 **nặng nhất ở batch này**: tiền/cổng thanh toán KHÔNG kết luận từ dev/local. Scope phải chứa `prd`, chạy thật trên QA PHP 8.5 có Stripe/UnivaPay test + prd |
| R2 | diff | **A2 — chia doanh thu tháng** (Carbon diffInMonths đổi dấu/UTC ở PHP8) | NEW-45/46 có TC | **RISK (chờ chốt)** | NEW-46 ra **6 bản ghi** (production PHP7 ra **5**) — behavior change do fix PHP8; TC ghi "không báo bug, chờ PO xác nhận". Expected đúng chưa chốt → §8 |

**Kết luận §1**: 0 GAP · 2 RISK (R1 exec/prd, R2 chờ chốt). **Thiết kế TC đủ cả 2 chiều; coverage chưa xác nhận do 24.6% pass + 0 prd.**

## 2. Thiếu so với quan điểm test

**Kết luận**: quét theo màn (payment/contract/sales/affiliate) + checklist A/B/C — **không phát hiện quan điểm Trigger khớp mà thiếu TC thiết kế**. Bảng đối chiếu checklist (nháp, để Leader thấy độ phủ):

| Mục checklist | Trạng thái B1 | TC tiêu biểu |
|---|---|---|
| A1 sort stable | ✅ phủ | NEW-493/494 (解約一覧 sort + biên khoá trùng ổn định), NEW-476, NEW-1564 |
| A2 ngày giờ/Carbon signed | ✅ phủ dày | NEW-45/46/231/540/543/546/547/548/568/569 (biên 29-31, nhuận, 0-9h JST, diffInMonths) |
| A3 tiền decimal | ✅ phủ dày | NEW-481/482 (báo giá + chiết khấu bậc), NEW-638 (thuế), NEW-232/817/818 (LegacyMath::arraySum, % làm tròn, #44069), NEW-334 (số tiền đồng nhất course/CSV/Stripe) |
| A4 null/TypeError | ✅ phủ | NEW-828 (u_code rỗng/sai), NEW-343 (gateway net err no 500), NEW-480/545 (undefined var / cvv null) |
| A5 encoding | ✅ phủ | NEW-215 (ký tự and + nháy đơn không escape), NEW-399/400/401/409 (BOM/UTF-8/Shift_JIS, kana maru-kabu-emoji), NEW-638 (PDF JP) |
| A6 type juggling == | ⚠️ gián tiếp | filter/search (NEW-383); không có TC riêng khẳng định juggling — rủi ro thấp ở màn tiền |
| B Stripe v22 | ✅ phủ dày | NEW-325 (+ API version 2026-09-30), 326/328/330/331/332/334/335/336 |
| B UnivaPay (Guzzle 7) | ✅ phủ | NEW-327/329/342/343/543/544, NEW-183-189 (liên kết cổng) |
| B Mail chuyển khoản | ⚠️ 1 phần | NEW-342 (mail đăng ký 振込); mail **gia hạn** NEW-534/535 ở batch **B10** — cross-ref |
| C APP_KEY giải mã token thanh toán | ✅ phủ (tốt hơn B3b) | NEW-334 (liên kết Stripe cũ dùng được không nhập lại credential), NEW-183/379 (config UnivaPay/sản phẩm do 5.5 ghi đọc đúng) |

→ Không sinh `Q<x>`. Điểm duy nhất mờ: **A6** (== juggling) không có TC chuyên biệt — rủi ro thấp, ghi 1 dòng §5 [NIT].

## 3. TC trùng lặp

Đã rà 183 TC — **không phát hiện trùng lặp**. Các cụm nhìn giống nhau là **tách atomic có chủ đích** (ghi rõ trong note TC, không gộp): 領収書/決済履歴 NEW-637 → NEW-1560/1561/1562/1563/1564/1565 (đổi năm · lọc có/không kết quả · bỏ lọc · sort · năm rỗng); NEW-638 → NEW-1566/1567/1568/1569/1413 (様 · tắt auto-name · đóng modal · bulk); 解約一覧 NEW-493 (sort chung) vs NEW-494 (biên khoá trùng). Giữ nguyên.

## 4. Mâu thuẫn trong TCs

Đã rà 183 TC × spec `billing-plan`/`bill-item`/`detail-contract`/`payment-system-integration` + kho `fa026`/`fa031` — **không phát hiện mâu thuẫn TC-vs-TC hay TC-vs-kho**. Các điểm "khác production có chủ đích / chờ chốt" đưa xuống §8 (không phải mâu thuẫn): NEW-46 (6 vs 5 bản ghi chia tháng), NEW-480 (PayPal 課金管理 undefined var).
- **CONF-IGNORE**: không có (ignore-features.md chỉ có IG-01 Booking Manager). ⚠️ Nhưng 2 màn chết thanh toán cũ — PayPal 「課金管理」 `/admin/user-point-settings` (NEW-480), 「支払履歴」 cũ `/basic/download-invoice` (NEW-639) — đang "giữ hành vi lỗi/trắng như production"; **ứng viên thêm vào ignore-features** → §8 hỏi Leader.

## 5. Issues khác

| # | Severity | TC / phạm vi | Vấn đề | Đề xuất |
|---|---|---|---|---|
| 1 | `[BLOCKER]` | Toàn batch B1 | **24.6% pass thật** (45/183: pass 45 · **0 fail/error** · skip 124 · chưa chạy 14). Thiết kế TC đủ nhưng 75% chưa có kết luận test (skip do runner thiếu Stripe/UnivaPay/thẻ test/prd — F-14) | Chạy lại B1 trên **QA PHP 8.5 có Stripe test + UnivaPay test + prd**; coi mọi "đủ" ở §1 là RISK tới khi có pass |
| 2 | `[MAJOR] RULE-08` (≈BLOCKER cho tiền) | Toàn nhóm bill/決済/返金/見積/領収書 (env dev 148 · local 21 · **prd 0**) | Task chạm **bill tiền** mà 0 TC chạy production. Với A3 (sai 1 yên = BLOCKER) đây là rủi ro cao nhất batch | `env_scope` phải chứa `prd`; chạy thật: mua 単品/継続 Stripe+UnivaPay, 3DS, refund, báo giá/領収書 PDF tiền+thuế, chia doanh thu tháng |
| 3 | `[MINOR]` | NEW-1398, NEW-1558, NEW-1559 | 3 TC **thiếu mã quan điểm** (`viewpoint`=None), chưa chạy | Gán mã quan điểm (`FUNC-PAY-*`/`REQ-T11`) |
| 4 | `[NIT]` | Toàn batch | A6 (type juggling == PHP8) chưa có TC chuyên biệt ở nhánh filter/rẽ nhánh tiền | Cân nhắc 1 TC filter 「決済ステータス」 giá trị biên nếu Leader thấy cần |
| 5 | `[NIT]` cross-ref B10 | NEW-342 (mail 振込 đăng ký) | Memory contract-transfer-mail-rules: cần regression **negative** "thẻ/tháng KHÔNG gửi mail chuyển khoản" + mail **gia hạn** (NEW-534/535) — thuộc batch **B10 Mail** | Kiểm khi review B10, không trùng ở B1 |

Chất lượng từng TC: **xuất sắc** — tự đầy đủ, oracle = production/base commit cụ thể, tiền/thuế ghi số chính xác, nêu rõ PB-xx và điều kiện môi trường. Không có TC mơ hồ.

## 6. TCs thừa / ngoài phạm vi task

Đã rà 183 TC — **không có TC ngoài phạm vi #43845**. Lưu ý 2 TC giá trị thấp (verify "màn chết vẫn chết như production"), Leader cân nhắc đưa màn vào ignore-features thay vì giữ TC regression mỗi vòng: **NEW-480** (PayPal 「課金管理」 /admin/user-point-settings — undefined var), **NEW-639** (「支払履歴」 cũ /basic/download-invoice — trang trắng). Cả hai là regression hợp lệ theo diff hiện tại nên **không flag thừa**, chỉ đề nghị quyết định ở §8.

## 7. TCs đề xuất bổ sung (7)

Đã đối chiếu 183 TC ở BƯỚC 0 + spec `billing-plan`/`bill-item`/`detail-contract` + kho `fa026`/`fa031` + checklist A/B/C. Rà **theo màn** (ban đầu) không thấy GAP thiết kế A/B/C.

> **Bổ sung 2026-10-27 — rà riêng Bill tiền hợp đồng theo 8 maincase** (105 TC billing-cluster + memory billing). 4/8 ĐỦ (MC2 契約詳細 6 trường · MC3 mua/nâng/再契約 · MC5 gateway+callback · MC8 **A2/A3** dày). Nhưng 4 ô trống khớp đúng **rule nghiệp vụ trong memory + 1 [BLOCKER]** mà bộ Studio chưa cover → 5 TC: **MC1** stored card token Stripe/UnivaPay giải mã + bill ngay sau deploy (config gateway đã có 183/186/2070 nhưng token thẻ chưa — [BLOCKER] APP_KEY) · **MC4** 2 **hành động** hủy (user + job cưỡng chế) → /basic/re-contract/ (7 TC cũ chỉ XEM 解約一覧) · **MC6** mail gửi **ngay khi tạo STK** mua mới (NEW-534 job gia hạn **đang Không đạt bug 44584**; NEW-342 chỉ modal) · **MC7** ma trận nút **振込キャンセル** (0 TC) · **MC8** job bill năm thu **đúng 1 năm KHÔNG 2年分**. Dẫn từ memory `billing-recontract-rules` / `contract-transfer-mail-rules` / `transfer-cancel-button-rule`. Toàn bộ `manual` + ENV chứa `prd` (RULE-08 bill tiền).

> **Bổ sung 2026-10-27 (bis) — rà riêng Bill item (FA-026 商品販売, sản phẩm) theo 8 maincase** (61 TC product-cluster + kho FA-026 + memory). **6/8 maincase ĐỦ thiết kế**: (1) CRUD + A3 giá — NEW-373/374/375/378-382 + NEW-481/482/638 · (2) Stripe/UnivaPay mua/sub/hủy/đổi thẻ/receipt/3DS — NEW-325-331/342/343/741/742/1108/1109/1111 · (3) ảnh sản phẩm Intervention v3 — NEW-180/182 · (5) order history A2 — NEW-230/231/229/637/1560-1565 · (7) LIFF mua hàng — NEW-68/69/325-327/828 · (8) A4 u_code null + A5 — NEW-828/742/215/399/638. **2 gap memory-backed chưa cover** → 2 TC: **G1** link mua/変更/解約/preview sản phẩm đã xoá → 「この商品ページはすでに削除されています。」 (NEW-69 chỉ 購入/preview không-lỗi) · **G2** mobile notify loại 3 lưu `form_answer_result.id` (không phải order). **MC8 hết hàng/購入上限** cover representative qua kho FA-026 group 16 + A4 NEW-828 (không đẻ lại). ID push đã tránh trùng (FUNC002-05, DATADB001-01).

| ID | Nhóm | Mã quan điểm | Màn hình/chức năng | Loại case | Chạy | Phạm vi ENV | Surface | Tên case | Tiền điều kiện | Các bước thực hiện | Dữ liệu nhập | Kết quả mong đợi | Kết quả thực thi | Ghi chú |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TC-COMPATLEGACY001-01 | API | COMPAT-LEGACY-001 | 契約詳細/Auto-bill: token thẻ Stripe/UnivaPay lưu bằng APP_KEY cũ **giải mã được + bill thành công ngay sau deploy** | Normal | manual | dev, local, prd, staging | job, api | HĐ có sẵn (card token lưu trước deploy) → sau deploy đổi cookie serialization (F-12), token vẫn giải mã, auto-bill charge thành công | ≥2 HĐ trả phí tạo TRƯỚC deploy: 1 Stripe (customer/card token đã lưu), 1 UnivaPay (transaction token đã lưu). Môi trường đã deploy PHP8.5/Laravel13 với **APP_KEY production giữ nguyên**. Có Stripe/UnivaPay test. Mốc production | 1. Sau deploy, mở 契約詳細 2 HĐ — kiểm thông tin thẻ/cổng hiển thị (token giải mã OK). 2. Chạy tay job auto-bill (hoặc tới kỳ) cho 2 HĐ. 3. Kiểm charge Stripe/UnivaPay thành công + payment_histories + 決済履歴. 4. Nếu dựng được case APP_KEY/encryption lệch → xác nhận báo lỗi rõ, KHÔNG charge sai | 2 HĐ token cũ (Stripe + UnivaPay) | Token thẻ cũ **giải mã đúng** bằng APP_KEY production trên bản mới; auto-bill charge đúng số tiền + ghi payment_histories/決済履歴 như production. KHÔNG fail âm thầm (encryption lệch → lỗi rõ, không charge sai) | | Lấp MC1 — stored card token decrypt (config gateway đã có 183/186/2070, token thẻ bill chưa) · **[BLOCKER]** APP_KEY/encryption (cross-ref B7 Auth T10 + B3b §5-6) · regression F-12 cookie/encryption · manual + prd (RULE-08) · Đánh giá spec: Spec ghi rõ (deploy-notes APP_KEY giữ nguyên) |
| TC-FUNC001-03 | API | FUNC-001 | Hủy hợp đồng 2 kiểu (user hủy · job hủy cưỡng chế) — cùng điều hướng /basic/re-contract/ + vào 解約一覧 | Normal | manual | dev, local, prd, staging | web, job | (a) User tự hủy HĐ → /basic/re-contract/, HĐ sang 解約済み; (b) job hủy cưỡng chế HĐ 延滞 quá hạn → cùng /basic/re-contract/, 解約一覧 ghi nhận | 2 HĐ trả phí active: HĐ-U (để user hủy), HĐ-J (chuyển khoản 延滞 quá mốc cưỡng chế). Admin đăng nhập. Stripe/UnivaPay test. Mốc production + memory `billing-recontract-rules` | 1. HĐ-U: user thao tác hủy qua UI → quan sát điều hướng + trạng thái. 2. Chạy job hủy cưỡng chế cho HĐ-J (延滞 quá hạn). 3. Mở 解約一覧 kiểm cả 2; mở 契約詳細 từng HĐ kiểm ステータス=解約済み + 操作履歴 | HĐ-U (user hủy), HĐ-J (job cưỡng chế 延滞) | Cả 2 kiểu hủy đều dẫn tới **/basic/re-contract/**, HĐ chuyển **解約済み**, xuất hiện ở **解約一覧** đúng thời điểm hủy; 操作履歴 ghi đúng loại hủy (user vs 強制). Không 500/TypeError PHP8. Giống production | | Lấp MC4 — 7 TC cũ chỉ XEM 解約一覧/理由/churn, chưa test **hành động hủy** · dẫn từ memory billing-recontract-rules · manual (gateway + job) · Đánh giá spec: Đã hỏi leader (2 kiểu hủy /re-contract/); ⚠️ mốc 延滞 bao nhiêu ngày job cưỡng chế → §8 |
| TC-NOTIMAIL001-01 | API | NOTI-MAIL-001 | Mua mới HĐ chuyển khoản: mail chuyển khoản gửi **ngay khi UnivaPay tạo STK** (chậm thì job gửi); thẻ/tháng KHÔNG gửi | Normal | manual | dev, local, prd, staging | job, api | Mua mới HĐ 銀行振込 → tạo STK → mail STK gửi ngay tới admin; STK chậm → job gửi bù; đối chứng thẻ/tháng không gửi | Admin mua mới HĐ 年間一括払い bằng 銀行振込. UnivaPay test tạo STK. Hộp mail admin (Gmail/Yahoo/Hotmail/Outlook). Mốc production + memory `contract-transfer-mail-rules` | 1. Mua mới HĐ 銀行振込 → UnivaPay tạo STK. 2. Kiểm mail STK gửi NGAY (銀行名/支店/口座/振込期限/tổng tiền), From=ADMIN_MAIL, không CC/BCC, không Spam 4 provider. 3. Giả lập STK tạo chậm → job gửi bù (không trùng). 4. Đối chứng: mua bằng **thẻ** / gói **tháng** → KHÔNG mail chuyển khoản | HĐ mua mới 年間 振込; đối chứng thẻ/tháng | Mail STK gửi **ngay khi tạo STK**, nội dung đủ (mua mới phủ 1 năm + 2年分 theo memory), không Spam; STK chậm → job gửi bù 1 lần. Thẻ/tháng **KHÔNG** gửi. Khác NEW-534 (job gia hạn, đang fail 44584) | | Lấp MC6 — mail NGAY khi tạo STK (NEW-534 là job gia hạn, Không đạt 44584; NEW-342 chỉ modal) · negative thẻ/tháng (cross-ref B10 §5-5) · dẫn từ memory contract-transfer-mail-rules · manual (mail thật) · Đánh giá spec: Đã hỏi leader |
| TC-FUNC001-04 | UI | FUNC-001 | Nút 振込キャンセル chỉ hiện ở **mua mới lần đầu + nâng từ Free**; luồng khác chỉ 契約詳細 | Normal | manual | dev, local, prd, staging | web | Ma trận hiển thị nút 振込キャンセル: mua mới lần đầu ✓ · nâng Free→trả phí ✓ · đổi phương thức/gia hạn/standard→pro/再契約/job bill ✗ (chỉ 契約詳細) | Dựng HĐ 銀行振込 (đang chờ chuyển khoản) ở từng luồng: mua mới lần đầu · nâng Free→Standard · đổi phương thức sang 振込 · gia hạn · standard→pro · 再契約 · HĐ bị job bill. Mốc production + memory `transfer-cancel-button-rule` | 1. Mỗi luồng mở màn tương ứng + 契約詳細, kiểm có/không nút 「振込キャンセル」. 2. Luồng CÓ nút (mua mới lần đầu, nâng Free): bấm 振込キャンセル → hủy STK đúng. 3. Luồng KHÔNG nút: xác nhận chỉ thao tác được ở 契約詳細 | 7 luồng như tiền đề | Nút 「振込キャンセル」 **chỉ hiện** ở mua mới lần đầu + nâng từ Free (bấm hủy STK đúng). Đổi phương thức/gia hạn/standard→pro/再契約/job bill **KHÔNG** có nút, chỉ thao tác qua 契約詳細. Giống production | | Lấp MC7 (0 TC) · dẫn từ memory transfer-cancel-button-rule · manual (dựng HĐ 振込 từng luồng) · Đánh giá spec: Đã hỏi leader |
| TC-JOBBILL001-01 | API | JOB-BILL-001 | Auto-bill job HĐ gói năm thu **đúng 1 năm**, KHÔNG thu 2年分 (2年分 chỉ nhãn GUI mua mới) | Normal | manual | dev, local, prd, staging | job | Job AutoPaymentJobUnivapay bill HĐ 年間一括払い tới kỳ → charge **1 năm tiền**, gia hạn +1 năm; 2年分 chỉ là nhãn GUI lúc mua mới, không phải số tiền job thu | HĐ 年間一括払い active tới kỳ gia hạn (thẻ hoặc 振込 UnivaPay). Giá gói 1 năm = P. GUI mua mới hiển thị 「2年分」. UnivaPay test. Mốc production + memory `billing-recontract-rules` | 1. Tới kỳ (hoặc chạy tay) job auto-bill cho HĐ năm. 2. Kiểm charge = **P (1 năm)**, KHÔNG phải 2P. 3. Kiểm expired_date_contract +1 năm + payment_histories 1 bản ghi = P. 4. Đối chiếu GUI mua mới hiển thị 2年分 nhưng số tiền thu = 1 năm | HĐ năm, giá 1 năm = P | Job bill charge **đúng 1 năm (P)**, gia hạn +1 năm, payment_histories = P. **2年分 KHÔNG được job thu** (chỉ nhãn GUI mua mới). Số tiền A3 chính xác tới yên. Giống production | | Lấp MC8 — rule memory "2年分 chỉ GUI, job bill năm thu 1 năm" chưa có TC xác nhận · A3 tiền [BLOCKER] · manual + prd (RULE-08) · Đánh giá spec: Đã hỏi leader |
| TC-FUNC002-05 | UI | FUNC-002 | 商品販売 FA-026 — Link mua/変更/解約/preview của sản phẩm ĐÃ XOÁ → 「この商品ページはすでに削除されています。」 | Abnormal | manual | dev, local, prd, staging | line-friend, web | Mở 4 loại link (mua · đổi thẻ · hủy · preview) của sản phẩm đã xoá → đều hiện đúng 「この商品ページはすでに削除されています。」, không 500 | Bot test có 1 sản phẩm 継続 P (F01 đã có hợp đồng) + 1 単品. Lấy sẵn 4 URL: 購入 · カード情報変更 · 解約用ページ · preview (u_code=preview). Sau đó **xoá** sản phẩm. Có mốc production + memory item-deleted-link-message | 1. Xoá sản phẩm. 2. Lần lượt mở 4 URL bằng app LINE LIFF + trình duyệt ngoài. 3. Ghi màn hiển thị + mã HTTP mỗi link | 4 URL (mua/đổi thẻ/hủy/preview) của sản phẩm đã xoá | Cả 4 link hiển thị đúng nguyên văn 「この商品ページはすでに削除されています。」, KHÔNG 500/trang lỗi, KHÔNG cho thao tác mua/đổi thẻ/hủy. Giống production | | Lấp G1 (maincase 4 — deleted-product 4 link types → message) · dẫn từ memory item-deleted-link-message · NEW-69 chỉ cover 購入+preview không-lỗi, thiếu change/hủy + exact message · manual vì LIFF app LINE · Đánh giá spec: Đã hỏi leader (memory Leader chốt) |
| TC-DATADB001-01 | Data | DATA-DB-001 | MobileNotify loại 3 (order notify) — lưu `form_answer_result.id`, KHÔNG phải id order thanh toán | Normal | manual | dev, local, prd, staging | mobile-app, web | Mua sản phẩm (có form) sinh notify app loại 3 → `order_item_id` = `form_answer_result.id` như production | Cờ `ENABLE_HANDLE_PUSH_MESSAGE_NOTIFY` **BẬT** (kho MT-26). Bot test, app mobile đăng nhập. Sản phẩm có form thu thập khi mua. F01 mua → sinh form_answer_result + order. Có mốc production + memory mobile-notify-order-item-id (spec db-mapping ghi sai) | 1. F01 mua sản phẩm (có form) thành công. 2. Chờ job notify. 3. App mobile nhận notify loại 3. 4. Đọc bảng mobile_notify dòng vừa sinh: cột `order_item_id`. 5. Đối chiếu với `form_answer_result.id` và với id order thanh toán | Mua sản phẩm có form | Notify app loại 3 sinh 1 dòng mobile_notify với `order_item_id` = **`form_answer_result.id`** (KHÔNG phải id order/đơn thanh toán), như production; badge app +1 đúng. Không 500/TypeError PHP8 | | Lấp G2 (maincase 6 — mobile notify loại 3 lưu form_answer_result.id) · dẫn từ memory mobile-notify-order-item-id · tiền đề cờ ENABLE_HANDLE_PUSH_MESSAGE_NOTIFY BẬT (kho MT-26) · regression MobileNotify mapping · manual vì app mobile thật + flag · Đánh giá spec: Đã hỏi leader (spec db-mapping ghi sai field này → §8) |

## 8. Spec update needed

| # | Điểm cần chốt | Nguồn | Ai chốt |
|---|---|---|---|
| 1 | Chia doanh thu gói năm ngày mùng 1 trước 9:00 JST: PHP8 ra **6 kỳ**, production PHP7 ra **5 kỳ** (PB-T6-1). 6 có phải kết quả đúng mong muốn? | NEW-46 · A2 Carbon diffInMonths | PO / người phụ trách sprint |
| 2 | PayPal 「課金管理」 `/admin/user-point-settings` throw Undefined variable (PB-43845-3, chưa có mã PB): ghi PB mới hay **xoá màn** (thêm vào ignore-features)? | NEW-480 | Leader |
| 3 | 「支払履歴」 cũ `/basic/download-invoice` trang trắng (PB-T21-17): giữ hay xoá route (ignore-features)? | NEW-639 | Leader |
| 4 | `.env UNIVAPAY_EXPIRED_TRANSFER` production có đặt không (hạn chuyển khoản 14 vs 30 ngày)? | NEW-543 | Dev |
| 5 | PB-T22-4: đổi thẻ hợp đồng có `cvv_authorize = null` có thể ném TypeError ở PHP8 (UnivapayPayment.php:1178) — nếu tái hiện thì task cha phải xử lý | NEW-545 | Dev + Leader |
| 6 | Mốc **延滞 bao nhiêu ngày** thì job **hủy cưỡng chế** HĐ (強制解約)? Cần chốt để viết expected TC-FUNC001-03 (MC4) | §7 TC-FUNC001-03 · memory `billing-recontract-rules` | Dev + Leader |
| 7 | **MobileNotify loại 3 (order notify)**: spec `db-mapping` ghi `order_item_id` = id order, nhưng thực tế lưu **`form_answer_result.id`** (memory `mobile-notify-order-item-id`). Sửa db-mapping cho đúng | §7 TC-DATADB001-01 · memory `mobile-notify-order-item-id` | Dev |
| 7 | **NEW-534** (job gửi mail gia hạn chuyển khoản) **Không đạt — bug 44584**: xác nhận fix trước khi kết luận MC6 (mail chuyển khoản) đạt | NEW-534 · §7 TC-NOTIMAIL001-01 | Dev |

---

# BATCH B2 — Booking Salon / Lesson / Event

## 0. Nguồn TC
- **Nguồn đã dùng**: MCP LME TEST STUDIO — task_id=507, ticket 43845 (subset B2 lọc theo `screen`/`viewpoint`: salon/lesson/event booking, 予約カレンダー, スタッフ, Google Calendar/Sheet sync, カレンダー予約 cũ).
- **Tổng số TC review**: 173 — nhưng **21 TC lọt nhầm batch** (khớp từ `staff`/`予約`): 12 TC staff-permission Friend List (REQ-RG-FRI-01: NEW-1381/1501-1511) → thuộc **B4**; 5 TC 配信予約/送信予約/アクション予約 (NEW-206/207/292/1083/1271) → **B3a/Chat**; 2 TC 絞り込み予約後配信 (NEW-1044/1045) → **B4**; NEW-1274 サロンコース絞り込み giữ ở B2. → **~152 TC booking thật** được review.

> **Đã áp [framework/php-upgrade-checklist.md](../../framework/php-upgrade-checklist.md)**. Rủi ro chính của booking khi nâng PHP là **A2 (Carbon diffIn*/ngày giờ)** — và đây là nơi bộ TC **phủ dày nhất**: thời lượng khối course, lịch qua nửa đêm 23:00→01:00, đệm trước/sau không lấn ngày, 受付開始 theo số ngày, khung 24:00, biên 0-9h JST. Vấn đề của B2 là **1 TC fail chưa ticket + chưa thực thi đủ** (39% pass, 0 prd) + **30 TC draft chưa chạy/thiếu mã**.

## 1. Coverage — dev-impact + diff code

- **dev-impact: CHƯA ĐỦ (chưa xác nhận + 1 fail).** T3/T6/T20 (salon/lesson/event booking, slot calc) có TC Normal+Abnormal+Boundary dày. **Nhưng** 68/173 pass (39%), **NEW-222 fail**, 0 prd.
- **diff code: CHƯA ĐỦ (chưa xác nhận).** `requirement_keys` REQ-T6 (slot/diffIn), REQ-T20 (booking flow), REQ-RG-BKG, REQ-T2 (message template) đều có TC. Chiều A2 (điểm sửa diffIn/Carbon) phủ rất tốt; không thấy điểm sửa thiếu TC thiết kế.

| Mã | Chiều | Vùng ảnh hưởng | TC hiện có | Status | Ghi chú |
|---|---|---|---|---|---|
| R1 | dev-impact | **NEW-222 fail** (đặt/huỷ lesson từ trang khách + admin) | NEW-222 | **RISK/[BLOCKER]** | fail, **chưa raise ticket** → §5. Phải xác định lỗi thật hay môi trường |
| R2 | dev-impact + diff | Booking slot / Google Calendar-Sheet sync chạy **production** (RULE-08 domain/job) | NEW-35-43 (slot/diffIn), NEW-385-395 (Google sync), NEW-217-219 (LIFF) đều env=dev/local | **RISK** | RULE-08: Google sync (domain/token/job nền) + slot không kết luận từ dev. Scope phải chứa `prd` |

**Kết luận §1**: 0 GAP · 2 RISK (R1 fail NEW-222, R2 exec/prd). Thiết kế A2/slot đủ; coverage chưa xác nhận (39% pass + 1 fail + 0 prd).

## 2. Thiếu so với quan điểm test

**Kết luận**: quét theo màn (salon/lesson/event) + checklist A/B/C — **không thiếu quan điểm thiết kế lớn**. Bảng độ phủ:

| Mục checklist | Trạng thái B2 | TC tiêu biểu |
|---|---|---|
| A2 ngày giờ/Carbon diffIn (rủi ro #1 của booking) | ✅ phủ rất dày | NEW-35 (thời lượng khối course), NEW-38 (qua nửa đêm 23:00→01:00), NEW-39 (đệm không lấn ngày), NEW-40/41 (受付開始 N ngày biên), NEW-223 (khung 24:00), NEW-221 (時間 mặc định), NEW-540 n/a |
| A1 sort stable | ✅ phủ | NEW-1322 (削除済み予約 sort + tham số rỗng #44201), NEW-1546 (booking cùng trạng thái tie) |
| A3 tiền | ✅ 1 phần (thanh toán booking ở B1) | NEW-1552 (course giá 0 không thu tiền) |
| A4 null/TypeError | ✅ phủ | NEW-34/209 (id không tồn tại → 404), NEW-214/216 (addHours ép (int) Carbon 3), NEW-1346 (số lượng phải nguyên) |
| A6 type juggling | ✅ phủ đúng điểm | NEW-219 (`'0 == "unlimited"'` PHP7 true → sửa `=== "unlimited" \|\| === 0`), NEW-224 (quantity ép float như 7.2) |
| B Google Calendar/Sheet (lib) | ✅ phủ | NEW-42/43 (busy block theo phút/nhiều ngày), NEW-385-388 (2 chiều + refresh token), NEW-393-395 (Sheet 11 cột), NEW-218 (Sheet lỗi vẫn huỷ + result_error_google) |
| C APP_KEY / Google token giải mã | ✅ phủ | NEW-387/394 (Google thu hồi quyền liên kết cũ), NEW-388 (refresh token), NEW-54 note (token cũ không nhập lại) |

**Điểm mờ duy nhất — 受付上限 option matrix** (memory salon-limit-4-options / salon-noshift-course-slot-rule #43379): B2 cover store-limit=1 (NEW-37) + staff 上限を設定しない/1 (NEW-219). **Chưa thấy TC cho limit N≥2 và option "店舗 合計" (option 3), 指定なし course slot (#43379)**. Vì upgrade chỉ chạm toán tử so sánh (NEW-219 đã cover path `0/unlimited`) nên dùng chung đường — đề xuất 1 regression TC ở §7 (R1) cho N≥2 để chắc, matrix đầy đủ đã thuộc kho FA-020.

## 3. TC trùng lặp

Đã rà 152 TC booking — **không phát hiện trùng**. Các cụm NEW-1552-1557 (lesson msg duyệt/từ chối đặt/huỷ) · NEW-1383-1386 (sửa/xoá khung, dữ liệu cũ, sort, validate) là **tách atomic có chủ đích** (ghi rõ note "tách từ NEW-xxx"). Giữ nguyên.

## 4. Mâu thuẫn trong TCs

Đã rà 152 TC × spec `salon-booking`/`lesson-booking`/`event-booking` + kho `fa019`/`fa020`/`fa021` — **không phát hiện mâu thuẫn TC-vs-TC / TC-vs-kho**. 1 điểm khác-production chủ đích đưa §8: NEW-218 (Sheet lỗi INVALID_ARGUMENT: nhánh mới catch Throwable huỷ tiếp vs production để lỗi lọt).
- **CONF-IGNORE** (`ignore-features.md` IG-01 — Booking Manager cũ 「カレンダー予約」 admin): **NEW-34, NEW-101, NEW-209** verify màn admin `/basic/manager-booking` **vẫn 404 như production** (tính năng đã khai tử 07/2025). Theo rule IG-01 → đề nghị cân nhắc xoá các TC này; **NHƯNG** ở task upgrade chúng có giá trị "xác nhận route chết không hồi sinh" → **để Leader chốt** (giữ như regression-dead-route hay xoá). ⚠️ **NEW-102/214/835** (trang KHÁCH đặt lịch cũ `/app-booking-calendar` + LIFF redirect sang salon/lesson) **KHÔNG thuộc IG-01** — luồng khách cũ vẫn active, là regression hợp lệ, giữ.

## 5. Issues khác

| # | Severity | TC / phạm vi | Vấn đề | Đề xuất |
|---|---|---|---|---|
| 1 | `[BLOCKER]` | NEW-222 (`fail`, **bug=[]**) | TC `fail` nhưng **chưa raise ticket** — đặt/huỷ lesson từ trang khách + admin (luồng chính booking) | Raise ticket hoặc xác định lỗi môi trường trước khi review tiếp |
| 2 | `[BLOCKER]` | Toàn batch B2 (152 booking thật) | **~39% pass** (68/173; bỏ 21 TC lọt nhầm thì 68/152≈45%). skip 74 · chưa chạy 28 · error 2 · fail 1 | Chạy lại trên QA PHP 8.5 có Google test + user LINE test + prd |
| 3 | `[MAJOR] RULE-08` | Google Calendar/Sheet sync + slot (env dev 134 · local 11 · **prd 0**) | Task chạm **domain/token/job nền** (Google sync 2 chiều, refresh token LOA) mà 0 TC chạy prd | Scope phải chứa `prd`; chạy thật Google sync + đặt/huỷ qua LIFF trên thiết bị thật |
| 4 | `[MINOR]` | 30 TC `viewpoint`=None, chưa chạy (NEW-1383-1386, 1546, 1552-1557, 1250/1251 + 12 TC lọt nhầm) | Thiếu mã quan điểm → không map coverage; phần lớn là draft "CẦN XÁC NHẬN baseline" | Gán mã quan điểm + chốt baseline base trước khi chạy |
| 5 | `[MINOR]` phân loại | 21 TC lọt nhầm batch (§0) | Staff-permission Friend List + 配信予約/送信予約 bị gộp vào "booking" do từ khoá | Review đúng chỗ: B4 (friend/permission) · B3a (broadcast/chat schedule) |

Chất lượng từng TC: **xuất sắc** — tự đầy đủ, oracle = production/base commit, nêu rõ điểm Carbon/diffIn bị chạm + PB-xx + điều kiện môi trường (LIFF/Google/thiết bị thật).

## 6. TCs thừa / ngoài phạm vi task

Đã rà 152 TC booking — **không có TC thừa/ngoài phạm vi #43845**. 21 TC lọt nhầm batch (§0, §5-5) KHÔNG phải thừa — chúng thuộc #43845 nhưng sai batch, review ở B4/B3a. TC IG-01 (NEW-34/101/209) xử lý ở §4 CONF-IGNORE.

## 7. TCs đề xuất bổ sung (10)

Đã đối chiếu 152 TC + spec `salon-booking`/`lesson-booking` + kho `fa019`/`fa020`/`fa021` + checklist A/B/C.

> **Bổ sung 2026-10-27 — rà riêng Lesson 「レッスン予約」 (FA-019) theo 8 maincase** (69 TC lesson). 6/8 ĐỦ: MC1 CRUD lịch+course+slot (52/53/55/56/73/74/1383/1384) · MC2 giờ slot+nhắc A2 (223/646/1323/234/550) · MC3 remind job (1557) · MC4 Google Sheet sync 4 type (393/1252/1254/1259/1253) · MC7 đặt từ LINE/LIFF (1245/102) · MC8 list/sort A1 + JP A5 + null A4 (1322/413/1547-1551/1550). 2 gap → 2 TC: **MC5** friend_info format (LIFF mảng / admin object / app không sửa — **0 TC**, memory) · **MC6** 定員 FULL + キャンセル待ち + 承認方式=3 no-cancel + hạn huỷ (NEW-222 chỉ đặt/huỷ cơ bản). ⚠️ **NEW-1322 lộ bug #44201** (bản mới trả 500/trống khi `sortStatus` rỗng, Laravel 5.5 sắp mới→cũ) — đã có ticket, theo dõi.

| ID | Nhóm | Mã quan điểm | Màn hình/chức năng | Loại case | Chạy | Phạm vi ENV | Surface | Tên case | Tiền điều kiện | Các bước thực hiện | Dữ liệu nhập | Kết quả mong đợi | Kết quả thực thi | Ghi chú |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TC-FUNC001-01 | UI | FUNC-001 | Salon 「予約カレンダー」: 受付上限 theo nhân viên N≥2 và 店舗合計 (option 3) chặn đúng khi đạt N | Boundary | manual | dev, local, prd, staging | line-friend | Khung salon đạt đúng N lượt nhận đồng thời (N=2) với giới hạn theo nhân viên và giới hạn 店舗合計 | Lịch salon スタッフタイプ 2 nhân viên NV1/NV2 ca 10:00–18:00 ngày D, course 60 phút. Cài (a) 「スタッフごとの同時受付上限」 NV1 = 2; (b) chạy lại với 店舗の受付上限 = 「合計」 N=2. User test U1/U2/U3 | 1. Cài NV1 limit=2. 2. U1, U2 đặt NV1 khung 10:00 ngày D (2 lượt cùng lúc). 3. U3 xem/đặt NV1 khung 10:00 → quan sát. 4. Đổi cài sang 店舗合計=2, lặp với 2 nhân viên khác nhau cùng khung | N=2 (staff limit + store 合計) | Sau 2 lượt 10:00: khung 10:00 của NV1 đầy, U3 không đặt được (「"指定なし"の受付上限数に達しています」 / khung mờ); khung giờ khác còn trống. Với 店舗合計=2: đạt 2 lượt bất kỳ nhân viên nào thì mọi nhân viên bị chặn khung đó — giống production (toán tử so sánh limit sau fix `'0==unlimited'`) | | Lấp R1/§2 · regression toán tử limit bị chạm (NEW-219 path) · bổ sung N≥2 + option 合計 (memory salon-limit-4-options) · manual vì cần user LINE thật · Đánh giá spec: Spec ghi rõ (salon-booking 受付上限) |
| TC-FRIEND001-02 | Data | FRIEND-001 | レッスン予約: friend_info khi đặt lịch — LIFF luôn lưu **mảng**, admin tạo lưu **object**; app KHÔNG sửa được friend info | Normal | manual | dev, local, prd, staging | line-friend, web, mobile-app | Đặt lịch lesson qua LIFF → friend_info lưu dạng **mảng**; admin tạo đơn hộ → lưu dạng **object**; app LME không sửa được friend info của booking | Bot test có lesson calendar + course + form câu hỏi gắn friend_info field. Friend F01 (LINE thật). Admin đăng nhập web. App LME có màn booking lesson. Mốc production + memory lesson-booking-friend-info-format | 1. F01 đặt lịch qua LIFF, trả lời câu hỏi gắn friend_info → kiểm DB `friend_information_value`/payload booking: định dạng **mảng**. 2. Admin tạo đơn hộ cho F01 trên web, nhập friend_info → kiểm định dạng **object**. 3. Trên app LME mở booking, thử sửa friend_info → xác nhận **không có đường sửa** (read-only). 4. So production | LIFF booking + admin booking cùng field friend_info | LIFF lưu friend_info dạng **mảng** (array); admin tạo lưu dạng **object** — đúng production (2 nguồn 2 format). App LME **không** cho sửa friend info của booking. Đọc cả 2 format không 500/TypeError (A4). Giống production | | Lấp MC5 (friend_info format — 0 TC) · dẫn từ memory lesson-booking-friend-info-format · regression đọc/ghi friend_info array vs object dưới PHP8 (A4 cấu trúc) · manual (LIFF + app thật) · Đánh giá spec: Đã hỏi leader (Leader chốt: LIFF mảng / admin object / app không sửa) |
| TC-FUNC004-01 | API | FUNC-004 | レッスン予約: 定員 FULL → chặn đặt + キャンセル待ち; 承認方式=3 không cho huỷ; quá hạn huỷ chặn | Boundary | manual | dev, local, prd, staging | line-friend, web | Khung đầy 定員 → khách không đặt được, đăng ký キャンセル待ち; có người huỷ → khung còn chỗ/thông báo waitlist; 承認方式=3 ẩn nút huỷ; quá hạn huỷ bị chặn | Lesson calendar: 1 khung 定員=2 đã đầy (2 booking), bật 「空き枠通知」(キャンセル待ち); 1 khung đặt 承認方式=3 (không cho huỷ); 1 khung có hạn huỷ (trước 1 ngày). Friend F01/F02/F03 (LINE thật). Mốc production | 1. F03 mở LIFF chọn khung đầy → xác nhận không đặt được, đăng ký 「キャンセル待ち」. 2. F01 huỷ booking khung đó → 残り tăng + F03 (waitlist) nhận thông báo trống chỗ. 3. Khung 承認方式=3: mở 予約履歴 → xác nhận KHÔNG có nút 予約をキャンセルする. 4. Khung có hạn huỷ: thử huỷ sau hạn → bị chặn message đúng. 5. So production | khung 定員=2 full · 承認方式=3 · khung quá hạn huỷ | Khung đầy: không đặt được, đăng ký キャンセル待ち OK; có người huỷ → 残り cập nhật + waitlist được 空き枠通知. 承認方式=3: không hiện nút huỷ (SCR-LSN-13). Quá hạn huỷ: bị chặn message đúng. 定員/残り tính đúng (không âm/không vượt). Không 500. Giống production | | Lấp MC6 (NEW-222 chỉ đặt/huỷ cơ bản; thiếu 定員 FULL + キャンセル待ち + 承認方式=3 + hạn huỷ) · regression F2/F8 (overlap/limit check) + A4 · manual (LIFF thật) · Đánh giá spec: Spec ghi rõ (FA-019 SCR-LSN-13/L10/L15, 定員) |
| TC-FUNC004-02 | API | FUNC-004 | サロン 受付上限: phân biệt đếm chỗ **option 1.1 (1 staff làm trọn, không ghép) vs 1.2 (tiếp sức ≥2 staff)** cho đơn 指定なし | Boundary | manual | dev, local, prd, staging | line-friend, web | Cùng dữ liệu 2 staff ca lệch nhau + course 2h + 指定なし: option 1.1 → khung KHÔNG đặt được; option 1.2 → đặt được (tiếp sức) | Lịch salon 2 staff NV-A ca 10:00–11:00, NV-B ca 11:00–12:00, course 2 tiếng, mỗi staff limit 1. Chạy 2 lần: (a) 受付上限=1.1 (1人で対応); (b) =1.2 (2人以上で交代). Đơn 指定なし. Mốc production + memory salon-limit-4-options/option2-relay (kho TC-SLN) | 1. Cài option 1.1, khách 指定なし chọn course 2h khung 10:00–12:00 → quan sát. 2. Đổi option 1.2, lặp. 3. So production | 2 staff ca lệch, course 2h, 指定なし, option 1.1→1.2 | Option **1.1**: khung 10:00–12:00 **KHÔNG đặt được** (không staff rảnh trọn 2h). Option **1.2**: **đặt được** (NV-A→NV-B tiếp sức phủ trọn). Đếm chỗ đúng từng option (A6 so sánh limit, không lọc theo hàm diff). Giống production | | Lấp MC2 (phân biệt 1.1/1.2 — Studio chỉ có NEW-37/opt3) · pickup kho **TC-SLN** (matrix 受付上限) chạy regression PHP8 (A6) · manual (LIFF thật) · Đánh giá spec: Spec ghi rõ (4 option) + Leader chốt 2026-10-20 |
| TC-FUNC004-03 | API | FUNC-004 | サロン #43379: đơn 指定なし thuộc course KHÔNG staff (đang có ca) làm được → **không chiếm suất** (áp 1.1/1.2/2) | Boundary | manual | dev, local, prd, staging | line-friend | Đơn 指定なし của course không ai đảm nhận/không ai có ca phù hợp không chiếm chỗ khung → khung vẫn đặt được course khác | Lịch salon có course X (chỉ NV-A đảm nhận) + course Y (NV-B đảm nhận). Khung T chỉ NV-B có ca (NV-A nghỉ). Option 1.1 (lặp 1.2, 2). Mốc production + memory salon-noshift-course-slot-rule (#43379, re-test #42335 chưa cover) (kho TC-SLN) | 1. Khách chọn 指定なし + course X tại khung T (NV-A nghỉ) → quan sát có chiếm suất không. 2. Khách khác chọn course Y khung T → xác nhận vẫn đặt được. 3. Lặp option 1.2, 2. 4. So production | course X (NV-A nghỉ) · course Y (NV-B có ca) · khung T | Đơn 指定なし course X (không ai làm được ở khung T) **không chiếm suất** khung T; course Y vẫn đặt được (#43379, áp 1.1/1.2/2). Option 3 chờ #43447 (không test). Không âm/vượt 定員. Giống production | | Lấp MC4 (#43379 — memory ghi "359 TC re-test #42335 chưa cover") · pickup kho TC-SLN · regression F2/F8 slot-count PHP8 · manual · Đánh giá spec: Đã hỏi leader (#43379 áp 1.1/1.2/2, opt 3 chờ #43447) |
| TC-INTGCAL001-01 | API | INTG-CAL-001 | サロン: cấm liên kết **trùng Google Calendar giữa 2 staff cùng 1 lịch salon**; khác lịch salon thì được | Abnormal | manual | dev, local, prd, staging | web | 2 staff CÙNG calendar salon không được liên kết cùng 1 Google Calendar; 2 staff khác calendar salon thì được | Lịch salon S1 có NV-A, NV-B; lịch S2 có NV-C. 1 Google Calendar GC1. Admin đã liên kết GC1 cho NV-A (S1). Mốc production + memory salon-google-calendar-link-rule | 1. Thử liên kết GC1 cho NV-B (cùng S1) → xác nhận bị **chặn** (message đúng). 2. Liên kết GC1 cho NV-C (khác lịch S2) → xác nhận **được**. 3. So production | GC1 · NV-A/NV-B (S1) · NV-C (S2) | Liên kết GC1 cho NV-B cùng S1 **bị chặn**; cho NV-C (lịch khác S2) **thành công**. Không 500. Giống production | | Lấp MC5 (cấm trùng Google cal giữa staff cùng salon — 0 TC) · dẫn từ memory salon-google-calendar-link-rule · manual (Google thật) · Đánh giá spec: Đã hỏi leader |
| TC-APICONTRACT001-01 | API | API-CONTRACT-001 | API app salon — mã HTTP: chặn nghiệp vụ **200 + result=error**; thao tác booking **bot khác → 403/404** | Abnormal | auto | dev, local, prd, staging | mobile-app, api | Lỗi nghiệp vụ (khung đầy/quá hạn) trả 200+result=error; truy cập booking bot KHÁC (IDOR) trả 403/404 | 2 bot: Bot-A (user token app), Bot-B (có booking B-BK). Khung đầy + khung quá hạn ở Bot-A. Mốc production + memory salon-app-api-http-codes | 1. Gọi API app đặt/thao tác khung đầy/quá hạn Bot-A → kiểm HTTP 200 + body result=error. 2. Dùng token Bot-A gọi API xem/thao tác booking B-BK của Bot-B → kiểm HTTP **403/404**. 3. So production | khung đầy/quá hạn Bot-A · booking B-BK Bot-B | Chặn nghiệp vụ (đầy/quá hạn): HTTP **200** + `result=error` (không 500). Truy cập booking bot khác: HTTP **403 hoặc 404** (chặn IDOR cross-bot), không lộ dữ liệu Bot-B. Giống production | | Lấp MC8 (rule HTTP code app — memory salon-app-api-http-codes) · regression F15 IDOR + API contract PHP8 · auto · Đánh giá spec: Đã hỏi leader (business-block 200+error; other-bot 403/404) |
| TC-STATE001-01 | API | STATE-001 | サロン LIFF: **キャンセルリクエスト** — request KHÔNG giữ suất sai + chặn admin xóa khung khi có request chờ | Normal | manual | dev, local, prd, staging | line-friend, web | Khách gửi キャンセルリクエスト (chưa duyệt) → suất giữ như 予約確定 đến khi duyệt; admin bị chặn xóa khung đang có request chờ | Lịch salon có 承認方式 cho キャンセルリクエスト. Khách F01 đã 予約確定 khung T, gửi キャンセルリクエスト (trạng thái 8, chờ admin duyệt). Mốc production + memory salon-lesson-booking-rules | 1. F01 gửi キャンセルリクエスト cho booking khung T. 2. Kiểm suất khung T **chưa được giải phóng** đến khi admin duyệt. 3. Admin thử **xóa khung T** (đang có request chờ) → xác nhận **bị chặn**. 4. Admin duyệt → lúc đó mới giải phóng suất. 5. So production | booking khung T + キャンセルリクエスト chờ | キャンセルリクエスト chờ **không giải phóng suất sai** (giữ như 予約確定 đến khi duyệt); admin **không xóa được khung** đang có request chờ; sau duyệt mới giải phóng. Không 500. Giống production | | Lấp MC9 (キャンセルリクエスト không giữ suất + chặn xóa khung — 0 TC) · dẫn từ memory salon-lesson-booking-rules · manual (LIFF thật) · Đánh giá spec: Đã hỏi leader |
| TC-FUNC001-05 | UI | FUNC-001 | サロン admin: đặt/duyệt **vượt chỗ (overbook)** được + **không có nút rút hủy** booking | Normal | manual | dev, local, prd, staging | web | Admin đặt/duyệt đơn vượt 定員 của khung (overbook) thành công; UI admin KHÔNG có nút rút hủy/hoàn tác hủy | Lịch salon khung T đã đạt 定員. 1 đơn chờ duyệt / キャンセルリクエスト ở khung T. Admin đăng nhập. Mốc production + memory salon-lesson-booking-rules | 1. Admin tạo đơn mới / duyệt request cho khung T **đã đầy** → xác nhận **đặt/duyệt được vượt chỗ**. 2. Rà màn quản lý đơn + 予約履歴 → xác nhận **không có nút rút hủy**. 3. So production | khung T đầy 定員 + đơn chờ | Admin **đặt/duyệt vượt 定員** thành công (overbook được phép cho admin, khác khách bị chặn); **KHÔNG có nút rút hủy** trên UI admin. Số liệu khung đúng dù vượt. Không 500. Giống production | | Lấp MC10 (admin overbook + không nút rút hủy — memory salon-lesson-booking-rules) · manual · Đánh giá spec: Đã hỏi leader |
| TC-FUNC004-04 | API | FUNC-004 | イベント予約: số lượng đặt phải **nguyên trong [1, 1回の予約上限]**; khung đầy 定員 → chặn; param số lượng không gây lỗi SQL (F8 vá binding) | Boundary | manual | dev, local, prd, staging | line-friend, api | Đặt sự kiện qua LIFF với số lượng biên (0/âm/vượt 1回の予約上限/non-integer) bị chặn đúng; khung đầy 定員 chặn; param số lượng chứa ký tự SQL không injection | Sự kiện có khung 13:00–15:00 定員=5, 「1回の予約上限」=3. Khách F01 (LINE thật) qua LIFF. Mốc production + dev-impact F8 (MobileEventBookingController::handleKeepSlot) | 1. F01 đặt số lượng hợp lệ (2) → OK, 残り giảm. 2. Đặt số lượng 0 / âm (-1) / 4 (vượt 1回上限=3) / "2abc" (non-integer) → mỗi cái bị chặn message đúng, không ghi DB. 3. Đặt khi khung đã đạt 定員=5 → chặn (満員). 4. Gửi param số lượng chứa `' OR 1=1`/SQL → không injection, trả lỗi chuẩn. 5. So production | số lượng 2 · 0 · -1 · 4 · "2abc" · SQL; khung đầy | Số lượng hợp lệ [1,3] đặt được, 残り/定員 cập nhật đúng (không âm/vượt). Số lượng 0/âm/>3/non-integer → chặn message đúng, không ghi DB record rác (A4). Khung đầy 定員 → 満員 chặn. Param số lượng không gây SQL error/injection (F8 binding vá). KHÔNG 500/TypeError PHP8. Giống production | | Lấp MC3 (F8 diff — handleKeepSlot: số lượng nguyên [1,1回の予約上限] + capacity + binding SQL; NEW-224 chỉ happy định mức 5/đặt 2) · regression F8 (MobileEventBookingController) + A4 · manual (LIFF thật) · Đánh giá spec: Spec ghi rõ (FA-021, dev-impact F8) |

> **Bổ sung 2026-10-27 — rà riêng Event 「イベント予約」 (FA-021) theo 6 maincase.** 5/6 ĐỦ: MC1 CRUD sự kiện+ngày+khung (103/104/105/261/262/263/264/266) · MC2 ngày/slot A2 (104/266/290) + remind A2 cross-ref B3a (TC-FUNCDATE001-02, リマインド=event) · MC4 remind job cross-ref B3a · MC5 LIFF đặt (224/335/749) · MC6 list/CSV (103/290/397) + null (264/239). 1 gap → **TC-FUNC004-04** MC3 F8 capacity/limit/binding-SQL (NEW-224 chỉ happy). A1 tie-sort event list + A5 tên sự kiện JP = light, không đẻ TC (chia sẻ path với lesson/salon).

> **Bổ sung 2026-10-27 — rà riêng Salon (FA-020) theo 10 maincase** (114 TC salon). 4/10 ĐỦ (MC1 CRUD · MC3 slot qua đêm/buffer · MC5.1 Google Sheet · MC6 remind · MC7 CSV). 6 ô trống đúng **6 rule memory** mà bộ Studio #43845 thiếu (kho FA-020 có nhưng KHÔNG nằm trong run Studio) → 6 TC trên (pickup kho `TC-SLN-*` nơi có, chạy regression PHP8): **MC2** 1.1/1.2 (A6) · **MC4** #43379 指定なし no-occupy · **MC5** cấm trùng Google cal giữa staff cùng salon · **MC8** mã HTTP app (200+error / other-bot 403/404) · **MC9** キャンセルリクエスト (không giữ suất, chặn xóa khung) · **MC10** admin overbook + không nút rút hủy. Memory: salon-limit-4-options · salon-limit-option2-relay-rule · salon-noshift-course-slot-rule · salon-google-calendar-link-rule · salon-app-api-http-codes · salon-lesson-booking-rules. (TC-FUNC001-01 salon opt-3 ở trên giữ nguyên.)

## 8. Spec update needed

| # | Điểm cần chốt | Nguồn | Ai chốt |
|---|---|---|---|
| 1 | Huỷ lịch salon khi Google Sheet lỗi INVALID_ARGUMENT: nhánh mới **catch Throwable → huỷ vẫn hoàn tất + báo Chatwork** (KHÁC production để lỗi lọt). Hành vi mới có đúng mong muốn? | NEW-218 · PB-T20-2 | PO / Leader |
| 2 | TC IG-01 (NEW-34/101/209 verify 「カレンダー予約」 admin 404): giữ làm regression-dead-route hay xoá theo ignore-features? | §4 CONF-IGNORE | Leader |
| 3 | NEW-222 fail chưa ticket: xác định lỗi thật (đặt/huỷ lesson) hay môi trường → raise ticket nếu thật | NEW-222 | Dev + QA |

---

# BATCH B4 — Friend / Tag / Filter / CSV / Cross-analysis

## 0. Nguồn TC
- **Nguồn đã dùng**: MCP LME TEST STUDIO — task_id=507, ticket 43845 (subset B4: 友だちリスト, 絞り込み filter, タグ管理, 友だち情報管理, CSV管理, クロス分析, データコピー, ブロック/非表示 + staff-permission Friend List gộp từ B2).
- **Tổng số TC review**: 269 (gồm 12 TC staff-permission Friend List gộp từ B2 + 2 TC filter 予約後配信).

> **Đã áp [framework/php-upgrade-checklist.md](../../framework/php-upgrade-checklist.md)**. Đây là **batch kém trưởng thành nhất** đến giờ: chỉ **28.6% pass** (77/269), **121 TC chưa chạy** (45%), **118 TC thiếu mã quan điểm** (gần nửa batch), rất nhiều TC ghi "CẦN XÁC NHẬN EXPECTED/baseline — giữ draft, không pass trước khi có baseline". Thiết kế filter rộng nhưng **chưa chạy + chưa chốt oracle base**.

## 1. Coverage — dev-impact + diff code

- **dev-impact: CHƯA ĐỦ (chưa xác nhận).** F2 (orWhere mảng — đếm bạn bè/filter), T5 (friend/tag/filter/CSV/cross) có TC thiết kế rộng. **Nhưng** 28.6% pass, 45% chưa chạy, nhiều TC chưa chốt baseline → coverage chưa xác nhận.
- **diff code: CHƯA ĐỦ (chưa xác nhận).** `requirement_keys` REQ-T4 (search/param), REQ-RG-FRI, REQ-B2B83/B3B97 (IDOR cross-bot), REQ-RG-MKT (data-copy) đều có TC. G-11 (`str_contains → Str::contains` needle rỗng) được cover bởi cụm search ký tự đặc biệt.

| Mã | Chiều | Vùng ảnh hưởng | TC hiện có | Status | Ghi chú |
|---|---|---|---|---|---|
| R1 | diff | **orWhere mảng (F2) — filter bạn bè / đếm số người** chạy thật + chốt baseline | NEW-1368/1449-1459 (AND/OR, friend-info, date biên, validation), NEW-22 (tag AND/OR), NEW-1500/1534 (cách ly bot, phân trang) — **toàn bộ exec=None** | **RISK** | Thiết kế đủ ma trận filter nhưng **0 TC đã chạy** + đa số chưa có baseline base → chưa xác nhận orWhere compat |
| R2 | diff | **IDOR cross-bot** (B2B83/B3B97) — friend-info/tag/data-copy của bot khác bị chặn | NEW-1338 (友だち情報管理 IDOR), NEW-1500 (tìm tên trùng 2 bot cách ly) | **RISK** | NEW-1338 đang `error` (chưa có kết luận) → §5 |
| R3 | dev-impact + diff | Friend/tag/CSV/cross-analysis chạy **production** (ES sync, CSV encoding, job linect) | NEW-573 (CSV), NEW-699 (data-copy), NEW-1159 (cross-copy) env=dev/local | **RISK** | RULE-08: ES sync / job nền / CSV domain không kết luận từ dev |
| G4 | dev-impact + diff | **Xoá friend cascade ~30 bảng** (T5 + A4) + kết bạn lại không hồi sinh + performance (#38390) | NEW-1261 chỉ dọn bản ghi giới hạn tag khi bulk-xoá 非表示; NEW-1483/1487/1479 chỉ kiểm "xoá đúng người" | **GAP** | Kho FA-013 group 14 (TC-FRL-136/141/142) là ma trận cascade đầy đủ; bộ Studio KHÔNG có TC cascade toàn bảng. Soft-delete + `LegacyQueryBuilder` đổi ở Laravel13/PHP8 → §7 G4 |
| G5 | dev-impact + diff | **Export CSV danh sách friend đã gắn giá trị** 1 trường friend info (F11 Excel 4 + A5 encoding) | NEW-127 chỉ "mở danh sách" theo 回答人数; KHÔNG có TC tải CSV | **GAP** | Kho FA-015 group 5 (TC-FRI-325→329) là ma trận export; bộ Studio friend-info KHÔNG có TC download CSV. Excel 4 + `mb_convert_encoding` Shift_JIS đổi ở PHP8 → §7 G5 |

**Kết luận §1**: 2 GAP (G4 cascade-delete · G5 CSV export friend-info) · 3 RISK. Thiết kế filter/IDOR đủ; coverage chưa xác nhận do exec cực thấp + baseline chưa chốt. _(G4+Q5 rà cụm Friend list; G5+Q6 rà cụm Friend info — bổ sung 2026-10-27 theo maincase, xem §7.)_

## 2. Thiếu so với quan điểm test

**Kết luận**: quét theo màn + checklist — ma trận filter (memory feedback-filter-regression-matrix: 5 kịch bản · friend-info · tag AND+OR) **có thiết kế**, không thiếu quan điểm lớn. Độ phủ:

| Mục checklist | Trạng thái B4 | TC tiêu biểu |
|---|---|---|
| A6 type juggling (filter / orWhere / LIKE) — rủi ro chính F2 | ✅ thiết kế rộng (chưa chạy) | NEW-1368 (AND+OR), NEW-1449-1451 (giữ/sửa/xoá nhóm), NEW-1457 (info text), NEW-1452-1456 (validate từng loại điều kiện), NEW-22 (tag 'tất cả'/'một trong') |
| A2 date filter JST | ✅ thiết kế (chưa chạy) | NEW-1458 (ngày thêm bạn 2 mốc biên, không lệch UTC) |
| A4 null/search edge | ✅ thiết kế | NEW-1417/1425-1428 (search rỗng/`?`/`"`/`%`/`_` — G-11 `str_contains` needle rỗng) |
| IDOR cross-bot (SEC/PERM-002) | ✅ thiết kế | NEW-1338, NEW-1500 (cách ly dữ liệu 2 bot) |
| C APP_KEY / ES sync | gián tiếp | NEW-1500 (đọc dữ liệu đã đồng bộ, không cần job ES mới) |

**Điểm mờ** (light Q, không đẻ TC — thuộc kho FA-013): friend-info **kiểu điểm 7 điều kiện** / **kiểu ngày 4 điều kiện** (memory friend-info-filter-conditions) — B4 cover text + ngày-biên, chưa thấy đủ 7 điều kiện kiểu điểm. Ma trận điều kiện đầy đủ thuộc kho FA-013; upgrade chỉ cần đại diện orWhere (đã có) → không đẻ lại (AP-5).

| Q5 | `FUNC-FILTER-001` + **ma trận filter bắt buộc** (F2 orWhere subquery + A6) | Cao | Ma trận filter bắt buộc (memory feedback-filter-regression-matrix) gồm **5 kịch bản (scenario, incl `is_deleted`)**. Bộ Studio chỉ cover **tag(AND/OR) + friend-info(text) + date-biên** — **chưa có TC lọc theo tình trạng kịch bản / conversion**, là shape orWhere khác (subquery/join) của F2. Các tiêu chí QR/対応status/affiliater/新規既存 được cover qua filter dùng chung ở từng màn (NEW-1043→1054) → không đẻ lại (AP-5) | `[MAJOR]` → §7 Q5 |
| Q6 | `FRIEND-001` + **A6 (rẽ nhánh `type_data`)** | Cao | Action khi set/đổi giá trị friend info rẽ theo `type_data`: 選択肢→actionId · ポイント→settingActions · 年月日→sinh/huỷ lịch gửi. Studio chỉ cover select-option (NEW-2137-2139) + date-config (NEW-2140); **chưa có point→settingActions và value-change→huỷ/sinh-lại lịch** (kho TC-FRI-238/239) | `[MAJOR]` → §7 Q6 |

## 3. TC trùng lặp

Đã rà 269 TC — **không phát hiện trùng**. Cụm NEW-14xx (search tên full/partial, ký tự ?/"/%/_, validate từng loại điều kiện) là **tách atomic 1-mục-tiêu/TC có chủ đích** (ghi rõ "Tách tình huống theo yêu cầu QA 26/10, mỗi TC một mục tiêu Pass/Fail"). Giữ nguyên.

## 4. Mâu thuẫn trong TCs

Đã rà 269 TC × spec `friend-list`/`friend-filter`/`friend-information`/`tag-management`/`csv-management` + kho `fa012`/`fa013`/`fa015`/`fa033` — **không phát hiện mâu thuẫn TC-vs-TC / TC-vs-kho**.
- ⚠️ **Rủi ro oracle**: rất nhiều TC filter ghi "**Expected chưa được xác nhận phải lấy baseline trước chấm, không coi là pass**" và "không tự đặt business rule mới". Đây KHÔNG phải mâu thuẫn nhưng là **thiếu chuẩn đánh giá** → mọi kết luận "đủ" ở §1 giữ RISK tới khi có baseline base (ghi §5).
- **CONF-IGNORE**: không có (B4 không chạm IG-01).

## 5. Issues khác

| # | Severity | TC / phạm vi | Vấn đề | Đề xuất |
|---|---|---|---|---|
| 1 | `[BLOCKER]` | Toàn batch B4 | **28.6% pass** (77/269) · **121 chưa chạy (45%)** · skip 61 · error 8 · fail 2. Kém trưởng thành nhất các batch | Chạy lại + chốt baseline base trước khi kết luận coverage |
| 2 | `[BLOCKER]` | 6 TC `fail`/`error` **bug=[]**: NEW-699, NEW-1338, NEW-1159, NEW-1212, NEW-1213, NEW-1214 | Data-copy / 友だち情報管理 IDOR / cross-analysis copy / richmenu-filter-modal đang `error`, chưa có kết luận, chưa raise ticket (NEW-1212-1214 thực ra là richmenu B3b lọt vào do 'filter') | Triage: lỗi môi trường vs lỗi thật → raise ticket nếu thật |
| 3 | `[MAJOR]` | **118 TC `viewpoint`=None** (NEW-14xx + 12 permission) | Gần nửa batch không map được coverage theo 80 quan điểm; nhiều TC còn ở trạng thái draft "CẦN XÁC NHẬN baseline" | Gán mã quan điểm + chốt baseline base (ưu tiên trước khi giao chạy) |
| 4 | `[MAJOR] RULE-08` | Friend/tag/CSV/cross/data-copy (env dev 141 · local 7 · **prd 0**) | ES sync, CSV encoding, job linect, data-copy không kết luận từ dev | Scope chứa `prd`; chạy thật CSV export/import + data-copy + cross-analysis trên prd |
| 5 | `[MINOR]` phân loại | NEW-1212/1213/1214 (richmenu filter modal), NEW-1044/1045 (filter 予約後配信), NEW-1274 | Lọt vào B4 do từ 'filter'/'絞り込み' — thực thuộc B3b (richmenu) / B2 (booking filter) | Đối chiếu đúng batch khi tổng hợp |

Chất lượng từng TC: nội dung tốt, tự đầy đủ, oracle = base — **nhưng** rất nhiều TC **chưa chốt được expected** (ghi "CẦN XÁC NHẬN"), là draft chờ baseline, không phải TC hoàn chỉnh.

## 6. TCs thừa / ngoài phạm vi task

Đã rà 269 TC — **không có TC thừa/ngoài phạm vi #43845**. Các TC lọt nhầm batch (§5-5) thuộc #43845, review đúng chỗ ở B3b/B2.

## 7. TCs đề xuất bổ sung (14)

Đã đối chiếu 269 TC + spec `friend-filter`/`friend-information`/`tag-management` + kho `fa012`/`fa013`/`fa015` + checklist. Ma trận filter đã có thiết kế rộng (AND/OR, friend-info, date biên, validation, IDOR cách ly) → với **phần đó không đẻ TC mới**; việc cần làm là (a) **chạy** 121 TC chưa chạy; (b) **chốt baseline base** cho các TC "CẦN XÁC NHẬN EXPECTED"; (c) **gán mã quan điểm** cho 118 TC (thêm TC lúc baseline chưa chốt là vô nghĩa — AP-5).

> **Bổ sung 2026-10-27 — rà riêng cụm Friend list (FA-013) theo 7 maincase** (đối chiếu 159 TC friend-list-cluster + kho `fa013`). 5/7 maincase ĐỦ hoặc RISK-do-môi-trường (1 List/sort — NEW-1440 cover A1 stable-tie · 5 Search/paging — NEW-648 cover Laravel5.5 pagination-compat · 6 Date JST — NEW-287/288 · 3 shared-filter mỗi màn — NEW-1043→1054 · 7 inline action — NEW-110/1372/1382/1462/1538). **2 vùng code KHÁC path chưa cover** → 2 TC bên dưới: **G4** cascade-delete ~30 bảng + re-follow (maincase 4, kho TC-FRL-136/141/142) · **Q5** scenario/conversion filter (maincase 2/3, "5 kịch bản" bắt buộc). Đã đối chiếu kho FA-013 — 2 TC đều có bản kho, dẫn chiếu ID, không trùng bộ BƯỚC 0.

> **Bổ sung 2026-10-27 (bis) — rà riêng cụm Quản lý friend info (FA-015) theo 7 maincase** (đối chiếu 94 TC friend-info-cluster + kho `fa015`). 5/7 maincase ĐỦ hoặc RISK-do-môi-trường (1 CRUD trường + folder-sort · 2 các kiểu trường select/記述/年月日/ポイント/画像/PDF — NEW-123/2116-2133 · 5 Folder CRUD/sort + JP label A5 — NEW-2135/2163-2172 · 6 input config rỗng — NEW-126/2134/2136; tất cả `exec=None` → chạy + chốt baseline như B4 §5). **2 vùng code KHÁC path chưa cover** → 2 TC: **G5** export CSV danh sách friend gắn giá trị (maincase 7, kho TC-FRI-325/328) · **Q6** A6 rẽ nhánh `type_data` khi set/đổi giá trị (maincase 3, kho TC-FRI-235/238/239). Phần media value upload image/PDF (maincase 4) cover representative qua NEW-853 + media B3b — không đẻ lại (AP-5). Đã đối chiếu kho FA-015, không trùng bộ BƯỚC 0.

> **Bổ sung 2026-10-27 (ter) — rà riêng màn Chi tiết bạn bè 「友だち詳細」 (FA-038) theo 8 maincase** (đối chiếu 188 TC friend-detail). Hiển thị 7 tab + sửa friend info (A5 NEW-1647 / A2 NEW-1641-1642, 60 TC) + tag (118/1654-1657) + memo (117/120/160/1648-1653) + block/unblock/xoá (31 TC; cascade ~30 bảng + A4 dùng chung **EP-08** với G4 `TC-DATAREF001-01`) cover **rất tốt**. 4 ô trống đẻ thêm 4 TC: **MC4** gán/đổi rich menu cho friend (EP-34 LINE SDK v12 — 0 TC) · **MC1.4** 表示設定 (chọn/sắp xếp mục) bảng 基本情報/友だち情報 + filter tab フォーム回答 (chỉ có TC display) · **MC1.2** sort tab booking **Lesson/Event** + tie-stability A1 (chỉ Salon có NEW-1687-1690) · **MC8** format ngày giờ JST xuyên tab (A2/F4). Ghi chú Leader (không đẻ TC): **MC5** 'gửi tin inline' — màn chỉ có nút チャット→/basic/chat-v3 (B6); action-inline đã cover qua NEW-118 (tag có action)/NEW-1646 (選択肢 có action) · **MC1.5** filter lịch sử **rich menu** chưa có TC (QR đã có NEW-1693-1695) · **MC7** BR-17 memo 2 cột `bot_line_user.memo`/`conversation.memo` không sync (→ §8). Đã đối chiếu spec FA-038, không trùng bộ BƯỚC 0.

> **Bổ sung 2026-10-27 — rà riêng Backup / データコピー (LOA→LOA) theo 6 maincase** (NEW-698/699/752/869/873/877/878/880/941/942/881). ĐỦ: MC1 khởi chạy copy + E2E (698/699/873) · MC4 tiến trình/trạng thái (699/873) · MC6 ngày tạo/hoàn tất A2 (880/698). CHƯA ĐỦ: MC2 deep-copy chỉ verify event (880) + auto-reply FK (941/942) · **MC3 rich menu re-register LINE API = 0 TC** · MC5 JP sau copy chưa verify. 2 gap đúng điểm nóng upgrade → 2 TC: **MC3** rich menu re-register LINE API sau copy (F6 SDK v12) · **MC2+MC5** deep-copy FK remap đa loại (scenario/template/tag/form/richmenu) + JP A5. ⚠️ NEW-699 (E2E copy) đang `error` (B4 §5-2).

| ID | Nhóm | Mã quan điểm | Màn hình/chức năng | Loại case | Chạy | Phạm vi ENV | Surface | Tên case | Tiền điều kiện | Các bước thực hiện | Dữ liệu nhập | Kết quả mong đợi | Kết quả thực thi | Ghi chú |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TC-DATAREF001-01 | Data | DATA-REF-001 | Danh sách bạn bè 「友だちリスト」 — Xoá friend (cascade ~30 bảng) + kết bạn lại | Normal | manual | dev, local, prd, staging | web, mobile-app | Xoá friend đầy đủ dữ liệu → dữ liệu liên quan xoá cascade, màn reload được; kết bạn lại KHÔNG hồi sinh dữ liệu cũ (A4) | Admin bot đã liên kết LINE OA. 1 friend F01 có ĐẦY ĐỦ dữ liệu: url rút gọn + lượt click, form answer, event/lesson/salon booking, item đơn + chu kỳ, tag, friend info, memo, lịch sử scenario, lịch sử hiển thị rich menu. Ghi đủ danh sách trước xoá. Có mốc hành vi production. (ref kho TC-FRL-136/141/142) | 1. /basic/friendlist (hoặc /hidden //user-block //block) chọn F01, bấm 削除, xác nhận; đo thời gian màn phản hồi. 2. Kiểm màn reload được ngay, F01 biến mất. 3. Mở URL分析 / form result / event list — dữ liệu F01 không còn tính/hiển thị. 4. Từ app LINE cho F01 kết bạn lại. 5. Mở chi tiết F01 mới, rà 13 mục lịch sử (kết bạn/友だち情報/memo/tag/salon-lesson-event/item/form/QR/richmenu/scenario). 6. F01 click lại url cũ, trả lời form, đặt event mới | 1 friend F01 đầy đủ 13 loại dữ liệu | Màn KHÔNG treo loading vô hạn, hoàn tất trong thời gian chấp nhận (ghi số thực để Leader chốt ngưỡng — Bug #38390). F01 biến mất; url/form/event của F01 không còn tính/hiển thị. Sau kết bạn lại: TẤT CẢ 13 mục lịch sử TRỐNG (không hồi sinh); click url/trả lời form/đặt event đều ghi nhận MỚI bình thường. KHÔNG 500/TypeError PHP8 trong cascade. Giống production | | Lấp G4 (maincase 4 — cascade ~30 bảng + A4 + PERF #38390) · regression DATA-REF dưới Laravel13/PHP8 (soft-delete + `LegacyQueryBuilder`) · dẫn từ kho TC-FRL-136/141/142 · manual vì cần dữ liệu đầy đủ + re-follow LINE thật + đo performance · ENV chứa prd (RULE-08 cascade/performance) · Đánh giá spec: Đã hỏi leader (kho: dữ liệu cũ không hồi sinh) |
| TC-FUNCFILTER001-01 | UI | FUNC-FILTER-001 | 友だちリスト — 絞り込み: lọc theo tình trạng kịch bản (5 trạng thái, incl `is_deleted`) + conversion, AND/OR | Normal | auto | dev, local, staging | web | Lọc bạn bè theo điều kiện kịch bản (5 trạng thái đăng ký) và conversion, kết hợp AND/OR → tập người trùng khít base (orWhere subquery compat) | Bot test có kịch bản S (có bạn 購読中/完了/停止, có bản ghi `is_deleted`=1/NULL), conversion CV. Dataset biết trước ai thuộc điều kiện nào. Có mốc base release_step_20260930_v2 cùng dataset (oracle = tập người bản cũ). Memory: dòng `is_deleted` 1/NULL bị bỏ qua ở cả 5 điều kiện; cặp bù nhau không trùng người | 1. Mở 絞り込み, thêm điều kiện 「シナリオ」 lần lượt từng trạng thái trong 5 trạng thái, ghi số người từng cái. 2. Thêm điều kiện 「コンバージョン」 CV. 3. Tổ hợp 1 nhóm AND (scenario + conversion) và 1 nhóm OR. 4. Mỗi cấu hình đọc 対象人数 + danh sách. 5. So từng tập với mốc base cùng dataset | scenario S (5 trạng thái, có `is_deleted` 1/NULL), conversion CV; AND/OR combos | Mỗi điều kiện scenario/conversion + tổ hợp AND/OR trả tập người + 対象人数 **trùng khít base** (PHP7.2/Laravel5.5). Dòng `is_deleted`=1/NULL bị bỏ qua đúng (không lọt vào bất kỳ trong 5 trạng thái); cặp điều kiện bù nhau không trùng người. orWhere mảng lồng (subquery scenario/conversion) cho kết quả y hệt — không sai do A6 type juggling / compat layer | | Lấp Q5 (maincase 2/3 — ma trận filter mandated "5 kịch bản"; scenario/conversion filter chưa cover) · regression F2 (orWhere mảng lồng subquery) + A6 · dẫn từ memory scenario-filter-is-deleted-rule + feedback-filter-regression-matrix · auto · Đánh giá spec: Đã hỏi leader (rule `is_deleted` — Leader chốt, spec chưa ghi) |
| TC-OUTEXPORT001-01 | API | OUT-EXPORT-001 | 友だち情報管理（情報一覧） — Export CSV danh sách friend đã gắn giá trị 1 trường | Normal | auto | dev, local, prd, staging | web, api | Export CSV danh sách friend gắn giá trị (toàn bộ / chọn vài bạn / 0 bạn) — encoding + ký tự đặc biệt giữ như production | Admin bot gói trả phí, màn 友だち情報管理. Trường 選択肢 「FI-CSV」 có ≥3 friend gắn giá trị; 1 giá trị chứa **dấu phẩy, xuống dòng, dấu ngoặc kép**. Có mốc file production cùng dữ liệu | 1. Mở 情報一覧 của 「FI-CSV」 (số 回答人数). 2. Bấm export CSV (toàn bộ) → tải file. 3. Export khi CHỌN 2 bạn → tải. 4. Export trường có 0 bạn → tải. 5. Mở các file bằng hex + Excel JP; so với file production | Trường 選択肢 FI-CSV, 1 giá trị chứa `, " \n` | Mỗi lần tải được file CSV; nội dung + số dòng khớp lựa chọn (toàn bộ / 2 bạn / chỉ header khi 0 bạn). Charset Shift_JIS (như production), giá trị chứa `, " \n` escape đúng như production, ký tự JP/①㈱/emoji xử lý y hệt production, byte khớp file production. KHÔNG 500/TypeError PHP8 (Excel 4 / `mb_convert_encoding`) | | Lấp G5 (maincase 7 — download CSV danh sách friend gắn giá trị) · regression F11 Export CSV (Excel 4) + A5 encoding dưới PHP8 · dẫn từ kho TC-FRI-325/326/327/328 · auto · ENV chứa prd (RULE-08 CSV encoding, theo B4 §5-4) · Đánh giá spec: Spec ghi rõ (OUT-EXPORT) + checklist A5 |
| TC-FRIEND001-01 | UI | FRIEND-001 | 友だち情報管理 — Action theo `type_data` khi set/đổi giá trị (選択肢→actionId · ポイント→settingActions · 年月日→sinh/huỷ lịch) | Normal | manual | dev, local, prd, staging | web, line-friend | Set/đổi giá trị từng kiểu trường → đúng nhánh action (A6 `type_data`); line user nhận đúng | Bot test có friend F01 (LINE thật). 3 trường: 選択肢 FI-SEL (option X gắn action gửi tin T), ポイント FI-PT (settingActions khi đạt mốc), 年月日 FI-DATE (action gửi tin kiểu 当日/指定). Có mốc hành vi production | 1. Màn admin set FI-SEL của F01 = option X → quan sát LINE F01. 2. Set FI-PT đạt mốc kích settingActions → quan sát. 3. Set FI-DATE = ngày tương lai gần → kiểm lịch gửi sinh (操作予約); đổi FI-DATE sang giá trị KHÔNG còn thoả → lịch bị huỷ; đổi về thoả lại → lịch sinh lại. 4. Mỗi nhánh kiểm tin trên LINE F01 + lịch sử | FI-SEL=X; FI-PT=mốc; FI-DATE=ngày tương lai→đổi | Mỗi kiểu đi đúng nhánh `type_data` (A6): 選択肢→chạy action theo actionId của option X (F01 nhận tin T); ポイント→settingActions chạy đúng khi đạt mốc; 年月日→sinh lịch gửi đúng mốc JST, đổi giá trị sang-không-thoả thì **huỷ** lịch, đổi về thoả thì **sinh lại** (TC-FRI-238/239). Không chạy nhầm nhánh kiểu khác; line user nhận/không-nhận đúng quy tắc. Giống production | | Lấp Q6 (maincase 3 — A6 rẽ nhánh `type_data`; point→settingActions + value-change→huỷ/sinh-lại lịch chưa cover) · regression A6 (switch `type_data` ở `FriendInformationController`) · dẫn từ kho TC-FRI-235/238/239 · manual vì cần LINE app thật · Đánh giá spec: Đã hỏi leader |
| TC-FUNC001-02 | UI | FUNC-001 | Chi tiết bạn bè 「友だち詳細」: gán/đổi/gỡ 表示中リッチメニュー cho 1 friend (EP-34 qua LINE API) | Normal | manual | dev, local, prd, staging | web, line-friend | Gán rich menu cho friend từ màn chi tiết → rich menu trên LINE của friend đổi đúng + DB cập nhật; đổi sang cái khác và gỡ cũng đúng, giống bản cũ | Admin bot đã liên kết LINE OA, có ≥2 rich menu đã đẩy lên LINE (RM-A, RM-B). Friend F01 đã kết bạn (LINE thật), 表示中リッチメニュー hiện RM-A (hoặc trống). Có mốc hành vi production | 1. Mở 友だち詳細 F01, mục 「表示中リッチメニュー」, chọn RM-B, lưu. 2. Trên LINE F01 kiểm rich menu hiển thị. 3. DB `bot_line_user.rich_menu_id`. 4. Đổi về RM-A rồi gỡ (không chọn), kiểm lại LINE + DB | RM-A, RM-B; friend F01 | Gán RM-B: rich menu trên LINE F01 đổi sang RM-B (EP-34 gọi LINE API thành công, builder SDK v12 đúng), `bot_line_user.rich_menu_id`=id RM-B. Đổi/gỡ phản ánh đúng trên LINE + DB. Không 500/lỗi SDK. Giống production | | Lấp MC4 (save rich menu cho friend — 0 TC) · regression F6/LINE SDK v12 EP-34 (richmenu LINE API) · manual vì cần LINE thật · ENV chứa prd (RULE-08 LINE-facing) · Đánh giá spec: Spec ghi rõ (FA-038 field 4, EP-34) |
| TC-FUNCDATE001-01 | UI | FUNC-DATE-001 | Chi tiết bạn bè: định dạng ngày giờ JST nhất quán xuyên 7 tab (A2/F4 LegacyDateSerialization) | Normal | auto | dev, local, prd, staging | web | Mọi mốc ngày giờ hiển thị ở các tab giữ đúng định dạng + múi giờ JST như bản cũ sau nâng PHP8/Laravel13 | Friend F01 có dữ liệu ở mọi tab: ngày kết bạn (followed_at), tin cuối, remind (終了日時/次回配信), booking salon/lesson/event (参加日時), 購入日時 (単品+継続), lịch sử quét QR (time), friend-info kiểu 年月日. Có mốc hiển thị production cùng dữ liệu | 1. Mở 友だち詳細 F01. 2. Lần lượt mở 基本情報 + 6 tab còn lại, ghi mọi giá trị ngày giờ hiển thị. 3. So từng giá trị với mốc production (định dạng + giờ JST) | friend F01 đủ dữ liệu các tab | Mọi ngày giờ hiển thị đúng định dạng production (vd `Y-m-d H:i:s`) và **đúng JST** — không lệch UTC, không đảo ngày/tháng, ngày chuỗi "0"/null không hiện sai (A2 Carbon diffIn* signed · F4 `LegacyDateSerialization`). Trùng khít mốc bản cũ ở mọi tab. Không 500 | | Lấp MC8 (format ngày giờ JST xuyên tab — 0 TC chuyên) · regression A2/F4 (ngày giờ JSON + Carbon) dưới PHP8 · auto · Đánh giá spec: Spec không ghi (quy tắc PHP8, so mốc bản cũ) |
| TC-LIST001-02 | UI | LIST-001 | Chi tiết bạn bè: 表示設定 (chọn + sắp xếp mục) bảng 基本情報/友だち情報 + tab フォーム回答 filter/phân trang giữ như bản cũ | Normal | auto | dev, local, staging | web | Lưu cấu hình 表示設定 (mục nào hiện + thứ tự) + filter/phân trang tab form answer → persist + render đúng như production | Friend F01 có nhiều friend-info field + ≥6 form answer (để phân trang 5). Có mốc production của cùng cấu hình 表示設定 + cùng dữ liệu form | 1. Mở 友だち詳細 F01, bấm 「表示設定」 trên bảng 基本情報 và 友だち情報: bỏ tick vài mục + đổi thứ tự, lưu. 2. Reload, kiểm 2 bảng hiển thị đúng tập mục + thứ tự đã lưu. 3. Mở tab フォーム回答, phân trang 5 + dùng filter (nếu màn có), đối chiếu mốc production | cấu hình 表示設定 (ẩn mục X + đổi thứ tự) | 表示設定 lưu server-side, sau reload 2 bảng chỉ hiện mục đã chọn theo đúng thứ tự (như production). Tab フォーム回答 phân trang 5 + filter trả đúng tập, định dạng ngày/nội dung như bản cũ. Không 500 | | Lấp MC1.4 (表示設定 chọn/sắp xếp mục + filter — chỉ có TC display) · regression hiển thị-config dưới Laravel13 · auto · ⚠️ Leader xác nhận 表示設定 áp cho bảng nào + tab form có filter không · Đánh giá spec: Spec ghi rõ (FA-038 SCR-FMP-01 表示設定, SCR-FMP-07 paginate 5) |
| TC-FUNCSEQ001-02 | UI | FUNC-SEQ-001 | Chi tiết bạn bè — tab booking: sort cột tab **Lesson + Event** + tie-stability A1 (bổ sung cho Salon NEW-1687-1690) | Normal | auto | dev, local, staging | web | Sort các cột ở tab Lesson và Event đúng chiều + khi trùng khoá giữ thứ tự chèn như bản cũ, giống cơ chế Salon đã có | Friend F01 có ≥3 booking Lesson (khác tên/trạng thái/ngày, trong đó **≥2 trùng khoá sort**) và ≥3 booking Event tương tự. Có mốc thứ tự production (dùng Salon NEW-1687-1690 làm chuẩn cơ chế) | 1. Mở 友だち詳細 F01, tab Lesson: sort từng cột có sort (tên/ngày/trạng thái) asc + desc, ghi thứ tự + các dòng trùng khoá. 2. Lặp cho tab Event. 3. So với mốc production | F01 có booking Lesson/Event, ≥2 dòng trùng khoá sort/tab | Sort Lesson + Event đúng chiều asc/desc như Salon; các dòng **cùng khoá sort** giữ thứ tự chèn như PHP7.2 (PHP8 `sort` stable — A1). Không tab nào đảo thứ tự so với bản cũ. Không 500 | | Lấp MC1.2 (sort Lesson/Event — chỉ Salon có NEW-1687-1690) + A1 tie-stability · regression · auto · Đánh giá spec: Spec không ghi chi tiết sort (so mốc bản cũ) |
| TC-DATABACKUP001-01 | API | DATA-BACKUP-001 | データコピー: sau copy, rich menu bot đích **đăng ký lại với LINE API** (SDK v12) + hiển thị đúng trên LINE | Normal | manual | dev, local, prd, staging | web, line-friend | Copy data có rich menu từ LOA-A→LOA-B: rich menu được push lên LINE account bot đích, friend bot đích thấy đúng | Bot nguồn LOA-A có ≥1 rich menu đã đẩy lên LINE (ảnh + vùng tap + action). Bot đích LOA-B đã liên kết LINE OA riêng, chưa có rich menu. Có mã copy của LOA-A. Friend F01 là bạn LOA-B (LINE thật). Mốc production | 1. Màn 「データコピー」 của LOA-B: nhập mã LOA-A, chạy copy tới hoàn tất. 2. Kiểm rich menu xuất hiện ở /basic/rich-menu của LOA-B (ảnh/vùng/action đúng). 3. Kiểm rich menu được **đăng ký lên LINE API** của LOA-B (richMenuId mới thuộc LOA-B, không phải của LOA-A). 4. Gán cho F01 / mở LINE F01 xem rich menu | mã copy LOA-A (có rich menu) | Rich menu copy sang LOA-B đầy đủ (ảnh/vùng tap/action remap đúng bot đích); được **đăng ký lại với LINE API** của LOA-B (SDK v12 build + push thành công, richMenuId thuộc LOA-B). F01 thấy rich menu đúng trên LINE. Không 500/lỗi SDK trong copy. Giống production | | Lấp MC3 (rich menu re-register LINE API sau copy — 0 TC) · regression F6 LINE SDK v12 (richmenu create/upload LINE) trong luồng copy · manual vì cần 2 LINE OA + app thật · ENV chứa prd (RULE-08 LINE-facing) · Đánh giá spec: Đã hỏi leader (hành vi production) |
| TC-DATAREF001-02 | Data | DATA-REF-001 | データコピー: deep-copy remap FK đúng đa loại (scenario/template/tag/form/richmenu) + không mất/lệch bản ghi + JP không mojibake (A5) | Normal | manual | dev, local, prd, staging | web | Copy đầy đủ LOA-A→LOA-B: mọi loại data sang đủ, FK trỏ nội bộ bot đích (không trỏ nhầm bot nguồn), số bản ghi khớp, nội dung JP nguyên vẹn | Bot nguồn LOA-A có dữ liệu đa loại **có ký tự JP** + FK lồng: scenario (step→template), template (text JP + emoji), tag (có action_id), form (fields), rich menu, event. Ghi đủ số lượng + FK từng loại. Bot đích LOA-B trống. Có mã copy. Mốc production | 1. Chạy copy LOA-A→LOA-B tới hoàn tất. 2. Mỗi loại (scenario/template/tag/form/richmenu/event): đếm số bản ghi LOA-B = LOA-A. 3. Kiểm FK: scenario.step→template_id, tag.action_id, form field FK… đều trỏ bản ghi **của LOA-B** (không còn id của LOA-A). 4. Kiểm nội dung JP (template text `①㈱🎉`, tên tag JP) không mojibake. 5. So với production | dữ liệu đa loại có JP + FK lồng | Mọi loại copy **đủ số bản ghi** (không mất/trùng/lệch); FK remap **trỏ nội bộ LOA-B** (không trỏ nhầm LOA-A — trỏ nhầm = rò rỉ chéo bot); nội dung JP/emoji **nguyên vẹn** (A5 utf8mb4 giữ qua copy). Không 500/TypeError PHP8 trong deep-copy (F2 query builder). Giống production | | Lấp MC2 (deep-copy FK remap đa loại — chỉ 880 event + 941/942 auto-reply) + MC5 (JP A5 sau copy) · regression F2 (query builder trong replicate) + A5 encoding · manual (dữ liệu đa loại) · ENV chứa prd (RULE-08 data) · Đánh giá spec: Đã hỏi leader |
| TC-FUNCFILTER001-02 | UI | FUNC-FILTER-001 | 友だちリスト — 絞り込み (modal filter): OR 3 điều kiện khác loại (tag + 友だち情報 text + 友だち追加日時) | Boundary | auto | dev, local, staging | web | Lọc OR với 3 điều kiện khác loại cùng lúc → union đúng, người khớp nhiều điều kiện chỉ 1 dòng, trùng khít base (orWhere mảng lồng ≥3 nhánh) | Bot test có 6 friend U1..U6 (chỉ dữ liệu test). U1=tag A·友だち情報 FI-TXT「alpha」·ngày thêm bạn 2026-01-10; U2=tag A·FI-TXT「beta」·2026-03-01; U3=không tag A·FI-TXT「alpha」·2026-02-15; U4=tag A·FI-TXT「gamma」·2026-05-20; U5=không tag A·FI-TXT「beta」·2026-01-05; U6=không tag A·FI-TXT「delta」·2026-06-01. Có mốc base release_step_20260930_v2 cùng dataset (oracle = tập người bản cũ). | 1. Mở 「友だちリスト」 → 「絞込み」, chọn tab 「どれか1つ以上満たす」 (OR).<br>2. Thêm điều kiện 「タグ」 = tag A.<br>3. Thêm điều kiện 「友だち情報」 FI-TXT khớp giá trị 「alpha」.<br>4. Thêm điều kiện 「友だち追加日時」 khoảng 2026-02-01..2026-02-28.<br>5. Lưu, đọc 対象人数 + danh sách ID.<br>6. So tập người + số với mốc base cùng dataset. | OR 3 điều kiện: tag A · FI-TXT=alpha · ngày 2026-02 | Kết quả = U1,U2,U3,U4 (tổng 4): U1 khớp cả tag+alpha nhưng chỉ 1 dòng (không nhân bản); U5,U6 bị loại (không thoả điều kiện nào). Tập người + 対象人数 trùng khít base PHP7.2/Laravel5.5. orWhere mảng lồng 3 nhánh cho kết quả y hệt — không sai do F2 compat layer / A6 type juggling. Không lỗi 500 hoặc lỗi JS mới; ngoại lệ đã được chấp nhận của base không tính hồi quy. | | Lấp gap [MAJOR] filter — OR ≥3 điều kiện khác loại (orWhere mảng lồng, điểm nóng F2); hiện chỉ có OR 2 điều kiện (NEW-109) · regression F2 + A6 · dẫn từ feedback-filter-regression-matrix (AND+OR) · auto · Đánh giá spec: Đã hỏi leader (so mốc bản cũ) |
| TC-FUNCFILTER001-03 | UI | FUNC-FILTER-001 | 友だちリスト — 絞り込み (modal filter): AND 3 điều kiện gồm loại trừ tag + 友だち情報 kiểu điểm (≥) + 友だち追加日時 | Boundary | auto | dev, local, staging | web | Lọc AND 3 điều kiện gồm loại trừ (không có tag) + toán tử số ≥ + khoảng ngày → giao đúng, trùng base (where mảng lồng + A6 so sánh kiểu số) | Bot test có 6 friend U1..U6 (chỉ dữ liệu test). U1=tag A·友だち情報 FI-PT(ポイント)=50·ngày 2026-01-10; U2=tag A·FI-PT=200·2026-03-01; U3=không tag A·FI-PT=100·2026-02-15; U4=tag A·FI-PT=10·2026-05-20; U5=không tag A·FI-PT=300·2026-01-05; U6=không tag A·FI-PT=250·2026-06-01. Có mốc base cùng dataset (oracle = tập người bản cũ). Memory: 友だち情報 kiểu điểm có 7 điều kiện (Leader chốt). | 1. Mở 「絞込み」 tab 「全て満たす」 (AND).<br>2. Thêm điều kiện 「タグ」 chế độ loại trừ: KHÔNG có tag A.<br>3. Thêm điều kiện 「友だち情報」 FI-PT (ポイント) toán tử ≥ 100.<br>4. Thêm điều kiện 「友だち追加日時」 khoảng 2026-01-01..2026-05-31.<br>5. Lưu, đọc 対象人数 + danh sách ID.<br>6. So với mốc base cùng dataset. | AND: không-tag-A · FI-PT≥100 · ngày 2026-01-01..05-31 | Kết quả = U3,U5 (tổng 2): U1,U2,U4 loại vì có tag A; U6 loại vì ngày 06-01 ngoài khoảng; U4 cũng loại vì FI-PT=10<100. Tập + 対象人数 trùng khít base. Toán tử ≥ so sánh đúng kiểu số (không bị A6 type juggling '100' vs 100 dưới PHP8); where mảng lồng 3 nhánh + loại trừ cho kết quả y hệt bản cũ. Không lỗi 500 hoặc lỗi JS mới; ngoại lệ base không tính hồi quy. | | Lấp gap [MINOR] filter — AND ≥3 điều kiện + loại trừ + toán tử số (NEW-1441 chỉ 2 điều kiện) · regression F2 (where mảng lồng) + A6 (so sánh số) · dẫn từ memory friend-info-filter-conditions · auto · Đánh giá spec: Đã hỏi leader (kiểu điểm 7 điều kiện — spec chưa ghi) |
| TC-FUNCBULK001-01 | UI | FUNC-BULK-001 | 友だちリスト — Modal アクション (友だち一括アクション): chuỗi 3 action khác loại trong 1 lần thực thi | Normal | auto | dev, local, staging | web, job | Cấu hình 3 action khác loại (gắn tag + ghi friend info + bắt đầu scenario) trong 1 modal, thực thi 1 lần → cả 3 áp đúng theo thứ tự cho đúng người được chọn | Admin bot test. 3 friend U1,U2 (sẽ chọn) + U3 (không chọn), chỉ dữ liệu test. Có tag T_RES (0 người), trường friend info X (rỗng ở U1,U2,U3), scenario S (bước đầu gửi text, có lịch). Ghi trạng thái trước thao tác. Có mốc hành vi production. | 1. Mở 「友だちリスト」, tick U1,U2 (để U3 không chọn); kiểm 「選択中 2 人」.<br>2. Mở 「アクション選択」 (modal 友だち一括アクション).<br>3. Thêm action 1: gắn tag T_RES.<br>4. Thêm action 2: ghi friend info X = 「BULK_VAL」.<br>5. Thêm action 3: bắt đầu scenario S.<br>6. Xác nhận thứ tự 3 action, bấm 「上記アクションを実行」 một lần.<br>7. Mở タグ管理 / chi tiết U1,U2,U3 + trạng thái scenario: kiểm tag, info, đăng ký scenario, lịch sử.<br>8. Đối chiếu mốc production. | 3 action: +tag T_RES · info X=BULK_VAL · start scenario S; chọn U1,U2 | Chỉ U1,U2 nhận cả 3 kết quả: có tag T_RES (số người tag=2), info X=「BULK_VAL」, đăng ký scenario S (trạng thái 購読中, bước đầu theo lịch). U3 không đổi (không tag, info rỗng, không đăng ký). 3 action áp theo đúng thứ tự cấu hình; lịch sử ghi đủ 3 thao tác. Không lỗi 500/TypeError PHP8 trong payload gộp (F2); ngoại lệ base không tính hồi quy. Giống production. | | Lấp gap [MAJOR] action — chuỗi action KHÁC LOẠI trong 1 lần (hiện chỉ NEW-1465 chạy 2 action cùng loại tag) · regression F2 (payload action gộp) + luồng job scenario · dẫn từ review 2 modal shared 2026-10-29 · auto (kiểm qua DB/lịch sử, không cần realtime LINE) · Đánh giá spec: Đã hỏi leader (hành vi production) |
| TC-FUNCBULK001-02 | UI | FUNC-BULK-001 | 友だちリスト — Modal アクション: nhiều action, mỗi action gắn bộ lọc 絞り込み riêng | Normal | auto | dev, local, staging | web | Cấu hình 2 action, mỗi action có điều kiện lọc riêng trong modal action → mỗi action chỉ áp cho tập friend khớp filter của riêng nó | Admin bot test gói Standard/Pro (Free bị chặn mở bộ lọc trong modal action). 4 friend U1,U2,U3,U4 sẽ chọn, chỉ dữ liệu test. U1=tag A·ngày thêm bạn 2026-01-10; U2=tag A·2026-03-01; U3=không tag A·2026-02-15; U4=tag A·2026-05-20. Có tag T1 (0 người), trường info Y (rỗng). Có mốc production. | 1. Mở 「友だちリスト」, chọn U1,U2,U3,U4.<br>2. Mở 「アクション選択」.<br>3. Action 1: gắn tag T1; bấm đặt điều kiện lọc → modal 「絞り込み」 thêm 「タグ」 = tag A (AND), lưu quay lại.<br>4. Action 2: ghi info Y=「F2」; đặt điều kiện lọc → 「友だち追加日時」 khoảng 2026-01-01..2026-02-28, lưu quay lại.<br>5. Bấm 「上記アクションを実行」 một lần.<br>6. Lọc theo T1 và kiểm info Y của từng friend; đối chiếu mốc production. | action1 +T1 filter(tag A); action2 Y=F2 filter(ngày 2026-01..02) | Action 1 chỉ gắn T1 cho friend trong lựa chọn CÓ tag A = U1,U2,U4 (U3 không được gắn). Action 2 chỉ ghi Y=「F2」 cho friend trong lựa chọn thuộc khoảng ngày = U1,U3 (U2,U4 ngoài khoảng). U1 nhận cả 2 (khớp cả 2 filter). Mỗi action đánh giá filter độc lập, không áp nhầm chéo; không ai bị bỏ sót/áp dư. Không lỗi 500/lỗi JS; ngoại lệ base không tính hồi quy. Giống production. | | Lấp gap [MINOR] action — nhiều action mỗi cái 1 filter riêng (NEW-1049 chỉ 1 action+1 filter) · regression F2 (filter mảng lồng per-action) · dẫn từ review 2 modal shared 2026-10-29 · auto · Đánh giá spec: Đã hỏi leader |

## 8. Spec update needed

| # | Điểm cần chốt | Nguồn | Ai chốt |
|---|---|---|---|
| 1 | **Baseline base cho ma trận filter** (ký tự `?`/`"`/`%`/`_` trong search; validation từng loại điều kiện tag/info/date; biên ngày JST): rất nhiều TC chưa có expected chốt, phải chạy base release_step_20260930_v2 cùng dataset ghi oracle **trước** khi chấm | NEW-1417/1425-1428, NEW-1452-1458, NEW-1368 | QA + Dev (ghi oracle base) |
| 2 | Ma trận quyền staff Friend List (6 bề mặt: list/filter/action/hidden/admin-block/user-block): "CẦN XÁC NHẬN MA TRẬN QUYỀN — chưa có evidence quyền độc lập". Chốt quyền thực tế trước khi chạy | NEW-1381/1501-1511 (12 TC) | Leader + Dev |
| 3 | NEW-1338 (友だち情報管理 IDOR cross-bot) đang error: xác định chặn 403 đúng như base chưa | NEW-1338 | Dev |
| 4 | **BR-17 (FA-038)**: memo lưu `bot_line_user.memo` (khi có `id`) HAY `conversation.memo` (khi có `conversation_id`) — **2 cột không sync** (POTENTIAL BUG). Chốt 1 nguồn chuẩn + xác nhận compat/binding không làm lệch nơi đọc-ghi memo | FA-038 BR-17 · NEW-117/1648 · memory `memo-bot-id-zero-recovered` | Dev + Leader |
| 5 | Màn 友だち詳細 có nút **"gửi tin inline"** riêng không, hay chỉ `チャット`→/basic/chat-v3 (thuộc B6)? MC5 hiện chỉ cover action-inline qua tag/選択肢 (NEW-118/1646) — xác nhận không thiếu đường gửi | FA-038 header actions | Leader |

---

# BATCH B5 — LINE webhook / API app mobile / API MCP / Public API

## 0. Nguồn TC
- **Nguồn đã dùng**: MCP LME TEST STUDIO — task_id=507, ticket 43845 (subset B5: webhook LINE `/line/callback`, API `/api/mobile/*`, API M2M nhóm api-job-auth, MCP OAuth, Public API `/api/v1`, Webhook転送, webhook UnivaPay/Google, APP LME mobile-app).
- **Tổng số TC review**: 124.

> **Đã áp [framework/php-upgrade-checklist.md](../../framework/php-upgrade-checklist.md)**. Batch này phủ **rộng và đúng điểm** các lib/hành vi nâng cấp: **LINE SDK v12** (webhook parser + signature), **F13 JSON phân trang API**, **C APP_KEY** (token MCP/webhook signing-secret cũ giải mã được), và **mặt tiếp xúc APP LME (mobile-app)** — trả lời luôn câu hỏi surface app-LME còn treo ở B3b. Vấn đề: 38% pass + 0 prd.

## 1. Coverage — dev-impact + diff code

- **dev-impact: CHƯA ĐỦ (chưa xác nhận).** F6 (LINE SDK v12 webhook/signature), F7 (socket JWT — ở B6), F13 (phân trang API), T7 (API app/MCP/public) đều có TC. **Nhưng** 47/124 pass (38%), 0 prd.
- **diff code: CHƯA ĐỦ (chưa xác nhận).** `requirement_keys` REQ-T18 (webhook/LINE SDK), REQ-T5 (API job nonce/ngày), REQ-T22 (API M2M), REQ-T10 (MCP OAuth), REQ-T11 (webhook thanh toán) phủ đủ. Không thấy điểm sửa thiếu TC thiết kế.

| Mã | Chiều | Vùng ảnh hưởng | TC hiện có | Status | Ghi chú |
|---|---|---|---|---|---|
| R1 | dev-impact + diff | Webhook LINE / API app / MCP / Public API chạy **production** (RULE-08 domain) | NEW-243-247 (webhook), NEW-505/560 (API app), NEW-792/797 (MCP), NEW-1092-1100 (Public API) — env dev/local | **RISK** | RULE-08: webhook domain + API public không kết luận từ dev/local |
| R2 | diff | **Webhook転送 chuyển tiếp event LME KHÔNG xử lý** (accountLink status 9…) sau khi SDK v12 đổi parser | NEW-694/695/802 chỉ cover config/validate/secret, **không có TC về nội dung được forward** | **GAP nhẹ** | memory forward-webhook-unhandled-event: event không xử lý vẫn phải forward nguyên văn → §7 R1 |

**Kết luận §1**: 1 GAP nhẹ (R2 forward nội dung) · 2 RISK (R1 exec/prd). Coverage webhook/API/MCP/Public thiết kế đầy đủ, chưa xác nhận exec.

## 2. Thiếu so với quan điểm test

**Kết luận**: không thiếu quan điểm lớn. Độ phủ checklist:

| Mục checklist | Trạng thái B5 | TC tiêu biểu |
|---|---|---|
| B LINE SDK v12 — webhook signature (F6) | ✅ phủ đúng điểm | NEW-246 (thiếu/sai chữ ký → 401, đúng → 200, Olioa bot_type=1 → 403, bug 44191), NEW-247 (body hỏng/thiếu events → không 500), NEW-243/244/245 (nhận event, Verify) |
| F13 JSON phân trang API (Laravel 13 thêm khoá) | ✅ phủ | NEW-560 (12 khoá paginator, per_page giữ kiểu, bug 44227), NEW-234 (khoá thừa `links` không fail), NEW-505 (chat phân trang) |
| A2 ngày JSON JST | ✅ phủ | NEW-283 (`Y-m-d H:i:s` không ISO), NEW-550 (thứ trong tuần đúng, 24:00), NEW-233 |
| A4/A6 null/ép kiểu API | ✅ phủ | NEW-549 (aff_fee `(float)` không TypeError), NEW-551/584 (`(int)` number), NEW-556 (`{message:success}` như prod) |
| C APP_KEY giải mã token cũ (rủi ro BLOCKER) | ✅ **phủ tốt** | NEW-797 (MCP token cấp trước nâng cấp vẫn gọi được), NEW-802 (署名シークレット 5.5 giải mã được) |
| Public API /v1 (hợp đồng) | ✅ phủ đầy đủ | NEW-1092-1100 (key đọc GET /friends, fields, send text, **idempotency** NEW-1095, **do_action** NEW-1096, date, page/limit, schema) |
| API job replay (SEC) | ✅ phủ | NEW-277 (nonce cache TTL 10 phút, replay 401) |
| Surface APP LME (mobile-app) | ✅ phủ | NEW-1387-1394 (xoá/block friend, gửi link, backup, change-bot), NEW-1535-1537 (tìm friend) |

→ Không sinh `Q<x>`.

## 3. TC trùng lặp

Đã rà 124 TC — **không phát hiện trùng**. NEW-505/524 (API chat get-list vs send các loại tin) khác mục tiêu; NEW-1387/1388 (block-friend vs xoá-friend) khác thao tác. Giữ nguyên.

## 4. Mâu thuẫn trong TCs

Đã rà 124 TC × spec `api-integration`/`webhook-relay` + mcp-rules — **không mâu thuẫn TC-vs-TC / TC-vs-kho**. Điểm khác-production chủ đích → §8: NEW-246/247 (webhook signature: nhánh mới ghi log cảnh báo/Chatwork khác production im lặng), NEW-560/234 (Laravel 13 thêm khoá JSON paginator).
- **CONF-IGNORE**: không có. ⚠️ Lưu ý: NEW-694 note dẫn `https://lme.jp/manual/api_webhook/` làm oracle — chỉ là link 「使い方を見る」 trong UI (không phải nguồn spec), không vi phạm rule cấm WebFetch manual.

## 5. Issues khác

| # | Severity | TC / phạm vi | Vấn đề | Đề xuất |
|---|---|---|---|---|
| 1 | `[BLOCKER]` | Toàn batch B5 | **38% pass** (47/124) · chưa chạy 16 · skip 57 · error 1 · fail 3 | Chạy lại trên QA PHP 8.5 có URL webhook public + prd |
| 2 | `[MAJOR]` | NEW-694 (`error`, bug=[]) | Webhook転送 lưu URL/bật chuyển tiếp đang `error`, chưa kết luận, chưa ticket | Triage lỗi môi trường vs thật |
| 3 | `[MAJOR] RULE-08` | Webhook LINE / API public / MCP (env dev 76 · local 32 · **prd 0**) | Webhook domain + API public + token mã hoá không kết luận từ dev/local | Scope chứa `prd`; chạy webhook thật + Public API trên prd |
| 4 | `[MINOR]` | 16 TC `viewpoint`=None (NEW-1387-1394 app-LME, NEW-1403/1406/1407 LOA, NEW-1535-1537) | Thiếu mã quan điểm → không map coverage | Gán mã (`API-CONTRACT-*`/`REQ-RG-ACC`…) |

Chất lượng từng TC: **xuất sắc** — oracle = base commit cụ thể, nêu rõ hàm/endpoint bị chạm (SDK v12 parser, Guzzle 7, Carbon ép kiểu), bug ticket (44191/44227/44355), điều kiện local (giả webhook) rõ ràng.

## 6. TCs thừa / ngoài phạm vi task

Đã rà 124 TC — **không có TC thừa/ngoài phạm vi #43845**.

## 7. TCs đề xuất bổ sung (3)

Đã đối chiếu 124 TC + spec `api-integration`/`webhook-relay` + checklist. Chỉ 1 GAP nhẹ (R2).

> **Bổ sung 2026-10-27 — rà riêng Webhook relay 「Webhook転送」 theo 2 maincase.** MC1 (cấu hình URL + bật/tắt, 2 tab LINE/L Message) **ĐỦ rất mạnh**: NEW-694 (lưu URL + bật, 2 tab độc lập, reload giữ) · 695 (validate https/trống) · 839/840/841 (menu + 署名シークレット + lỗi rỗng) · 842/843 (sort log cả 2 tab) · 844/848 (quyền owner/staff) · 802 (secret bản cũ). MC2 (forward nguyên văn) mới có TC-INTGLINE001-01 (kênh **LINE**, event không xử lý) → thêm 2 TC: **TC-INTGLINE001-02** kênh **L Message (LME)** + bật/tắt gate forward thật · **TC-INTGLINE001-03** ghi 転送エラー khi URL ngoài lỗi (NEW-841/842/843 chỉ hiển thị/sort lỗi có sẵn, chưa TC nào tạo lỗi).

| ID | Nhóm | Mã quan điểm | Màn hình/chức năng | Loại case | Chạy | Phạm vi ENV | Surface | Tên case | Tiền điều kiện | Các bước thực hiện | Dữ liệu nhập | Kết quả mong đợi | Kết quả thực thi | Ghi chú |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TC-INTGLINE001-01 | API | INTG-LINE-001 | Webhook転送: event LINE mà LME KHÔNG xử lý vẫn được chuyển tiếp nguyên văn tới URL đích | Normal | manual | dev, local, prd, staging | job, api | Webhook転送 bật ở tab LINE — gửi event `accountLink` (status 9) và vài event LME không xử lý (status 3/5-8) tới `/line/callback`, kiểm URL đích nhận nguyên văn | Bot test bật Webhook転送 tab 「LINE公式アカウントデータ転送」 trỏ URL đích test ghi log (vd webhook.site). SDK v12 parser đã deploy. Có body thật của event `accountLink` + 1 event LME chưa handle | 1. Bật 転送 tab LINE, URL = endpoint test ghi request. 2. Gửi POST `/line/callback/add/{bot_id}` body chứa event `accountLink` (status 9) + chữ ký hợp lệ. 3. Gửi tiếp body event LME không xử lý (status 3/5). 4. Đọc request mà URL đích nhận; đối chiếu body nguyên văn | event accountLink status 9; event status 3/5 | URL đích nhận **nguyên văn** body các event (kể cả event LME không tự xử lý) — SDK v12 parser không làm rớt/đổi event chưa handle; webhook `/line/callback` vẫn trả 200. Giống production (memory forward-webhook-unhandled-event: event không xử lý vẫn forward) | | Lấp R2/§1 · regression forward sau đổi parser SDK v12 (F6) · manual + local (giả webhook) · dẫn từ memory forward-webhook-unhandled-event-rule · Đánh giá spec: Spec không ghi đầy đủ status 3/5-8/10/30/31/33/50 (chưa chốt) → §8 |
| TC-INTGLINE001-02 | API | INTG-LINE-001 | Webhook転送 tab 「L Messageデータ転送」: forward event LME nguyên văn tới URL ngoài; bật→forward, tắt→ngừng | Normal | manual | dev, local, prd, staging | job, api | Kênh L Message (LME) bật 転送 → event LME được POST nguyên văn tới URL đích; tắt 転送 → không còn POST (bổ sung cho TC-INTGLINE001-01 chỉ kênh LINE) | Bot test, màn 「Webhook転送」 tab 「L Messageデータ転送」. 転送先URL = endpoint test ghi request (vd webhook.site). Có 1 event LME thật (kết bạn/action) kích hoạt webhook LME. Kênh LINE để 停止中 để chứng minh độc lập. Có mốc production | 1. Tab 「L Messageデータ転送」 nhập 転送先URL, bật 「転送の状態」, 保存する (toast + nhãn 転送中). 2. Kích hoạt 1 event LME. 3. Đọc request URL đích nhận; so body nguyên văn + header. 4. **Tắt** 転送 (停止中), lưu. 5. Kích hoạt lại event LME. 6. Kiểm URL đích KHÔNG nhận nữa; tab LINE không bị ảnh hưởng | 転送先URL (kênh LME); 1 event LME | Khi 転送中: URL đích nhận body event LME **nguyên văn** (Guzzle 7 POST không đổi/rớt field), webhook LME nội bộ vẫn chạy bình thường. Khi 停止中: URL đích **không** nhận request (bật/tắt gate đúng). Độc lập với tab LINE. Giống production | | Lấp MC2 kênh L Message (TC-INTGLINE001-01 chỉ kênh LINE) + bật/tắt gate forward thật · regression F12 Guzzle 7 POST · manual + local (giả webhook) · ENV chứa prd (RULE-08 domain) · Đánh giá spec: Spec ghi rõ (SCR-02 tab L Message) |
| TC-INTGLINE001-03 | API | INTG-LINE-001 | Webhook転送: URL ngoài lỗi/timeout → ghi 「転送エラー」, webhook nội bộ vẫn 200 (Guzzle 7 catch Throwable) | Abnormal | manual | dev, local, staging | job, api | Khi URL đích trả 5xx/timeout, lỗi forward được ghi vào card/list 転送エラー + KHÔNG làm webhook nội bộ 500 | Bot test bật 転送 (tab LINE hoặc LME) trỏ 転送先URL = endpoint **trả HTTP 500 hoặc treo (timeout)**. Card 転送エラー ban đầu 「転送エラーはありません」. Có mốc production | 1. Cấu hình 転送先URL = endpoint trả 500 / timeout. 2. Bật 転送, lưu. 3. Gửi 1 event tới `/line/callback/add/{bot_id}` chữ ký hợp lệ. 4. Kiểm webhook nội bộ vẫn xử lý + trả 200. 5. Mở card/list 「転送エラー」 tab tương ứng: kiểm phát sinh bản ghi lỗi (発生日時 JST, nội dung) + sort cột 発生日時 (như NEW-842/843) | 転送先URL lỗi 500/timeout; 1 event | Webhook nội bộ `/line/callback` vẫn trả **200** và xử lý event như thường (lỗi forward KHÔNG chặn luồng chính — Guzzle 7 `catch Throwable`, F3). Lỗi forward **được ghi** vào 転送エラー (1 bản ghi, 発生日時 JST, sort được). KHÔNG 500/TypeError PHP8. Giống production | | Lấp MC2 — 転送エラー logging khi URL ngoài lỗi (NEW-841/842/843 chỉ hiển thị/sort lỗi có sẵn, chưa TC nào tạo lỗi) · regression F3 Guzzle 7/Throwable + A4 · manual + local · Đánh giá spec: Spec ghi rõ (card 転送エラー) |

## 8. Spec update needed

| # | Điểm cần chốt | Nguồn | Ai chốt |
|---|---|---|---|
| 1 | Webhook signature nhánh mới **ghi log cảnh báo + Chatwork** (chế độ LOG_ONLY / chặn 401) KHÁC production (tự ký so chính nó, im lặng). Hành vi mới + mức báo Chatwork có đúng mong muốn? | NEW-246/247 · PB-1 | PO / Leader |
| 2 | Laravel 13 thêm khoá `links` (+ `current_page_url`…) vào JSON paginator API app — xung đột quy ước "JSON y như production". Chấp nhận khoá thừa hay strip? | NEW-560/234 · bug 44227 | Leader |
| 3 | Webhook転送: các event LME không xử lý (status 3/5-8/10/30/31/33/50) có forward nguyên văn không — spec chưa ghi đủ danh sách (memory mới chốt accountLink status 9) | §7 TC-INTGLINE001-01 | Dev + Leader |

---

# BATCH B6 — Chat 1:1 & Realtime

## 0. Nguồn TC
- **Nguồn đã dùng**: MCP LME TEST STUDIO — task_id=507, ticket 43845 (subset B6: 1:1チャット `/basic/chat-v3`, チャット設定, チャット管理, chat nhóm, web mobile chat, realtime node_serve/socket, AI設定, emoji/avatar).
- **Tổng số TC review**: 73.

> **Đã áp [framework/php-upgrade-checklist.md](../../framework/php-upgrade-checklist.md)**. Rủi ro chính của chat khi nâng PHP: **F7 socket JWT realtime** (node_serve + Redis EVAL), **F6 LINE SDK v12** (push/reply/quote + refresh token 401), **C APP_KEY** (channel_access_token), **A2 giờ tin JST**. Bộ TC phủ cả 4 — đồng thời **NEW-307/308 trả lời cross-ref APP_KEY của B3b** (channel token refresh/decrypt). Vấn đề: 26% pass + NEW-1347 fail + 0 prd.

## 1. Coverage — dev-impact + diff code

- **dev-impact: CHƯA ĐỦ (chưa xác nhận + fail).** F6 (push/reply SDK v12), F7 (socket JWT), T4 (chat) có TC dày. **Nhưng** 19/73 pass (26%), NEW-1347 fail, 0 prd.
- **diff code: CHƯA ĐỦ (chưa xác nhận).** `requirement_keys` REQ-T16 (push/reply/token), REQ-T17 (loại tin), REQ-T18 (realtime/webhook), REQ-T5 (giờ tin), REQ-B6F9 (socket token) phủ đủ.

| Mã | Chiều | Vùng ảnh hưởng | TC hiện có | Status | Ghi chú |
|---|---|---|---|---|---|
| R1 | dev-impact | **NEW-1347 fail** (socket JWT token ở 1:1/nhóm/web mobile + bot-switch tab) | NEW-1347 | **RISK/[BLOCKER]** | fail, chưa ticket — là đường token socket của bản vá #43734. TC gắn nhiều lỗi-có-sẵn-production "không chấm fail"; cần xác định fail do đâu → §5 |
| R2 | dev-impact + diff | Chat realtime (node_serve/Redis) + push/reply LINE chạy **production** | NEW-249/253 (realtime), NEW-300/303/306-308 (push/reply/token), NEW-11/169/170 (media) env dev/local | **RISK** | RULE-08: socket domain + LINE push không kết luận từ dev/local |

**Kết luận §1**: 0 GAP · 2 RISK (R1 fail NEW-1347, R2 exec/prd). Coverage chat/realtime thiết kế đầy đủ.

## 2. Thiếu so với quan điểm test

**Kết luận**: không thiếu quan điểm lớn. Độ phủ checklist:

| Mục checklist | Trạng thái B6 | TC tiêu biểu |
|---|---|---|
| F7 socket JWT realtime | ✅ phủ | NEW-1347 (token socket + tự refresh 9 phút + bot-switch tab → 403, memory bot-switch-other-tab-reload), NEW-249/253 (tin realtime JST, không lệch UTC) |
| F6 LINE SDK v12 push/reply/quote | ✅ phủ | NEW-300 (push + quote token), NEW-303 (reply token postback), NEW-306 (push bạn đã chặn → lỗi gửi), NEW-516/518/520/521 (các loại tin) |
| C APP_KEY / channel_access_token (cross-ref B3b) | ✅ **phủ** | NEW-307 (token sai 401 → tự refresh bằng channel_id/secret), NEW-308 (refresh thất bại → câu lỗi JP) |
| A2 giờ tin JST (realtime/lịch sử) | ✅ phủ | NEW-249/253 (0-9h JST không lùi), NEW-280 (tải tin cũ qua ranh giới năm) |
| A4 null / Guzzle 7 err | ✅ phủ | NEW-252 (mất mạng LINE → không 500), NEW-498 (content JSON hỏng → không TypeError) |
| Media chat (#44065) | ✅ phủ | NEW-11 (video thumbnail/mp3→m4a), NEW-169/170 (ảnh resize/EXIF), NEW-304 |
| Chat settings 8 tab + badge | ✅ phủ | NEW-293-297 (対応ステータス CRUD/validate), NEW-158 (badge), NEW-298/415 (チャット管理) |
| Session expired CSRF | ✅ phủ | NEW-654 (ajax 401 SESSION_EXPIRED) |

→ Không sinh `Q<x>`.

## 3. TC trùng lặp

Đã rà 73 TC — **không phát hiện trùng**. NEW-296 (lưu/mở lại cờ chat-setting) vs NEW-1358-1366 (tác dụng thực tế từng cờ) là **tách chủ đích** (NEW-296 persistence, NEW-13xx effect — ghi rõ "không dùng NEW-296 thay coverage"). Giữ nguyên.

## 4. Mâu thuẫn trong TCs

Đã rà 73 TC × spec `chat-11`/`chat-management`/`chat-setting` + kho `fa001`/`fa041` — **không mâu thuẫn TC-vs-TC / TC-vs-kho**. 1 mâu thuẫn **tài liệu** (không phải TC): `smoke-list.md:82` ghi "giờ chat realtime đang lệch UTC, giao T23" nhưng HEAD đã sửa `ChatEvent.php` → expected = JST (NEW-249 note) → §8.
- **CONF-IGNORE**: không có.

## 5. Issues khác

| # | Severity | TC / phạm vi | Vấn đề | Đề xuất |
|---|---|---|---|---|
| 1 | `[BLOCKER]` | NEW-1347 (`fail`, bug=[]) | TC socket JWT token (1:1/nhóm/web mobile + bot-switch tab) `fail`, chưa ticket. TC này gắn **nhiều lỗi-có-sẵn-production** (web mobile `0==e.has_error`, chat nhóm `isHideTop`/`checkFriend` undefined) đều ghi "KHÔNG chấm fail" → cần xác định fail thật nằm ở đâu | Triage NEW-1347: fail ở nhánh nào (socket thật hay env node_serve/Redis) → raise ticket nếu lỗi thật |
| 2 | `[BLOCKER]` | Toàn batch B6 | **26% pass** (19/73) · skip 40 · chưa chạy 8 · error 3 · fail 3 | Chạy lại trên QA PHP 8.5 có node_serve + Redis + LINE thật + prd |
| 3 | `[MAJOR] RULE-08` | Chat realtime (node_serve/Redis) + push LINE (env dev 54 · local 11 · **prd 0**) | Socket domain + LINE push không kết luận từ dev/local | Scope chứa `prd`; chạy realtime + push thật |
| 4 | `[MAJOR]` baseline | NEW-1358/1359/1362-1366 (8 TC tác dụng cờ chat-setting), exec=None | Đều ghi "cần chốt oracle base 303a131b9c trước chạy, chưa có thì blocked" — draft chờ baseline | Chốt oracle base cho từng cờ (既読/重複送信/phím tắt/preview/auto-confirm/短縮URL) |
| 5 | `[MINOR]` | NEW-1545, NEW-980, NEW-982 (viewpoint=None) | Thiếu mã quan điểm | Gán mã (`FUNC-*`) |

Chất lượng từng TC: **xuất sắc** — oracle = base commit, nêu rõ điểm SDK v12/Guzzle 7/Carbon/socket bị chạm, phân biệt rõ lỗi-có-sẵn-production (không chấm fail) vs lỗi nâng cấp.

## 6. TCs thừa / ngoài phạm vi task

Đã rà 73 TC — **không có TC thừa/ngoài phạm vi #43845**.

## 7. TCs đề xuất bổ sung (0)

Đã đối chiếu 73 TC + spec `chat-11`/`chat-setting` + kho `fa001`/`fa041` + checklist. **Không đề xuất TC mới** — F7 socket (NEW-1347 + 249/253), F6 push/reply/token (NEW-300/303/306-308), C APP_KEY channel token (NEW-307/308), media, chat-settings đều có TC. Việc cần làm: **chạy + chốt baseline 8 TC chat-setting effect + triage NEW-1347**, không phải viết thêm (AP-5).

## 8. Spec update needed

| # | Điểm cần chốt | Nguồn | Ai chốt |
|---|---|---|---|
| 1 | `smoke-list.md:82` ghi giờ chat realtime "lệch UTC, giao T23" nhưng `ChatEvent.php` đã sửa JST ở HEAD — cập nhật smoke-list cho khớp (expected = JST) | NEW-249/253 | Dev (sửa tài liệu) |
| 2 | NEW-1347 socket token fail: xác định fail thật (đường token #43734) vs env node_serve/Redis chưa dựng → raise ticket nếu thật | NEW-1347 | Dev + QA |
| 3 | Oracle base cho 8 cờ chat-setting (既読情報/重複送信防止/phím tắt/送信プレビュー/自動確認/短縮URL): phạm vi tác dụng + điều kiện trùng + thời gian chưa chốt, phải ghi từ base 303a131b9c | NEW-1358/1359/1362-1366 | Dev + Leader |

---

# BATCH B7 — Account / Auth / BotConnect / Admin / System

## 0. Nguồn TC
- **Nguồn đã dùng**: MCP LME TEST STUDIO — task_id=507, ticket 43845 (subset B7: ログイン/login-v2, 二段階認証, パスワード再設定, 新規登録, 接続設定/LOA, PC接続 wizard, 入れ替え/bot swap, マイページ, スタッフ管理/権限, TrustProxies/proxy, deploy session, System Admin top/ユーザーリスト/登録経路/お知らせ).
- **Tổng số TC review**: 115.

> **Đã áp [framework/php-upgrade-checklist.md](../../framework/php-upgrade-checklist.md)**. Batch này phủ **trọn mục C (auth/mã hoá)** của checklist — và **đóng cross-ref [MAJOR] APP_KEY mà B3b để mở**: NEW-237/916 (LOA connection đọc channel token cũ) + NEW-800 (re-login mật khẩu cũ sau deploy) kết hợp B6 NEW-307/308 (refresh channel token) + B5 NEW-797/802 (MCP/webhook token cũ) ⇒ token mã hoá cũ giải mã được đã có TC. Vấn đề còn lại: 38% pass + 0 prd.

## 1. Coverage — dev-impact + diff code

- **dev-impact: CHƯA ĐỦ (chưa xác nhận).** F1 (route param lệch → redirect), F14 (session/hashing), T1 (toàn màn /basic·/admin·login) có TC. **Nhưng** 44/115 pass (38%), 0 prd.
- **diff code: CHƯA ĐỦ (chưa xác nhận).** `requirement_keys` REQ-T10 (auth/session/encryption), REQ-RG-ACC (bot connect), REQ-INT (deploy/proxy), REQ-H393 (TrustProxies IP mới), REQ-SEC (password token) phủ đủ.

| Mã | Chiều | Vùng ảnh hưởng | TC hiện có | Status | Ghi chú |
|---|---|---|---|---|---|
| R1 | dev-impact + diff | **C — APP_KEY / channel_access_token giải mã** (giải cross-ref B3b) | NEW-237/916 (LOA cũ đọc token + tên/ảnh), NEW-800 (session deploy), + B6 NEW-307/308, B5 NEW-797/802 | **RISK → đã có TC** | Không còn GAP; chỉ cần chạy trên prd (RULE-08) |
| R2 | dev-impact + diff | Login/session/proxy/deploy chạy **production thật** (F-12, TrustProxies IP mới 142.91.106.63) | NEW-194/800 (deploy session), NEW-200/1354/1355 (proxy/LB), NEW-1189 (asset) env dev/local | **RISK** | RULE-08 + F-14: deploy/proxy/session chỉ kết luận được trên prd/QA PHP 8.5 lúc deploy thật |

**Kết luận §1**: 0 GAP · 2 RISK (đều exec/prd). Coverage auth/session đầy đủ; **cross-ref APP_KEY của B3b đã được giải**.

## 2. Thiếu so với quan điểm test

**Kết luận**: không thiếu quan điểm lớn. Độ phủ mục C + T1 + deploy:

| Mục checklist | Trạng thái B7 | TC tiêu biểu |
|---|---|---|
| C — F-12 session cũ logout sau deploy | ✅ phủ | NEW-194 (trang mở trước deploy → phiên mất, không ghi dữ liệu sai), NEW-800 (mọi vai trò logout 1 lần, re-login mật khẩu cũ OK) |
| C — bcrypt no-rehash (re-login mật khẩu cũ) | ✅ gián tiếp | NEW-800/429/782 (đăng nhập mật khẩu đặt trước deploy thành công) |
| C — 2FA | ✅ phủ | NEW-83/84 (bật/tắt + lịch sử), NEW-782 (sai mật khẩu/reCAPTCHA/mã 2FA → câu JP) |
| C — APP_KEY channel token (cross-ref B3b) | ✅ phủ | NEW-237/916 (LOA cũ hiển thị + lấy bạn bè), kết hợp B6/B5 |
| C — password reset token (IDOR + biên 24h) | ✅ phủ | NEW-747 (confirm_password thiếu token → 422, mật khẩu nạn nhân không đổi), NEW-748 (biên 24h) |
| ENV proxy/HTTPS TrustProxies (IP mới) | ✅ phủ | NEW-200 (URL https + IP thật), NEW-1354 (proxy không tin cậy spoof bị bỏ qua), NEW-1355 (deploy qua LB + IP 142.91.106.63) |
| DEPLOY asset version | ✅ phủ | NEW-1189 (js/css version mới sau F5, không 404, 3 luồng critical) |
| F1 route param lệch (redirect loop) | ✅ phủ | NEW-809/150/153/154 (chọn/đổi bot → /basic/home đúng mã, không lặp redirect) |
| Bot connect/swap wizard PC接続 | ✅ phủ | NEW-154/155/236/581/916, NEW-1405-1413/1512/1513 (modal channel validate) |

→ Không sinh `Q<x>`.

## 3. TC trùng lặp

Đã rà 115 TC — **không phát hiện trùng**. NEW-194 (deploy 1 màn template/broadcast) vs NEW-800 (deploy session mọi vai trò) khác mục tiêu; cụm NEW-1405-1413/1512/1513 là validate từng field channel (tách atomic). Giữ nguyên.

## 4. Mâu thuẫn trong TCs

Đã rà 115 TC × spec `login-user`/`register-user`/`bot-add-v2`/`change-bot`/`my-page`/`staff-management` + kho `fa039` — **không mâu thuẫn TC-vs-TC / TC-vs-kho**.
- **CONF-IGNORE**: không có. Lưu ý **F-16** (3 controller Auth `RegisterController`/`ForgotPasswordController`/`ResetPasswordController` không route → xoá): **không có TC** xác nhận (và không cần — chúng vốn không có route, không phải mặt người dùng) → chỉ ghi §8 để Dev xác nhận đã xoá sạch.

## 5. Issues khác

| # | Severity | TC / phạm vi | Vấn đề | Đề xuất |
|---|---|---|---|---|
| 1 | `[BLOCKER]` | NEW-809 (`fail`, bug=[]) | 「アカウント一覧」 bấm tên bot P/Q/R → trang chủ bot `fail`, chưa ticket. TC ghi "ảnh bot 404 dev #44354 không chấm" → fail có thể ở nhánh khác (URL/redirect) | Triage NEW-809: fail do redirect/URL thật hay ảnh env → raise ticket nếu lỗi điều hướng thật |
| 2 | `[BLOCKER]` | Toàn batch B7 | **38% pass** (44/115) · skip 54 · chưa chạy 12 · error 2 · fail 3 | Chạy lại trên QA PHP 8.5 **lúc deploy thật** (F-12/proxy/asset cần đúng môi trường deploy) + prd |
| 3 | `[MAJOR]` | NEW-83 (`fail`, bug 44354) | 2FA bật/tắt + lịch sử `fail` (có ticket 44354) | Theo dõi #44354 |
| 4 | `[MAJOR] RULE-08` | Login/session/proxy/deploy (env dev 93 · local 10 · **prd 0**) | F-12 session, TrustProxies IP mới 142.91.106.63, deploy asset chỉ kết luận được trên prd/QA lúc deploy | Scope chứa `prd`; chạy NEW-194/800/1355/1189 trong quy trình deploy thật |
| 5 | `[MINOR]` | 12 TC `viewpoint`=None (NEW-1404-1412/1512/1513/1523-1525) | Thiếu mã quan điểm (phần lớn là validate channel modal của 接続設定) | Gán mã (`FUNC-*`/`REQ-RG-ACC`) |

Chất lượng từng TC: **xuất sắc** — oracle = base commit, nêu rõ điểm F1 (route param)/F-12/TrustProxies/APP_KEY bị chạm, phân biệt lỗi-có-sẵn (ảnh bot 404 #44354).

## 6. TCs thừa / ngoài phạm vi task

Đã rà 115 TC — **không có TC thừa/ngoài phạm vi #43845**.

## 7. TCs đề xuất bổ sung (2)

Đã đối chiếu 115 TC + spec `login-user`/`bot-add-v2`/`change-bot` + kho `fa039` + checklist C. **Không đề xuất TC mới** — mục C (session/2FA/password/APP_KEY), ENV proxy, DEPLOY asset, F1 route-param đều có TC; **cross-ref APP_KEY của B3b đã giải** bằng NEW-237/916/800 (+B6/B5). Việc cần làm: **chạy trong quy trình deploy thật trên prd** + triage NEW-809, không phải viết thêm (AP-5).

> **Bổ sung 2026-10-27 — rà riêng cụm Change bot (LINE公式アカウント入れ替え) theo 7 maincase** (44 TC change-bot-cluster + kho FA-039): **5/7 maincase ĐỦ thiết kế**: (1) nhập credentials + xác thực SDK v12 — NEW-154/242/1014-1019/1405/1409/1410/1525 · (2) webhook LOA mới — NEW-1015/1020/256/1406/1407 · (5) credential sai/đã dùng/hết hạn → không 500 — NEW-242/1024/1405/1406/1407/1409/1410/1525 · wizard PC接続/クイック接続 đầy đủ SCR-01→14. **Nhưng bộ Studio dừng ở màn 完了 (UI wizard), KHÔNG cover end-state sau đổi** → 2 gap: **G1 (MC4)** setting/scenario/tag/bạn bè giữ nguyên + remap channel mới (kho FA-039 **group 12** "Setting giữ nguyên sau khi đổi" 19 TC — Studio 0) · **G2 (MC7)** sau đổi bot nhận webhook + gửi tin qua **channel mới**. **MC6 rollback** khi đổi thất bại giữa chừng → §8 (hỏi Dev swap có transactional không). ID đã tránh trùng.

| ID | Nhóm | Mã quan điểm | Màn hình/chức năng | Loại case | Chạy | Phạm vi ENV | Surface | Tên case | Tiền điều kiện | Các bước thực hiện | Dữ liệu nhập | Kết quả mong đợi | Kết quả thực thi | Ghi chú |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TC-COMPATLEGACY001-02 | UI | COMPAT-LEGACY-001 | LINE公式アカウント入れ替え — sau khi đổi LOA xong: setting/scenario/tag/bạn bè của bot GIỮ NGUYÊN + remap channel mới | Normal | manual | dev, local, prd, staging | web | Hoàn tất 入れ替え sang LOA mới → toàn bộ setting/scenario/tag/friend-info/rich menu của bot giữ nguyên, remap đúng sang channel/LIFF mới | Bot X (gói Standard+) đang kết nối LOA cũ, có sẵn ≥2 tag, 1 scenario, 1 rich menu đang hiển thị, friend-info fields, ≥1 template, ≥1 bạn bè. Ghi đầy đủ danh sách + ID trước đổi. Có LOA mới hợp lệ (4 credentials). Mốc production + kho FA-039 group 12 | 1. Ghi baseline: list tag/scenario/richmenu/friend-info/template của bot X. 2. Chạy 入れ替え 「すぐに入れ替える」 sang LOA mới tới màn 完了. 3. Sau hoàn tất mở lần lượt: タグ管理, scenario, rich menu, friend-info, template, 通知設定. 4. Đối chiếu từng mục với baseline. 5. Kiểm channel_access_token/LIFF đã trỏ LOA mới | Bot X đầy đủ setting + LOA mới (4 credentials) | Sau 入れ替え: **toàn bộ setting/scenario/tag/friend-info/richmenu/template giữ nguyên** (số lượng + nội dung khớp baseline), remap sang channel/LIFF mới đúng; cảnh báo "data không chuyển" chỉ áp cho bạn-bè-LINE của OA mới, KHÔNG phải setting LME. Không 500/TypeError. Giống production + kho FA-039 group 12 | | Lấp G1 (maincase 4 — data/setting giữ nguyên sau đổi LOA) · bộ Studio chỉ cover wizard SCR-01→14, thiếu end-state (kho FA-039 group 12, 19 TC) · regression ChangeBotService remap + APP_KEY re-encrypt token channel mới · manual vì đổi LOA thật · ENV chứa prd · Đánh giá spec: Đã hỏi leader (kho FA-039) |
| TC-INTGHOOK001-01 | API | INTG-HOOK-001 | LINE公式アカウント入れ替え — sau đổi LOA: bot nhận webhook + gửi tin qua channel MỚI | Normal | manual | dev, local, prd, staging | line-friend, api, web | Sau 入れ替え sang LOA mới → kết bạn mới trên OA mới nhận được webhook; gửi tin test từ LME tới bạn OA mới thành công (channel mới) | Bot X vừa hoàn tất 入れ替え sang LOA mới (TC trên). Tài khoản LINE test F-new chưa kết bạn OA mới. channel_access_token mới hợp lệ. Mốc production | 1. F-new kết bạn OA mới (quét QR/add). 2. Kiểm webhook /line/callback/add/{bot_id} nhận event trên channel mới (F-new xuất hiện ở 友だちリスト). 3. Từ chat 1:1 gửi tin text tới F-new. 4. Kiểm F-new nhận tin trên LINE. 5. F-new gửi tin tới OA → auto-reply (nếu có) chạy | F-new + OA mới | Webhook channel MỚI nhận đúng (F-new vào 友だちリスト, không 401/signature-fail); gửi tin từ LME tới F-new **thành công qua channel mới** (channel_access_token mới, LINE SDK v12); F-new gửi → bot xử lý. KHÔNG dùng nhầm token OA cũ. Giống production | | Lấp G2 (maincase 7 — sau đổi LOA bot nhận/gửi qua channel mới) · RULE-06 output cuối + webhook signature (F6 LINE SDK v12) + APP_KEY token mới · bộ Studio dừng ở màn 完了 (UI), chưa verify end-state send/receive · manual vì cần LINE thật · ENV chứa prd · Đánh giá spec: Đã hỏi leader |

## 8. Spec update needed

| # | Điểm cần chốt | Nguồn | Ai chốt |
|---|---|---|---|
| 1 | NEW-809 fail: xác định fail do điều hướng /basic/home thật hay chỉ ảnh bot 404 (#44354 dev) → raise ticket nếu lỗi điều hướng | NEW-809 | Dev + QA |
| 2 | F-16: 3 controller Auth (`RegisterController`/`ForgotPasswordController`/`ResetPasswordController`) đã xoá sạch, không cài `laravel/ui` — xác nhận không còn route/残り (không cần TC vì vốn không có mặt người dùng) | F-16 | Dev |
| 3 | TrustProxies IP mới 142.91.106.63: hạ tầng xác nhận LB/proxy prd thật đi qua IP này trước khi chạy NEW-1355 | NEW-1355 | Hạ tầng + Leader |
| 4 | **入れ替え thất bại giữa chừng** (maincase 6): `ChangeBotService` lỗi sau khi đã nhận credential / giữa remap — swap có **transactional/rollback** để bot không rơi trạng thái nửa vời (nửa cũ-nửa mới) không? Không atomic → bổ sung TC rollback | maincase 6 change-bot · `ChangeBotService` | Dev + Leader |

---

# BATCH B9 — Job / Queue / Cron

## 0. Nguồn TC
- **Nguồn đã dùng**: MCP LME TEST STUDIO — task_id=507, ticket 43845 (subset B9: job bill/retry, queue worker + scheduler + log, xả hàng đợi deploy, job mail theo lô, Google Sheet/Calendar sync queue, data-copy job, force-delete/cleanup, lệnh artisan vận hành).
- **Tổng số TC review**: 63.

> **Đã áp [framework/php-upgrade-checklist.md](../../framework/php-upgrade-checklist.md)**. **Batch sạch & trưởng thành nhất**: **0 fail · 0 error · 0 TC thiếu mã quan điểm**. Phủ đúng rủi ro job khi nâng PHP: **A2 diffInDays trong job** (bill_max_friend/backfill/cross-trash), **A3 tiền trong bill job** (Stripe/UnivaPay), **queue drain payload 5.5→13 (F-14)**, **log channel + deprecations tách file**, **scheduler JST**. Vấn đề duy nhất: 37% pass + 0 prd (RULE-08 job nền).

## 1. Coverage — dev-impact + diff code

- **dev-impact: CHƯA ĐỦ (chưa xác nhận).** F10 (job framework), các job bill (F5), job mail (F12), job Google sync (F13), queue/cron (T10 deploy) có TC. **Nhưng** 23/63 pass (37%), 0 prd.
- **diff code: CHƯA ĐỦ (chưa xác nhận).** `requirement_keys` REQ-INT (queue/scheduler/log), REQ-T6/T11 (bill job date+money), REQ-T12 (mail job), REQ-T13 (CSV/Google job), REQ-T19 (batch/scheduler), REQ-T5 (lock) phủ đủ.

| Mã | Chiều | Vùng ảnh hưởng | TC hiện có | Status | Ghi chú |
|---|---|---|---|---|---|
| R1 | dev-impact + diff | **Bill job (tiền) + Google sync (domain) chạy production** (RULE-08) | NEW-338/339 (bill_stripe), NEW-340/344 (bill UnivaPay), NEW-44 (bill_max_friend), NEW-1259 (Google sync queue) env local/dev | **RISK** | RULE-08: job nền + bill tiền + domain không kết luận từ local/dev |
| R2 | diff | **Xả hàng đợi payload 5.5→13 khi deploy** (F-14) — kết quả (a)/(b) chưa chốt | NEW-204/205 | **RISK (chờ chốt)** | NEW-205: job payload 5.5 còn sót → chạy đúng HAY vào failed_jobs? → quyết định runbook F-17 → §8 |

**Kết luận §1**: 0 GAP · 2 RISK (R1 exec/prd, R2 chờ chốt runbook). Coverage job/queue/cron đầy đủ.

## 2. Thiếu so với quan điểm test

**Kết luận**: không thiếu quan điểm. Độ phủ checklist (phủ tốt nhất các batch):

| Mục checklist | Trạng thái B9 | TC tiêu biểu |
|---|---|---|
| A2 diffInDays trong job (rủi ro Carbon 3 âm/float) | ✅ phủ dày | NEW-44 (bill_max_friend 29 ngày nguyên), NEW-47 (backfill +1 cả 2 đầu), NEW-48 (cross-trash ≥90 ngày) |
| A3 tiền trong bill job | ✅ phủ | NEW-338/339 (bill_stripe thành công/lỗi), NEW-340/344 (bill UnivaPay), NEW-44 (10469 không ra số lẻ) |
| Queue drain deploy (F-14) payload 5.5→13 | ✅ phủ | NEW-204 (xả hết trước deploy), NEW-205 (job 5.5 còn sót) |
| Queue worker + log file job | ✅ phủ | NEW-201 (DeleteActionInSourceMessage ghi log đúng file), NEW-203 (log channel APP_LOG + deprecations tách) |
| Scheduler JST + 51 lịch | ✅ phủ | NEW-202/671/672 (schedule:list đủ lịch, Next Due JST, cron chạy không TypeError/ValueError) |
| Job mail theo lô (cross-ref B1) | ✅ phủ | NEW-534/535 (mail gia hạn 振込 đúng người/không trùng/SMTP lỗi hoãn), NEW-673/674/675 (mail affiliate + batch error isolation F-10) |
| Batch error F-10 (Throwable không dừng lô) | ✅ phủ | NEW-674 (1 bản ghi lỗi PHP8 không dừng cả lô + Chatwork chống lặp) |
| Lock job (JOB-LOCK) | ✅ phủ | NEW-278 (月次決済 chạy 2 lần song song → bỏ qua, TTL 360 phút) |
| CSV import/export job (A5) | ✅ phủ | NEW-405 (export SJIS kana/emoji), NEW-404 (import dòng lệch cột bỏ qua), NEW-89 (staff history BOM) |

→ Không sinh `Q<x>`.

## 3. TC trùng lặp

Đã rà 63 TC — **không phát hiện trùng**. NEW-202 vs NEW-671/672 (scheduler) khác góc (list vs run vs đủ 51 lịch); NEW-338 vs NEW-339 (bill_stripe thành công vs lỗi) khác loại case. Giữ nguyên.

## 4. Mâu thuẫn trong TCs

Đã rà 63 TC × spec (job không có spec-features riêng, oracle = base Kernel/code) + kho — **không mâu thuẫn TC-vs-TC / TC-vs-kho**. Điểm khác-production chủ đích → §8: NEW-674 (Chatwork báo cho PHP8 Error — production im lặng), NEW-205 (hành vi job payload sót chưa chốt).
- **CONF-IGNORE**: không có.

## 5. Issues khác

| # | Severity | TC / phạm vi | Vấn đề | Đề xuất |
|---|---|---|---|---|
| 1 | `[MAJOR]` (không BLOCKER) | Toàn batch B9 | **37% pass** (23/63) · skip 38 · chưa chạy 2 · **0 fail/error**. skip do cần worker/cron + Stripe/UnivaPay/Google/SMTP thật + quyền artisan (F-14) | Chạy lại trên QA PHP 8.5 có đủ service + chạy artisan tay; đây là batch **ít rủi ro nhất** vì 0 fail |
| 2 | `[MAJOR] RULE-08` | Bill job (tiền) + Google sync (domain) (env local 34 · dev 27 · **prd 0**) | Bill tiền + domain Google không kết luận từ local/dev | Scope chứa `prd`; verify bill_stripe/bill_max_friend/Google sync trong quy trình deploy thật |

Chất lượng từng TC: **cao nhất trong các batch** — mọi TC có mã quan điểm, oracle = base commit/Kernel cụ thể, nêu rõ điểm Carbon/money/queue bị chạm, điều kiện local (artisan tay + đọc DB/log) rõ ràng, phân biệt lỗi-có-sẵn (PB-xx) vs nâng cấp. Không có TC mơ hồ, không fail.

## 6. TCs thừa / ngoài phạm vi task

Đã rà 63 TC — **không có TC thừa/ngoài phạm vi #43845**.

## 7. TCs đề xuất bổ sung (0)

Đã đối chiếu 63 TC + base Kernel + checklist. **Không đề xuất TC mới** — job bill (A3), diffInDays job (A2), queue drain (F-14), log channel, scheduler, batch error (F-10), mail job đều có TC. Đây là batch hoàn chỉnh nhất về thiết kế; việc cần làm: **chạy trên prd/QA có service thật** + chốt runbook F-17 (§8), không viết thêm (AP-5).

## 8. Spec update needed

| # | Điểm cần chốt | Nguồn | Ai chốt |
|---|---|---|---|
| 1 | **Runbook deploy F-17**: job payload 5.5 còn sót sau chuyển code → (a) chạy đúng hay (b) vào failed_jobs? Nếu (b) thì bước **xả hàng đợi trước deploy là BẮT BUỘC** trong `deploy.md` | NEW-205 | Dev + Leader |
| 2 | NEW-674: nhánh mới báo Chatwork cho PHP8 `Error` (production im lặng vì là ErrorException) — mức báo Chatwork có đúng mong muốn? | NEW-674 · F-10 | PO / Leader |
| 3 | NEW-1259: hợp đồng đồng bộ Google Sheet (`calendar_sync_googles` type_sync 1-4) sau khi bỏ cờ mode #41033 — xác minh hợp đồng hiện hành vs cơ chế cắt 5 giây/`result_error_googles` | NEW-1259 | Dev |

---

# BATCH B10 — Mail / Notify / Push

> ⚠️ **Snapshot mới**: block này review trên bộ TC Studio #507 **re-fetch 2026-10-26** — task đã tăng **1537 → ~2018–2030 TC** (re-run `pipeline-qa` 02:52). B10 được lọc thủ công từ bộ phân loại (bộ classifier gom "通知/mail" quá rộng kéo cả TC đăng ký/login/My Page/affiliate — các TC đó là **delta của B7/B4/B1**, đã loại khỏi B10, sẽ rà ở delta-sweep). **Lõi Mail/Notify/Push thật = 34 TC.**

## 0. Nguồn TC
- **Nguồn đã dùng**: MCP LME TEST STUDIO — task_id=507, ticket 43845 (subset B10 curated 34 TC: F12 Symfony Mailer migration — đăng ký/2FA/reset/account mail · định tuyến kênh SMTP mặc định/RESEND/API · SMTP riêng tls/ssl · Gmail API · web push PC VAPID + push_subscriptions + FCM app · 通知設定 CRUD/staff-admin/default bot · 3 kênh App/PC/ChatWork · ChatWork link · お知らせ/ヘッダー通知 · OLIOA push · web-mobile notify list).
- **Tổng số TC review**: 34.

> **Đã áp [framework/php-upgrade-checklist.md](../../framework/php-upgrade-checklist.md)**. B10 phủ trọn **F12 (SwiftMailer→Symfony Mailer + webpush 13.0.1 + FCM google/auth)** — hotspot mail/push của nâng cấp PHP 8.5. Thiết kế đầy đủ, nhưng **chỉ 7/34 pass, 0 prd/staging** → rủi ro chính là EXECUTION, không phải coverage. 0 fail / 0 error.

## 1. Coverage — dev-impact + diff code

- **dev-impact: CHƯA ĐỦ (chưa xác nhận trên môi trường thật).** F12 (mail Symfony Mailer + web push + FCM + 3 kênh notify) có TC dày ở mọi mặt. **Nhưng** 7/34 pass (local/dev), 27 skip (cần mail thật / thiết bị / VAPID / ChatWork room / prd).
- **diff code: CHƯA ĐỦ (chưa xác nhận).** `requirement_keys` REQ-T12-01/02/04 (mail routing/SMTP/web push), REQ-T13 (Gmail/FCM), REQ-T23 (OLIOA push + account mail), REQ-RG-MKT-04/SYS-03 (通知設定/お知らせ) phủ đủ các điểm sửa `SmtpMailer::schemeOptions/defaultWithTimeout`, `MailApiService`, `PushSubscription` (webpush 13), `FirebaseService` (google/auth).

| Mã | Chiều | Vùng ảnh hưởng | TC hiện có | Status | Ghi chú |
|---|---|---|---|---|---|
| R1 | dev-impact + diff | **Mail thật (F12) gửi trên prd/staging** (RULE-08) | NEW-525/526/528/529/777 (đăng ký/2FA/reset/account), NEW-530/531/532/533 (routing/timeout/SMTP tls-ssl/encryption) — toàn **local (Mailpit)**, prd=0 | **RISK** | RULE-08: mail thật không kết luận từ local; STARTTLS/From/DKIM thật chỉ xác nhận trên SMTP thật |
| R2 | dev-impact + diff | **Web push + FCM + 3 kênh notify thật** (VAPID/Firebase/ChatWork/thiết bị) | NEW-414/536/538/1278/1289/1290/1284/1285/1286 — **toàn skip** (needs-human/needs-prep) | **RISK** | RULE-08 + thiết bị thật: push một-lần-đúng-một chỉ chứng minh được trên device/endpoint thật |
| R3 | diff | **Mail timeout: bỏ fallback mốc 5s** (gỡ `SmtpTimeoutPlugin`, `MAIL_TIMEOUT`) — hành vi đổi so với 5.5 | NEW-531 Ca 2 | **RISK (chờ chốt)** | SMTP chậm >5s nay KHÔNG fallback → có thể kéo dài; QA leader chốt 22/10 nhưng chưa nằm ở "Việc báo trước" → §8 |
| G2 | dev-impact + diff | **Điều kiện trigger notify "trần 100%"** (tin thứ 1.000 gửi thành công → エルメ notify; action độc lập web vs multi-action job Java; gửi lỗi → LINE OA) | NEW-422 chỉ modal cảnh báo TRƯỚC khi gửi (エルメ超過); NEW-1284 chỉ 配信エラー — KHÔNG có TC notify lúc chạm trần khi gửi **thành công** + phân biệt web/job | **GAP** | memory limit-notify-web-vs-job-scope (Leader chốt). F13 đếm 配信数 compat chạm → §7 G2 |

**Kết luận §1**: 2 GAP (G1 deliverability/Spam · G2 trigger notify trần 100% — §7) · 3 RISK (R1 mail-prd, R2 push/notify thật, R3 timeout). Coverage **thiết kế đầy đủ**; thiếu deliverability + điều kiện trigger notify trần, còn lại là môi trường. _(G2 bổ sung 2026-10-27 khi rà cụm Setting notify theo 6 maincase.)_

## 2. Thiếu so với quan điểm test

Độ phủ checklist F12 + NOTI-MAIL + MSG:

| Mục | Trạng thái B10 | TC tiêu biểu |
|---|---|---|
| F12 mail Symfony Mailer — routing kênh | ✅ phủ | NEW-530 (default/Microsoft→RESEND/API mail), NEW-529 (default lần đầu + RESEND gửi lại) |
| F12 — SMTP tls/ssl + encryption rỗng (schemeOptions/auto_tls) | ✅ phủ | NEW-532 (Gmail tls 587 / SES ssl 465 + 587 STARTTLS), NEW-533 (encryption rỗng/sai = như SwiftMailer) |
| F12 — timeout/fallback (defaultWithTimeout) | ✅ phủ | NEW-531 (SMTP câm → fallback API; SMTP chậm >5s → §8) |
| F12 — mail nội dung JP MIME (=?utf-8?B?=) | ✅ phủ | NEW-525/528/396 (tiêu đề JP không vỡ) |
| F12 web push — VAPID subscribe/unsubscribe | ✅ phủ | NEW-536 (POST subscribe/unsubscribe 200, pushKey, VAPID không sinh khoá mới) |
| F12 web push — push_subscriptions compat job Java | ✅ phủ | NEW-538 (cột endpoint/public_key/auth_token/content_encoding đúng dạng; dòng 5.5 cũ không đổi) |
| F12 — AESGCM encode + ký VAPID | ✅ phủ | NEW-1278 (3 bộ latin/JP①②㈱/emoji🎉 — không vỡ ký tự, ký khoá OK) |
| FCM app (google/auth JWT→oauth2) | ✅ phủ | NEW-414 (token Firebase mới, không invalid_grant/TypeError) |
| 3 kênh notify một-lần-đúng-một | ✅ phủ | NEW-1289/1290 (device thật, 1 event=1 push, badge+1, 1 mobile_notify), NEW-1284/1285/1286 (配信エラー/add-friend/chat × App/PC/ChatWork) |
| 通知設定 CRUD + (user,bot) + staff/admin | ✅ phủ | NEW-696 (toggle/freq/items persist), NEW-697 (staff vs admin riêng) |
| Default bot mới + chống nhân đôi dòng (firstOrCreate) | ✅ phủ | NEW-1287 (QR back/forward → 1 dòng), NEW-1291/1292 (default 3 kênh ON/realtime) |
| PHP8 null-safe (ChatWork chưa cấu hình) | ✅ phủ | NEW-756 (notifySettingData null → không 500), NEW-776 (`''==0` ép (int) OLIOA) |
| お知らせ/ヘッダー通知 | ✅ phủ | NEW-716/718 (CRUD + chuông header) |

→ Không sinh `Q<x>` cho F12/mail-push. _(Bổ sung 2026-10-27: maincase 4 "điều kiện trigger notify trần 100%" là gap coverage — xem §1 G2 + §7.)_

## 3. TC trùng lặp

Đã rà 34 TC — **không trùng**. Các cặp dễ nhầm đều tách chủ đích: NEW-1289 (1 event, device thật) vs NEW-1290 (dataset nhiều loại event) khác grain; NEW-1284/1285/1286 tách theo **nguồn sự kiện** (配信エラー / add-friend / chat) chứ không trùng; NEW-1291 (wizard step-by-step) vs NEW-1292 (quick-connect) khác luồng tạo bot; NEW-530 (routing) vs NEW-531 (timeout) vs NEW-532/533 (SMTP riêng) khác mặt kiểm. Giữ nguyên.

## 4. Mâu thuẫn trong TCs

Đã rà 34 TC × spec `notify-setting` + kho NS-* + deploy-notes/progress — **không mâu thuẫn TC-vs-TC / TC-vs-kho**.
- **CONF-SPEC**: NEW-531 Ca 2 — oracle "SMTP chậm >5s vẫn gửi, không fail" (QA leader chốt 22/10) **khác** mô tả cũ `MAIL_TIMEOUT`/`SmtpTimeoutPlugin` fallback ở 5s. Không phải TC sai — là **hành vi mới có chủ đích** nhưng chưa vào mục "Việc báo trước" của deploy-notes → §8 (chốt PO).
- **CONF-IGNORE (nghi vấn, cần Leader xác nhận)**: (a) **Gmail send** (NEW-396) — note ghi "mọi lời gọi gửi Gmail ở AuthController/LoginMobileController **đang bị comment** ⇒ production KHÔNG có đường UI gửi Gmail, chỉ còn màn liên kết"; TC phải gọi tay qua tinker. Nếu đúng là path chết trên prod → ứng viên thêm vào [framework/ignore-features.md](../../framework/ignore-features.md), hạ mức smoke. (b) **OLIOA push** (NEW-776) — note "Leader xác nhận màn OLIOA còn dùng trên production". → cả 2 ghi §8 để Leader chốt, **không tự loại**.

## 5. Issues khác

| # | Severity | TC / phạm vi | Vấn đề | Đề xuất |
|---|---|---|---|---|
| 1 | `[MAJOR] RULE-08` | Mail thật (F12) — NEW-525/526/528/529/530/531/532/533/777 | **0 TC chạy prd/staging**; toàn local Mailpit. STARTTLS/From/DKIM/giao nhận thật + không rơi Spam chỉ kết luận được trên SMTP thật | Scope chứa `prd/staging`; chạy mail đăng ký/2FA/reset trên SMTP thật khi deploy |
| 2 | `[MAJOR] RULE-08` | Web push + FCM + 3 kênh — NEW-414/536/538/1278/1284-1290 | **Toàn skip** (needs-human: thiết bị thật, VAPID/Firebase thật, room ChatWork thật) | Chạy tay trên QA device + endpoint thật; đây là cụm rủi ro cao nhất của B10 (push một-lần-đúng-một) |
| 3 | `[MAJOR]` (exec) | Toàn batch B10 | **7/34 pass (21%)** · 27 skip · **0 fail/0 error** | Chạy lại trên QA PHP 8.5 có mail/push/ChatWork/device thật |
| 4 | `[MINOR]` triage | NEW-1292 | Note ghi "bug #4447 **Reject**" | Xác nhận #4447 bị reject (không phải bug thật) → đóng, không chặn |
| 5 | `[MINOR]` cross-ref | NEW-536/538 bugs=[44065], NEW-489 bugs=[44071] | Gắn ticket media/#44065 + #44071 (lỗi có sẵn) — không phải lỗi nâng cấp | Theo dõi #44065/#44071 (đã nằm ở B3b/B4) |

Chất lượng từng TC: **cao** — oracle = base/production cụ thể, nêu rõ điểm F12 bị chạm (SmtpMailer::schemeOptions/defaultWithTimeout, PushSubscription webpush 13, FirebaseService google/auth), phân biệt lỗi-có-sẵn (PB-6 Gmail, PB-T13-2 FCM log, #44065) vs lỗi nâng cấp, chốt rõ case manual (device/mail thật).

## 6. TCs thừa / ngoài phạm vi task

Đã rà 34 TC — **không có TC thừa/ngoài phạm vi #43845**. (Các TC đăng ký/login/My Page/affiliate bị classifier kéo nhầm vào B10 đã loại ra ở bước curate — chúng thuộc B7/B4/B1, sẽ rà ở delta-sweep, không tính vào B10.)

## 7. TCs đề xuất bổ sung (2)

> **Bổ sung 2026-10-27 — rà riêng cụm Setting notify (通知設定) theo 6 maincase**: 5/6 maincase ĐỦ thiết kế (1 web push VAPID — NEW-536/538/1278 · 2 mobile app FCM — NEW-414/1289/1290 · 3 ChatWork — NEW-1284-1286 · 5 bật/tắt từng loại + A6 flag + test gửi — NEW-696/776 · 6 null/JP A4/A5 — NEW-756/776/1278), tất cả đang exec=skip → RISK môi trường (§5-2). **1 gap thật**: maincase 4 — điều kiện trigger notify "trần 100%" (G2 bên dưới).

Đã đối chiếu 34 TC + checklist F12 + kho NS-*. Có **2 GAP coverage thật** (ngoài các RISK môi trường đã nêu ở §5 — các RISK đó là "chạy TC đã có trên prd", không đẻ TC mới theo AP-5):

| ID | Nhóm | Mã quan điểm | Màn hình/chức năng | Chạy | Phạm vi ENV | Surface | Tên case | Tiền điều kiện | Các bước thực hiện | Dữ liệu nhập | Kết quả mong đợi | Kết quả thực thi | Ghi chú |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TC-NOTIMAIL001-02 | API | NOTI-MAIL-001 | Mail hệ thống メール送信: deliverability mail đăng ký/2FA/reset sau đổi SwiftMailer→Symfony Mailer | manual | prd, staging | api | Mail đăng ký/2FA/đặt-lại-mật-khẩu vào Inbox (không rơi Spam) ở Gmail/Yahoo/Outlook sau khi đổi Mailer | Môi trường prd/staging dùng SMTP thật (MAIL_* / RESEND_MAIL_*) như production. Có 3 hộp thư thật: 1 Gmail, 1 Yahoo!, 1 Outlook/Hotmail đã dọn Spam. Tài khoản QA (không dùng dữ liệu khách). | 1. Trên prd/staging, kích hoạt gửi mail đăng ký bước 1 tới địa chỉ Gmail QA → kiểm hộp thư. 2. Lặp với mail 2FA (đăng nhập owner) tới Yahoo!. 3. Lặp với mail đặt lại mật khẩu tới Outlook/Hotmail. 4. Với mỗi mail: mở "Hiển thị bản gốc", đọc header `From`, `Return-Path`, `Message-ID`, kết quả `SPF`/`DKIM`/`DMARC`; ghi mail nằm Inbox hay Spam. | 3 địa chỉ thật Gmail/Yahoo/Outlook; mail: 本登録のお願い / ログイン認証コード / パスワード再設定 | Cả 3 mail tới **Inbox, không rơi Spam/Junk** ở cả 3 nhà cung cấp. Header `From` đúng MAIL_FROM_ADDRESS/RESEND_MAIL_FROM_ADDRESS như production; `DKIM=pass`, `SPF=pass`, `DMARC=pass`. Tiêu đề JP hiển thị đúng (=?utf-8?B?=), không vỡ chữ. Không khác bản 5.5 về khả năng vào Inbox. | | Lấp G1 · basis: F12 đổi SwiftMailer→Symfony Mailer có thể đổi `Message-ID`/thứ tự header/`From` → ảnh hưởng DKIM/DMARC & phân loại Spam; NEW-525..533 chỉ kiểm trên Mailpit local nên KHÔNG bắt được deliverability thật · bài học [[contract-transfer-mail-rules]] (mail chuyển khoản kiểm Gmail/Yahoo/Hotmail/Outlook không Spam) áp cho mail tài khoản · manual + prd vì mail thật + mắt người kiểm Spam (RULE-08) |
| TC-NOTIMAIL001-03 | Job | NOTI-MAIL-001 | 通知設定 / 配信 — Notify khi 配信数 chạm trần (tin thứ 1.000 gửi thành công) | manual | dev, local, prd, staging | web, job, line-friend | Tin thứ 1.000 (chạm trần tháng) gửi qua action độc lập (web) và multi-action (job Java) → エルメ notify đúng khi thành công; gửi lỗi → LINE OA notify | Bot test gói có trần 配信 tháng = 1.000 (hoặc ngưỡng test tương đương). Đã gửi 999 tin thành công trong tháng (đếm qua 配信数サマリー). Có 1 action độc lập (QR/form/salon/kết bạn) gửi 1 tin + 1 multi-action (chạy job Java) gửi. Admin bật 通知設定 nhận mục 配信/エラー trên App/PC/ChatWork. Có mốc hành vi production | 1. Kích hoạt action độc lập gửi tin thứ 1.000 (web, đồng bộ) thành công → quan sát エルメ notify (App/PC/ChatWork) + 配信数サマリー. 2. Reset về 999, kích hoạt multi-action (job Java) gửi tin thứ 1.000 → quan sát notify do job sinh. 3. Gửi qua chat 1:1 / send-test / トークリスト → xác nhận KHÔNG sinh notify trần. 4. Tạo 1 tin gửi LỖI (bạn đã chặn) → xác nhận LINE OA notify | 999 tin đã gửi; action độc lập + multi-action + chat1:1/send-test; 1 tin lỗi | Tin thứ 1.000 gửi **thành công** → **エルメ notify ngay** đúng kênh đã bật, cả khi qua action độc lập (web sync) lẫn multi-action (job Java) — như production. Chat 1:1 / send-test / トークリスト **KHÔNG** sinh notify trần. Gửi **lỗi** → chỉ **LINE OA** notify (không phải notify thành công エルメ). 配信数 đếm đúng (F13). KHÔNG 500/sai đếm do PHP8/Laravel13 | | Lấp G2 (maincase 4 — điều kiện trigger notify trần 100% web-vs-job) · regression F13 (đếm 配信数 compat) + trigger-source (web sync vs job Java) · dẫn từ memory limit-notify-web-vs-job-scope · manual vì cần gửi thật + quan sát notify + ngưỡng bill · ENV chứa prd (RULE-08) · Đánh giá spec: Đã hỏi leader (Leader chốt, spec chưa ghi) |

## 8. Spec update needed

| # | Điểm cần chốt | Nguồn | Ai chốt |
|---|---|---|---|
| 1 | **NEW-531 Ca 2**: SMTP chậm >5s nay KHÔNG fallback ở mốc 5s (gỡ `SmtpTimeoutPlugin`/`MAIL_TIMEOUT`) — hành vi đổi so với 5.5. Có cần đưa vào mục "Việc báo trước" của `deploy-notes.md` + ngưỡng chấp nhận thời gian chờ? | NEW-531 · progress.md T12 | PO + Leader |
| 2 | **Gmail send path**: mọi lời gọi gửi Gmail ở `AuthController`/`LoginMobileController` đang bị comment → production không có đường UI gửi Gmail (chỉ còn màn liên kết SCR-GML-01). Xác nhận là path chết → thêm vào `ignore-features.md`, hạ smoke; nếu còn dùng thì mở lại đường gọi | NEW-396 | Dev + Leader |
| 3 | **Màn OLIOA push** (`/basic/push-notifications`) còn dùng trên production? Nếu đã bỏ → ignore-feature | NEW-776 | Leader |
| 4 | **#4447 (NEW-1292)**: xác nhận đã **Reject** (không phải bug thật) để đóng, không chặn release | NEW-1292 | QA Leader |

---

# BATCH B3a — Message authoring (Template · Broadcast · Step/Scenario · AutoReply · Remind · Action-schedule/modal · Conversion · Welcome)

> ⚠️ **Snapshot mới 2026-10-26** (1537→~2018 TC). B3a **chưa từng review** nên gồm cả bộ gốc + TC mới. Lọc tay từ 992 TC chưa-review, loại các màn richmenu/QR/popup (→B3b delta), 友だち/tag (→B4 delta), マイページ/アカウント/login (→B7 delta), 回答フォーム (→B8). **Lõi message-authoring = 319 TC.** Đây là vùng lớn nhất; review theo 7 sub-area.

## 0. Nguồn TC
- **Nguồn đã dùng**: MCP LME TEST STUDIO — task_id=507, ticket 43845 (subset B3a curated 319 TC: テンプレート/一覧/作成 + Template V2 · 一斉配信 V1/V2 (broadcast) · ステップ配信 cũ/mới + scenario · 自動応答 (auto-reply) + callback · アクションスケジュール実行 + Modal アクション SC-004 · リマインド配信 · コンバージョン · 新規友だち用 welcome).
- **Tổng số TC review**: 319.

> **Đã áp [framework/php-upgrade-checklist.md](../../framework/php-upgrade-checklist.md)**. Trục nâng cấp của B3a: **F6 LINE SDK v12 message builder** (build tin text/image/video/audio/imagemap/carousel/GRP/quick-reply) · **Intervention Image v3** (media trong tin — **hotspot #44065**, 98/319 TC gắn ticket này) · **F9 auto-reply binding SQL** (`HandleCallbackMessage`) · **IDOR** đã vá ở broadcast/scenario/action-schedule/template V2/Action · **A5 encoding** text (& < " ') PHP8. 45% pass, **0 prd/staging**.

## 1. Coverage — dev-impact + diff code

- **dev-impact: CHƯA ĐỦ (chưa xác nhận + có fail).** F6 (builder các loại tin), F9 (auto-reply binding), media Intervention v3 có TC dày ở cả 7 sub-area. **Nhưng** 144/319 pass (45%), **7 fail (media) + 13 error (runner dev)**, 0 prd.
- **diff code: CHƯA ĐỦ (chưa xác nhận).** Khớp `dev_impact`: auto-reply binding SQL (`HandleCallbackMessage`), IDOR broadcast V2 (`saveBroadcastV2`/`copyBroadcastV2`), action-schedule copy, template V2, step send-test V3 (`sendTestStepMessageV3`) — đều có TC.

| Mã | Chiều | Vùng ảnh hưởng | TC hiện có | Status | Ghi chú |
|---|---|---|---|---|---|
| R1 | dev-impact + diff | **Media trong tin (Intervention v3) — #44065**: mp4/mp3/image map/EXIF/PNG trong suốt/thumbnail/carousel | NEW-7/8/9/10/13/163-168/167/351/523/832 (7 **fail**, nhiều skip) + 98 TC gắn #44065 | **RISK → [BLOCKER] cross-ref B3b** | Cùng root cause media của B3b; RULE-08 media chưa chạy prd. Phần media của B3a phải validate cùng bản vá #44065 của B3b |
| R2 | diff | **Lỗi `error/unknown` runner dev** (không phải bug sản phẩm) | NEW-419 (broadcast draft, local **pass**), NEW-667 (action-schedule, local **pass**), NEW-513 (step send-test, local partial OK), NEW-670/737/1228 (local needs-prep) | **RISK (re-run)** | `dev: error/unknown` nhưng local pass/partial → runner dev lỗi, chưa có kết luận test; re-run trên QA PHP 8.5 |
| R3 | dev-impact + diff | **Auto-reply binding SQL (F9)** — text khớp đúng `auto_reply` sau đổi binding | cụm 自動応答 (~45 TC) + NEW callback | **RISK** | Có TC luồng thường; thiếu abnormal text chứa ký tự SQL/LIKE/khoảng trắng để chứng minh binding không mis-match/injection → §7 R1 |
| R4 | diff | **A5 encoding text tin (& < " ' / emoji)** round-trip save→mở lại→gửi | SCR-TPL-02A text có URL + rải rác | **RISK** | PHP8.1 đổi mặc định `htmlspecialchars` ENT_QUOTES; cần 1 TC chuyên ký tự đặc biệt → §7 R2 |

**Kết luận §1**: 0 GAP tuyệt đối (coverage thiết kế rộng) · **6 RISK** (R1 media [BLOCKER] cross-ref B3b · R2 re-run dev errors · R3 auto-reply binding abnormal · R4 encoding · R5 error-list resend-execution cross-cutting · R6 remind A2 diffIn SIGNED [MAJOR]). 4 RISK (R3/R4/R5/R6) đẻ TC ở §7. _(R5 bổ sung 2026-10-27 khi rà cụm Error list 配信エラー theo 4 maincase — feature cross-cutting, không nằm trong 319 TC gốc của B3a.)_

## 2. Thiếu so với quan điểm test

Độ phủ 7 sub-area (nháp nội bộ — chỉ nêu phần mỏng):

| Sub-area | Trạng thái | Ghi chú |
|---|---|---|
| Template (list/create/V2/pack/carousel/send-test) | ✅ dày (~90 TC) | media trong template = R1 (#44065) |
| Broadcast 一斉配信 V1/V2 (compose/preview/copy/schedule/IDOR) | ✅ phủ (~30) | NEW-737 IDOR V2 (#42749/#42752) — error runner |
| Step/Scenario ステップ配信 (soạn/list/step/send-test/job) | ✅ phủ (~35) | NEW-513 send-test V3 PHP — error runner |
| AutoReply 自動応答 (list/create_v2/callback/get-list-group) | ✅ phủ (~45) | **thiếu abnormal binding text → R3/§7** |
| Action-schedule 実行 + Modal アクション SC-004 | ✅ phủ (~18) | NEW-667/670 error runner |
| Remind リマインド配信 + event remind | ✅ phủ (~10) | — |
| Conversion コンバージョン + welcome 新規友だち用 | ✅ phủ (~12) | NEW-1228 copy error runner |

→ `Q`: không thiếu quan điểm lớn. (Encoding text đưa về R4/§7.)

## 3. TC trùng lặp

Rà theo digest 319 TC — các cụm biến thể là **tách phiên bản chủ đích, không trùng**: Template V1 (「テンプレート」) vs V2 (「テンプレート作成」/「テキスト」) · Broadcast V1 (/message-send-all) vs V2 (saveBroadcastV2) · Step cũ (「ステップ配信」 thêm/sửa tin) vs mới (「ステップ配信（作成・編集）」) · AutoReply cũ vs create_v2 (SCR-AR-02). Mỗi cặp kiểm đúng phiên bản code khác nhau. **Không đề nghị xóa.** (Không đọc đủ steps 319 TC nên không khẳng định DUP-EXACT tuyệt đối — Leader soi cụm nghi ngờ nếu cần.)

## 4. Mâu thuẫn trong TCs

Rà digest + `dev_impact` — **không phát hiện CONF-TC / CONF-SPEC / CONF-KHO**.
- NEW-1228 (conversion copy): bản sao **giữ nguyên tên gốc** (2 dòng cùng tên) — ghi rõ "production cũng vậy, `ConversionController::copyConversion` giữ tên"; **không** mâu thuẫn, là hành vi chủ đích.
- **CONF-IGNORE**: không có (các màn cũ Template登録/step cũ/scenario-setting cũ vẫn trong phạm vi, không thuộc `ignore-features.md`).

## 5. Issues khác

| # | Severity | TC / phạm vi | Vấn đề | Đề xuất |
|---|---|---|---|---|
| 1 | `[BLOCKER]` cross-ref B3b | 98 TC gắn #44065 · 7 fail (NEW-9/10/164/165/166/351/832) | **Media trong tin (Intervention Image v3)** là hotspot nâng cấp — fail cụm mp3/mp4/image map/EXIF/PNG trong suốt/carousel. Cùng root với B3b | Validate phần media của B3a **cùng bản vá #44065** của B3b; chưa pass thì chưa kết luận được template/broadcast/step có media |
| 2 | `[MAJOR]` | 13 TC `error` (dev `unknown`): NEW-419/667/513/670/737/1228/523/667… | Lỗi **runner dev**, nhiều cái **local pass/partial** → chưa phải bug sản phẩm nhưng **không có kết luận test** | Re-run trên QA PHP 8.5; nếu local pass + dev tái hiện error → điều tra runner, không raise bug sản phẩm vội |
| 3 | `[MAJOR]` (exec + RULE-08) | Toàn batch B3a | **144/319 pass (45%)** · 66 skip · 89 chưa chạy · **0 prd/staging** (dev 216, local 14) | Chạy lại trên QA + prd cho media (RULE-08) và tin gửi thật qua LINE |
| 4 | `[MINOR]` | 130/319 TC `viewpoint`=None | Thiếu mã quan điểm → khó map coverage theo mã | Gán mã (`MSG-*`/`FUNC-*`/`MEDIA-*`) khi có dịp |

Chất lượng TC: **cao** — oracle = base/production, phân biệt rõ lỗi-có-sẵn (PB-T21-8 cloneFilter, PB-T21-26 step cũ, /null 404 layout) vs lỗi nâng cấp; IDOR broadcast/action được kiểm bằng ca hợp lệ (#42749/#42752); builder tin giữ thứ tự + phần tử trùng (buildTemplateMessages).

## 6. TCs thừa / ngoài phạm vi task

Rà 319 TC — **không có TC thừa/ngoài phạm vi #43845**. (Các TC richmenu/QR/popup/friend/tag/account bị classifier kéo nhầm đã loại ở bước curate → thuộc B3b/B4/B7 delta, không tính vào B3a.)

## 7. TCs đề xuất bổ sung (7)

Đã đối chiếu 319 TC + `dev_impact` (F6/F9) + checklist A5. 3 RISK có cơ sở regression chưa có TC chuyên (R3/R4 message-authoring + R5 error-list):

> **Bổ sung 2026-10-27 — rà riêng cụm Error list (配信エラー / エラーリスト v2) theo 4 maincase** (14 TC error-list cluster; feature cross-cutting delivery-result, không có file kho riêng). **4/4 maincase ĐỦ thiết kế**: (1) 3 tab × 4 loại tin (1:1チャット/メッセージ配信/ステップ配信/その他) + badge — NEW-706 (pass) · (2) phân trang group-count — NEW-823/706 · (3) chi tiết — NEW-707/990/991 (preview không giữ nhầm nội dung) · (4) xóa + đặt lịch resend — NEW-707/680 (bulk 1001 qua job). **1 hole duy nhất**: nhánh **thực thi gửi lại thật** (すぐに再送 / job tới giờ) → tin re-delivered + chuyển tab **再送済み履歴** chưa có TC (NEW-707 cố ý KHÔNG resend, NEW-680 chỉ dừng ở 再送登録済み) → **R5** bên dưới (RULE-06 output cuối).

> **Bổ sung 2026-10-27 — rà cụm Scenario (ステップ配信 FA-009) theo 8 maincase** (83 TC cluster + kho FA-009): **8/8 maincase ĐỦ thiết kế → KHÔNG đẻ TC mới** (AP-5). (1) CRUD scenario+step — NEW-593/663/2001-2003/348-350 · (2) folder CRUD/sort — NEW-1805/1806/1996/1998 · (3) job gửi theo bước mọi loại tin (LINE SDK v12) — NEW-208/512/513/1807/1178 · (4) filter A6 + start/stop thủ công — NEW-663/1804/1382/1491/1663-1665/1527/1780-1781 · (6) list/copy/xóa — NEW-591/1174/1180/506/592/1997 · (7) JP/emoji A5 + null A4 — NEW-348/353/1185/352/1999/2000 · (8) line-friend nhận đúng + đúng thời điểm (A2 N日後 08:30) — NEW-208/1803/1804/2007. **(5) Media trong step** (image NEW-351 **fail**) = cross-ref **R1 #44065** (đã BLOCKER), video/audio/PDF step qua NEW-512 + cụm media #44065 — không TC riêng. **A1-stable sort** scenario-list cover representative qua TC-FUNCSEQ001-01 (template, cùng list-component). Lưu ý exec: nhiều TC skip/None + 0 prd (B3a §5).

> **Bổ sung 2026-10-27 — rà cụm Remind (リマインド配信 /basic/events, action_type=event) theo 6 maincase** (44 TC cluster + kho FA-021): **5/6 maincase ĐỦ thiết kế**: (1) CRUD remind+step — NEW-267/268/269/270/988/2102-2115 · (3) job gửi LINE SDK v12 — NEW-514/2106/2107/994 · (4) filter A6 + list/sort — NEW-665/1050/2107/2102 · (5) line-friend nhận đúng thời điểm — NEW-2106/2108/2110/2111 · (6) JP/emoji A5 + null A4 — NEW-2110/365/2105/666. **1 strengthening**: maincase 2 **A2 diffIn SIGNED [MAJOR]** — chỉ NEW-2109 (1 mốc 30/4, `exec=None`) → mở rộng matrix biên nhuận/cuối năm/cận hiện tại ở **R6** bên dưới.

> **Bổ sung 2026-10-27 — rà Template theo 8 maincase** (137 TC template: CRUD 53 · media 27 · send-test 34 · token 16). 7/8 maincase ĐỦ (CRUD đủ 10 loại · ma trận send-test đầy đủ · A5 encoding mạnh nhờ NEW-1882 không double-encode + NEW-360/65/66 + TC-MSG001-01 · folder CRUD). 1 ô trống đẻ thêm 1 TC: **MC5 — tie-stability (A1) + drag-reorder position cho template list** (TC-FUNCSEQ001-01). Minor chỉ ghi chú, không đẻ TC: PDF-trong-template upload/download (có thể chỉ là URL token — đã có NEW-67) · chặn ảnh >10.000px (MED-L10, chỉ có TC resize 2048px NEW-167) · null/param xấu tới API template (A4, đã gián tiếp qua NEW-587/1849/1329).

> **Bổ sung 2026-10-27 — rà Action schedule (アクションスケジュール) theo 6 maincase** (NEW-456/507/508/577/667/668/669/670/700/983/984/1327 + 769). 4/6 ĐỦ: MC1 CRUD (507/668/669/670/700/983/984) · MC2 thời điểm 実行予定 A2 (507/668/669) · MC5 filter A6 + sort A1 (769/1327/577/667) · (một phần MC6 validate 700). 2 ô trống cốt lõi — đúng điểm nóng **job nền + LINE SDK v12 + A2/A4**: **MC3** chuỗi action chạy khi schedule **fire** (NEW-456 chỉ hẹn rồi **huỷ**) · **MC4** **cron fire trên PHP8** đúng giờ JST + A2/A4 edge (NEW-667 chỉ XEM 実行予定/実行済) → 2 TC (gộp MC6 ngày quá khứ/null/biên vào TC cron). Toàn bộ `manual` + ENV có `prd`/`staging` (RULE-08 job/output).

| ID | Nhóm | Mã quan điểm | Màn hình/chức năng | Loại case | Chạy | Phạm vi ENV | Surface | Tên case | Tiền điều kiện | Các bước thực hiện | Dữ liệu nhập | Kết quả mong đợi | Kết quả thực thi | Ghi chú |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TC-FUNC001-06 | API | FUNC-001 | Trả lời tự động 自動応答: khớp từ khoá chứa ký tự đặc biệt sau đổi binding SQL | Abnormal | auto | dev, local, prd, staging | line-friend, api | Auto-reply khớp đúng rule khi từ khoá/tin bạn bè chứa ký tự SQL/LIKE/khoảng trắng — không mis-match, không injection | Bot test có 3 auto-reply: A rule khớp chính xác 「100%OFF」, B khớp chứa 「a_b」, C khớp chứa 「株式会社」. Bạn F01 đã kết bạn, chưa chặn. | 1. F01 gửi lần lượt: 「100%OFF」, 「100XOFF」, 「a_b」, 「axb」, 「株式会社 ① test」, và chuỗi có `'` `%` `_` `\` `"`. 2. Với mỗi tin, đọc auto-reply bot trả về + bản ghi log callback. | 6 tin như trên (gồm ký tự `' % _ \ "` và JP ①㈱) | A chỉ khớp đúng 「100%OFF」 (không khớp 「100XOFF」 — `%` không bị coi là wildcard); B khớp 「a_b」 không khớp 「axb」 (`_` không là wildcard); C khớp cả 2 chuỗi chứa 「株式会社」. Không tin nào gây lỗi 500/SQL error; không auto-reply nào khớp nhầm. Hành vi = bản 5.5. | | Lấp R3 · basis: `dev_impact` "Auto-reply HandleCallbackMessage binding SQL text tin nhắn và id auto_reply" — binding tham số có thể đổi cách khớp `%`/`_`; cụm 自動応答 hiện thiếu abnormal ký tự đặc biệt · auto (runner mô phỏng callback) |
| TC-MSG001-01 | UI | MSG-001 | Mẫu tin テンプレート: text chứa & < " ' / emoji round-trip save→mở lại→gửi (A5 encoding PHP8) | Normal | auto | dev, local, prd, staging | web, line-friend | Tin text có ký tự đặc biệt HTML + emoji lưu, mở lại, gửi tới LINE giữ nguyên không bị escape nhân đôi | Bot test, màn 「テンプレート作成」 loại 「テキスト」. Bạn F01 kết bạn. | 1. Tạo template text nội dung `A&B <tag> "quote" 'apos' 100%OFF 🎉①㈱`. 2. Lưu, mở lại template để đối chiếu ô text. 3. Gửi thử template tới F01. 4. Đọc tin trên LINE F01. | `A&B <tag> "quote" 'apos' 100%OFF 🎉①㈱` | Ô text sau mở lại hiển thị **đúng nguyên văn** (không thành `&amp;` / `&lt;` / `&quot;` nhân đôi, không mất emoji/①㈱). Tin F01 nhận đúng nguyên văn. Lưu DB không double-encode. Hành vi = bản 5.5. | | Lấp R4 · basis: PHP8.1 đổi mặc định `htmlspecialchars`/`htmlentities` sang ENT_QUOTES\|ENT_HTML5 (checklist A5) → nguy cơ double-encode `"`/`'`; NOTE NEW-419 ghi "ký tự & < \" thuộc t7" nhưng chưa có TC round-trip chuyên · auto |
| TC-FUNCSEQ001-01 | UI | FUNC-SEQ-001 | Danh sách Template 「テンプレート（一覧）」: thứ tự khi **nhiều template trùng khoá sort** + **chuỗi thêm→sort→sửa→sort→xoá→sort** giữ nguyên sau F5 (A1 sort STABLE + position) | Normal | auto | dev, local, prd, staging | web | Thứ tự hiển thị/sắp xếp template giống hệt bản cũ dù PHP8 đổi `sort` thành stable; drag-reorder + reload giữ đúng vị trí | Bot test, 1 folder có **≥4 template cùng `作成日`/`最終編集日`** (tạo trùng mốc để ép khoá sort bằng nhau) + ≥2 template có thể kéo đổi `position`. Có mốc thứ tự hiển thị của cùng dữ liệu trên production/bản cũ | 1. Mở 「テンプレート（一覧）」, sort theo cột 作成日 (rồi 最終編集日) — ghi thứ tự các template **cùng mốc ngày**. 2. Kéo đổi vị trí 2 template (drag-reorder), ghi thứ tự. 3. Thực hiện chuỗi liên tiếp KHÔNG reload: thêm 1 template→quan sát sort, sửa 1 template→sort, xoá 1 template→sort. 4. F5 tải lại trang. 5. So từng bước với mốc bản cũ (MAP-SORT-01) | Dữ liệu có ≥4 template cùng khoá 作成日/最終編集日; ≥2 template kéo đổi vị trí | Các template **cùng khoá sort** giữ **thứ tự chèn** như PHP7.2 (PHP8 `sort` stable — không đảo ngẫu nhiên). Drag-reorder lưu đúng `position`, sau F5 (bước 4) thứ tự **không đổi** (FUNC-SEQ-001/MAP-SORT-01). Chuỗi thêm/sửa/xoá→sort không làm nhảy thứ tự so với bản cũ. Không màn nào 500/JS error | | Lấp MC5 · A1 checklist upgrade (sort STABLE) + MAP-SORT-01/FUNC-SEQ-001 (template trong ma trận sort) · regression · bổ sung cho TC-LIST001-01 (B3b) vốn chỉ phủ richmenu/QR/popup · dẫn từ framework/php-upgrade-checklist A1 · auto · Đánh giá spec: Spec không ghi (quy tắc PHP8, Leader chốt so mốc bản cũ) |
| TC-MSG001-02 | Job | MSG-001 | 配信エラー / エラーリスト v2 — Thực thi gửi lại (すぐに再送 + lịch tới giờ) → tin tới LINE + chuyển tab 再送済み履歴 | Normal | manual | dev, local, prd, staging | line-friend, web, job | Gửi lại tin lỗi (ngay + theo lịch) cho 2 loại (1:1チャット + メッセージ配信) → tin tới đúng LINE user, chuyển tab 再送済み履歴 nội dung/thời điểm đúng, badge giảm | Bot test; F01 kết bạn (đã bỏ chặn để nhận lại). Seed 2 tin lỗi của F01 (is_confirmed=0): 1 loại 1:1チャット (type=2) text JP, 1 loại メッセージ配信 có emoji. Worker queue chạy. Có mốc hành vi production | 1. 配信エラー → loại 1:1チャット → tab 未確認エラー → 詳細 → 「すぐに再送する」 → xác nhận. 2. Quan sát LINE F01 nhận lại tin + tin chuyển sang 再送済み履歴 + badge 1:1チャット -1. 3. Với tin メッセージ配信: 詳細 → đăng ký 再送タイミング (giờ tương lai gần) → đợi worker tới giờ chạy. 4. Sau job: kiểm LINE F01 nhận tin + tin nằm tab 再送済み履歴 loại メッセージ配信 với 再送日時 (JST) đúng. 5. Kiểm tab 再送済み履歴 không có checkbox/xoá | 2 tin lỗi: 1:1チャット (JP text) + メッセージ配信 (emoji) của F01 | Gửi ngay (b1-2): F01 nhận lại đúng nội dung trên LINE; tin rời 未確認エラー sang 再送済み履歴, badge 1:1チャット -1. Gửi theo lịch (b3-4): job tới giờ chạy, F01 nhận tin, tin nằm 再送済み履歴 loại メッセージ配信 với 再送日時 = giờ đã đặt (JST), không gửi trùng/lặp (attempts=1). Tab 再送済み履歴 không thao tác xoá/checkbox. Nội dung JP/emoji không vỡ. KHÔNG 500/TypeError PHP8 trong job gửi lại. Giống production | | Lấp R5 (maincase 1 tab 再送済み履歴 content + maincase 4 resend EXECUTION — RULE-06 output cuối tới LINE) · NEW-707 cố ý KHÔNG resend, NEW-680 chỉ tới 再送登録済み → nhánh gửi-lại-thật + 再送済み履歴 chưa có TC · regression job SendingScheduleSendChat + F6 gửi LINE SDK v12 · manual vì cần LINE thật · ENV chứa prd (RULE-08 output/job) · Đánh giá spec: Đã hỏi leader (hành vi production) |
| TC-FUNCDATE001-02 | Job | FUNC-DATE-001 | リマインド配信 (/basic/events) — Tính mốc nhắc qua ranh giới NĂM / THÁNG NHUẬN + cận hiện tại (A2 diffIn SIGNED) | Boundary | manual | dev, local, prd, staging | line-friend, job, web | Remind 「終了N日前 HH:MM」 tính send-time đúng JST ở mốc nhuận/cuối năm/cận hiện tại — không lệch do diffIn SIGNED PHP8 | Bot test, U1 kết bạn chưa chặn, job remind chạy. Reminder R có bước 「リマインド終了 1日前 10:00」. Có mốc base release_step_20260930_v2 cùng dữ liệu | 1. Đăng ký U1 vào R với 4 mốc kết thúc qua UI: (a) 2028-03-01 (năm nhuận), (b) 2027-03-01 (không nhuận), (c) 2027-01-01 (qua năm), (d) kết thúc = hôm nay+1 ngày (diff nhỏ, kiểm dấu). 2. Mở lại kiểm cấu hình + mốc dự kiến. 3. Theo dõi LINE U1 tại từng mốc 1日前 10:00 JST, ghi thời điểm thực nhận. 4. So từng mốc với base | 4 end-date: 2028-03-01 · 2027-03-01 · 2027-01-01 · hôm nay+1 | Mỗi mốc 1日前 10:00 JST tính đúng: (a) **2028-02-29** 10:00 (nhuận, không nhảy 03-01/02-28), (b) **2027-02-28** 10:00, (c) **2026-12-31** 10:00 (qua năm), (d) đúng hôm nay 10:00. U1 nhận mỗi tin **đúng một lần** đúng thời điểm JST, không lệch ngày/múi giờ, không gửi sớm/trùng do diffIn trả SIGNED ở PHP8/Carbon. Khớp base. KHÔNG 500/TypeError trong job scan | | Lấp R6 (maincase 2 — A2 diffIn SIGNED + JST, [MAJOR]) · mở rộng NEW-2109 (chỉ 1 mốc 30/4, exec=None) sang nhuận 29/2 / cuối năm / cận hiện tại (bắt lỗi dấu diffIn PHP8) · regression A2 (event_step_time / ScenarioStepTime diffIn signed) · manual vì cần job qua mốc + LINE thật · ENV chứa prd (RULE-08 job/time) · Đánh giá spec: Đã hỏi leader (so mốc base) |
| TC-FUNCSCHEDULE001-01 | API | FUNC-SCHEDULE-001 | アクションスケジュール: cron fire đúng giờ JST (PHP8) → **chuỗi action chạy thật** (tag + template + đổi rich menu) trên friend đã lọc | Normal | manual | dev, local, prd, staging | job, line-friend | Lịch hẹn tới giờ → cron PHP8 fire → action chain (gắn tag · gửi template · đổi rich menu) chạy đúng cho đúng tập friend qua LINE SDK v12 | Bot test có 1 アクションスケジュール 「AS-FIRE」 đặt giờ fire **gần (vài phút tới)**, action chain = [gắn tag `AS-DONE` + gửi template `AS-TPL` + đổi rich menu sang RM-B]; đối tượng lọc = friend có tag `SEG-A`. 2 friend LINE thật: F-A (tag SEG-A), F-B (không). Cron action_schedules bật trên runner PHP8. Mốc production | 1. Tạo/kiểm lịch AS-FIRE (実行予定 = giờ gần). 2. Để cron chạy tới giờ (hoặc chạy tay job executor). 3. Đúng thời điểm JST: kiểm F-A được gắn tag AS-DONE + nhận template AS-TPL trên LINE + rich menu đổi RM-B. 4. Kiểm F-B (không SEG-A) KHÔNG bị tác động. 5. Mở 「アクションスケジュール実行」 → 実行済 ghi nhận | lịch AS-FIRE (tag+template+richmenu); F-A/F-B | Cron PHP8 fire **đúng giờ JST** (không lệch UTC/±1 ngày); chuỗi action chạy **đủ** cho F-A: tag AS-DONE gắn, template AS-TPL tới LINE (SDK v12 build đúng), rich menu đổi RM-B. F-B bị lọc, không chạy. 実行済 ghi đúng. KHÔNG 500/TypeError PHP8 trong job. Giống production | | Lấp MC3 (chuỗi action chạy khi fire — NEW-456 chỉ hẹn rồi huỷ) + MC4 (cron fire trên PHP8, A2 JST) · regression F6 LINE SDK v12 + job nền PHP8 + F2 filter · manual + prd (RULE-08 job/output/LINE) · Đánh giá spec: Đã hỏi leader (hành vi production) |
| TC-JOB001-01 | Job | JOB-001 | アクションスケジュール cron PHP8: ngày quá khứ / null / biên tháng (29-31, nhuận) / khung 00:00-09:00 JST → fire/skip đúng, không 500/TypeError (A2/A4) | Boundary | manual | dev, local, staging | job | Cron executor xử lý các lịch có mốc ngày biên/xấu mà không crash, fire hoặc bỏ qua đúng quy tắc như bản cũ | Seed các lịch: (a) 実行予定 **quá khứ** (đã qua), (b) ngày kết thúc **null**/không set, (c) lịch tháng ngày 31 vào tháng ngắn (→30/28/29 nhuận), (d) 実行予定 rơi **00:00-09:00 JST**. Cron action_schedules trên runner PHP8. Mốc production | 1. Chạy cron executor. 2. (a) lịch quá khứ: xử lý theo rule bản cũ (fire bù / bỏ qua), không treo. 3. (b) ngày kết thúc null: không TypeError, lịch chạy/dừng đúng. 4. (c) ngày 31 tháng ngắn: fire vào ngày biên đúng (cuối tháng), không nhảy sai. 5. (d) khung 00:00-09:00 JST: fire đúng ngày JST, không lệch sang hôm trước. 6. Kiểm log + 実行済/実行予定 | lịch quá khứ · null end · ngày 31 · 00:00-09:00 JST | Cron PHP8 xử lý **mọi** case không 500/TypeError (A4 null): quá khứ theo rule bản cũ, null end-date không crash, ngày 31→cuối tháng đúng (Carbon A2), khung 00:00-09:00 fire đúng ngày JST (không lệch −1 ngày). Trùng khít production PHP7.2 | | Lấp MC4 (cron A2/A4 trên server mới) + MC6 (ngày quá khứ/null/biên A4) · regression A2 Carbon signed + A4 null TypeError trong job PHP8 · manual · ENV chứa staging (job nền RULE-08) · Đánh giá spec: Spec không ghi chi tiết (quy tắc PHP8, so mốc bản cũ) |

## 8. Spec update needed

| # | Điểm cần chốt | Nguồn | Ai chốt |
|---|---|---|---|
| 1 | **13 TC `error/unknown` trên dev** (NEW-419/513/667/670/737/1228/523…) — là lỗi runner hay bug thật? Nhiều cái local pass. Triage trước khi raise bug sản phẩm | NEW-419/667/513… | QA + Dev |
| 2 | Phần **media trong tin** của B3a (98 TC #44065) chốt chung với bản vá Intervention v3 ở B3b — khi nào #44065 Close thì mới kết luận template/broadcast/step có media | #44065 · B3b | Dev + Leader |

---

# BATCH B8 — Form answer / Google Sheet

> ⚠️ **Snapshot mới 2026-10-26** (1537→~2018 TC). B8 **chưa từng review**. Lọc tay từ TC chưa-review theo màn フォーム/回答/スプレッドシート + feature form-answer/shop-card. **= 59 TC.** 3 TC lệch batch (NEW-1317 trang lỗi 404/500/503 → B11 · NEW-794 知らせ発行 → B11 system · NEW-126 友だち情報管理 → B4) lọt vào do keyword, ghi ở §6.

## 0. Nguồn TC
- **Nguồn đã dùng**: MCP LME TEST STUDIO — task_id=507, ticket 43845 (subset B8: form CRUD v1/v2/v3 · 分岐タイプ rẽ nhánh · 診断 scoring · delete/restore · folder · CSV câu trả lời (SJIS) · upload/download tệp đính kèm · escape/CSRF trang công khai · LIFF form enduser + friend_info field · Googleスプレッドシート連携 (OAuth/relink/resync/append job)).
- **Tổng số TC review**: 59.

> **Đã áp [framework/php-upgrade-checklist.md](../../framework/php-upgrade-checklist.md)**. Trục nâng cấp B8: **A5 encoding** (escape trang form công khai + CSV SJIS) · **Intervention v3 / media** (upload-download tệp — #44065, 12/59 TC) · **D-7 đọc file media server** (`stream_get_meta_data`) · **D-11 upload guard** (đuôi nguy hiểm → 422) · **Google apiclient + job Java** (sync spreadsheet). 28/59 pass (47%), **0 prd/staging**.

## 1. Coverage — dev-impact + diff code

- **dev-impact: CHƯA ĐỦ (chưa xác nhận + 1 fail).** Form CRUD/分岐/診断, CSV, upload/download, escape/CSRF, LIFF, Google Sheet sync đều có TC. **Nhưng** 28/59 pass, **NEW-70 fail (dev) + 2 error runner**, 0 prd.
- **diff code: CHƯA ĐỦ (chưa xác nhận).** Khớp `dev_impact`: D-7 `MediaFileService::readMediaFile`, D-11 upload guard (#43715), Google Sheet job `HandleFormAnswerSyncGoogleSheetTask`, escape form công khai, IDOR/tool-scope form của chính bot.

| Mã | Chiều | Vùng ảnh hưởng | TC hiện có | Status | Ghi chú |
|---|---|---|---|---|---|
| R1 | dev-impact + diff | **NEW-70 tải tệp đính kèm qua media/CDN** (D-7 `stream_get_meta_data` thay `$http_response_header`) | NEW-70 **fail@dev / pass@local** | **RISK → [MAJOR] plausible regression** | fail đúng nhánh vừa sửa, chỉ kích hoạt khi file KHÔNG trên đĩa web (media server). Local có file trên đĩa → pass. Cần xác định dev-fail là lỗi đọc media thật hay env |
| R2 | dev-impact + diff | **Google Sheet sync (OAuth + job Java + spreadsheet thật)** | NEW-391/392/1030/1031/1035/1036/1039/1034 — **toàn skip** | **RISK** | RULE-08: tích hợp ngoài + job nền + Google thật, chưa chạy prd; job ghi theo thứ tự phần tử neo A1 (không tra header) |
| R3 | diff | **Upload/download tệp media trong form** (#44065 Intervention v3) | NEW-70/735/736/1334 + 12 TC #44065 | **RISK cross-ref B3b** | cùng hotspot media; D-11 upload guard local pass (422 cho đuôi nguy hiểm) nhưng dev error runner |

**Kết luận §1**: 0 GAP · **3 RISK** (R1 media-read [MAJOR] triage · R2 Google Sheet sync prd · R3 media upload/download cross-ref B3b). Coverage thiết kế ĐỦ.

## 2. Thiếu so với quan điểm test

Độ phủ: FUNC form CRUD/v3 ✅ · 分岐/診断 scoring (NEW-368/819/827) ✅ · delete+restore ✅ · OUT-EXPORT CSV SJIS (NEW-402/496) ✅ · SEC-ESCAPE escape 1 lần (NEW-649/650/651/652) ✅ · SEC-CSRF (NEW-650/655) ✅ · SEC-UPLOAD D-11 (NEW-735/736) ✅ · LIFF-ENTRY form enduser v1/v3 + friend_info field xóa/còn + 年月日 + action theo giá trị (NEW-1003/1004/1056/1059/1061/1062) ✅ · INTG-SHEET OAuth/relink/resync/append ✅ · DATA-DB cleanup remind khi xóa page (NEW-1038) ✅.

→ `Q`: không thiếu quan điểm. (A5 encoding form công khai + CSV đã có TC chuyên — không đẻ thêm.)

## 3. TC trùng lặp

Rà 59 TC — **không trùng**. Các biến thể tách chủ đích: form v1/v2 vs v3 (code khác); LIFF form bản cũ (NEW-1059) vs mới (NEW-1056) kiểm nhánh friend_info khác; Google Sheet resync-từ-đầu (NEW-1030) vs append-dòng-mới (NEW-1031) là 2 nhánh job khác. Giữ nguyên.

## 4. Mâu thuẫn trong TCs

Rà 59 TC × memory/kho form + `dev_impact` — **không mâu thuẫn**.
- ✅ **Khớp rule hard-delete**: NEW-371 expected ghi đúng "khôi phục form thì **câu trả lời đã xoá KHÔNG quay lại** (xoá vĩnh viễn #4173)" — trùng [[form-delete-answers-hard-deleted]]; TC ghi đúng, không phải CONF.
- **CONF-IGNORE / dead-code**: `FormAnswerController::downloadViewerOld` (audit runtime-audit:1513) **không có route** (code chết) — NEW-496 kiểm đường thật `downloadViewer`. Không phải ignore-feature; ghi §8 để Leader chốt có cần TC cho hàm chết không.

## 5. Issues khác

| # | Severity | TC / phạm vi | Vấn đề | Đề xuất |
|---|---|---|---|---|
| 1 | `[MAJOR]` (triage) | NEW-70 (`fail@dev`, pass@local, #44065) | Tải tệp đính kèm qua **media/CDN** fail trên dev — đúng nhánh D-7 `MediaFileService::readMediaFile` (`stream_get_meta_data`). Có thể là **regression đọc file media thật** | Dựng file trên media server (không trên đĩa web) + chạy lại; nếu tái hiện fail → raise bug D-7 |
| 2 | `[MAJOR]` (exec + RULE-08) | Toàn batch B8 | **28/59 pass (47%)** · 28 skip · **0 prd/staging** (dev 55, local 4). Google Sheet sync + CSV + upload/download chưa chạy môi trường thật | Chạy Google Sheet sync + upload/download trên QA có Google thật + media server (RULE-08) |
| 3 | `[MINOR]` (triage) | NEW-496 (`error@local`), NEW-736 (`error@dev`, pass@local) | Lỗi **runner unknown**, không phải bug sản phẩm (NEW-736 local pass 422 đúng; NEW-496 kiểm dead-code path) | Re-run; không raise bug vội |

Chất lượng TC: **cao** — oracle = production/base cụ thể (D-7/D-11/#4173/#43715), phân biệt dead-code (downloadViewerOld) vs đường thật, escape-once rõ ràng, IDOR form của chính bot (tool-scope). LIFF + job sync nêu rõ cần Google/spreadsheet thật.

## 6. TCs thừa / ngoài phạm vi task

Trong phạm vi #43845 — **không có TC thừa**. 3 TC **lệch batch** (vẫn thuộc task, chỉ sai nhóm do classifier): NEW-1317 (trang lỗi 404/500/503 → thuộc **B11**), NEW-794/NEW-655 (知らせ発行 system notification → **B11**), NEW-126 (友だち情報管理 độ dài tên trường → **B4**). Sẽ tính ở batch đúng khi delta-sweep; không đề nghị xóa.

## 7. TCs đề xuất bổ sung (0)

Đã đối chiếu 59 TC + `dev_impact` + checklist A5 + memory form. **Không đề xuất TC mới** — escape form công khai (A5), CSV SJIS (A5), upload guard D-11, media read D-7, Google Sheet sync (OAuth/relink/resync/append/job), 診断 scoring, LIFF friend_info, delete/hard-delete answers đều đã có TC. Việc cần làm: **triage NEW-70 (media/CDN)** + **chạy Google Sheet + upload/download trên prd/QA thật**, không phải viết thêm (AP-5).

## 8. Spec update needed

| # | Điểm cần chốt | Nguồn | Ai chốt |
|---|---|---|---|
| 1 | **NEW-70**: xác định tải tệp media/CDN fail trên dev là bug đọc file thật (D-7) hay env chưa dựng media server → raise bug nếu thật | NEW-70 | Dev + QA |
| 2 | `FormAnswerController::downloadViewerOld` (code chết, không route) — có cần TC riêng hay xác nhận bỏ hẳn (thêm `ignore-features.md`)? | NEW-496 | Leader + Dev |
| 3 | Spec `form-answer` BR-07 **thiếu rule** "xoá form → câu trả lời xoá vĩnh viễn, khôi phục không có lại" (#4173) — bổ sung vào spec để khỏi hiểu nhầm (TC NEW-371 đang ghi đúng) | NEW-371 · [[form-delete-answers-hard-deleted]] | Leader (cập nhật spec) |
