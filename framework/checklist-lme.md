# Quan điểm test LME — Tầng 1 (80 quan điểm / 18 nhóm + 12 RULE)

> **Nguồn**: [Bảng quan điểm test — HỢP NHẤT ELME v1.0](https://docs.google.com/spreadsheets/d/1IijLnq0gLZDFxOMWOYxXafz1Wnzv3W0g/edit?gid=1184713662#gid=1184713662) (2026-07-10, biên soạn: QA Lead) — file `.xlsx` trên Drive, 13 sheet.
>
> v1.0 **hợp nhất 2 nguồn**: bộ checklist vận hành cũ của team (CL-Func-xx / CL-NonF-xx / CLJ01 / các tính năng chung) + bộ quan điểm dựng từ 129 bug history. Sheet 9 "Truy vết" chứng minh **không mục nào của checklist cũ bị mất**. Vì vậy file này **thay thế hoàn toàn** bản checklist-lme cũ (fetch 2026-06-25) — mã CL-Func-xx đã được quy về mã quan điểm mới.
>
> Ngày fetch: 2026-07-13. Sync lại: `uv run scripts/fetch_xlsx.py 1IijLnq0gLZDFxOMWOYxXafz1Wnzv3W0g <out.xlsx>` (file là Office, **không** đọc được bằng Sheets API).

---

## 0. Cách dùng — đọc trước khi viết/review TC

### 0.1 Kiến trúc 2 tầng

| Tầng | File | Trả lời câu hỏi |
|---|---|---|
| **Tầng 1 — Quan điểm** | File này | "Soi ở góc nào?" — 80 quan điểm / 18 nhóm |
| **Tầng 2 — Catalog** | [catalog-lme.md](catalog-lme.md) | "Ở đâu trong LME, nhập dữ liệu gì?" — 21 kiểu input (A), 15 thành phần UI (B), bản đồ 21 đường gửi tin (C), khác biệt production (D/D2), ma trận media (E) |

**Cầu nối**: mỗi quan điểm ghi `Catalog: A/B/C/D/E`; mỗi dòng catalog ghi ngược lại mã quan điểm liên kết.

> **Viết TC = đọc quan điểm ở tầng 1 → mở đúng catalog ở tầng 2 để lấy dữ liệu và vị trí cụ thể. Bỏ bước hai là chỗ bug lọt.**

### 0.2 Ba khái niệm KHÔNG được lẫn

- **RULE** (§1) — quy định quy trình. Vi phạm → kết quả test **không được nghiệm thu**, dù quan điểm đã tick đủ.
- **Quan điểm** (§2) — góc nhìn kỹ thuật cần soi. Leader định nghĩa.
- **Test case** — cụ thể hóa quan điểm thành: làm gì / nhập gì / mong đợi ra sao. Member viết.

### 0.3 Độ ưu tiên = mức RỦI RO nếu lọt bug (không phải độ khó test)

- **Luôn Cao**: tiền & gói cước; thông tin cá nhân; gửi tin & đối tượng nhận tin; xóa/copy dữ liệu đang được tham chiếu; quyền truy cập API; xử lý trùng; migration trên dữ liệu thật; nhật ký thao tác; asset khi release; khác biệt production.
- **Nâng lên Cao có điều kiện** (nền Trung bình): UI/thông báo khi có nguy cơ **báo thành công giả**; định dạng dữ liệu khi ảnh hưởng URL/LIFF/thanh toán/tin nhắn; đồng bộ app khi có output trên app hoặc LINE; dữ liệu lớn khi là gửi tin/export/sync; media khi ảnh gửi ra cho LINE user.
- **Trung bình**: UI chỉn chu, khác biệt trình duyệt không ảnh hưởng dữ liệu; luồng phụ có cách né tạm.
- **Thấp**: trải nghiệm nhỏ, câu chữ không ảnh hưởng quyết định của user hay dữ liệu.
- **Phân vân → chọn mức cao hơn và ghi lý do.**

### 0.4 Loại case — chỉ 3 giá trị

`Normal` / `Abnormal` / `Boundary`.

> Cột `Loại case` của [templates/04-tc-list.template.md](../templates/04-tc-list.template.md) dùng **đúng 3 giá trị này** — bám sheet canonical "7. Ví dụ test case". **Không có loại thứ 4.**
>
> **Regression không phải 1 loại case.** TC verify tính năng cũ không hỏng (quan điểm nhóm REG-* / COMPAT-LEGACY-001, impact T* trong `03-dev-impact.md`) xếp vào `Normal` (luồng cũ chạy đúng) hoặc `Abnormal` (điều kiện lỗi cũ), và ghi chữ `regression` ở cột `Ghi chú`.
>
> **Ưu tiên không phải 1 cột.** Bảng TC không có cột Priority — độ ưu tiên suy ra từ ưu tiên của **mã quan điểm** ở §2 (cột `Mã quan điểm liên kết` của TC).
>
> _(Format cũ 4 giá trị `Positive/Negative/Boundary/Regression` + cột Priority chỉ còn tồn tại ở các task folder tạo trước 2026-07-16 — giữ nguyên, không convert.)_

### 0.5 Khi phân vân Đạt / Không đạt

- Spec không ghi rõ → lấy chuẩn "hành vi mà user bình thường sẽ mong đợi". Phân vân → ghi Ghi chú + báo leader, **không tự quyết rồi bỏ qua**.
- "Không báo lỗi nhưng vỡ layout" và "trên LINE app thật bị lỗi dù màn admin vẫn bình thường" — **cả hai đều là lỗi**.
- Quan điểm liên quan tag / phân khúc / đối tượng gửi tin: **bắt buộc test tới bước nhận tin thật trên LINE app (iOS + Android)**, không dừng ở màn xem trước.

---

## 1. 12 RULE bắt buộc

| Mã | Tên rule | Nội dung |
|---|---|---|
| **RULE-01** | **PATTERN TỐI THIỂU** | Quan điểm ưu tiên **Cao**: tối thiểu **3 TC — Normal + Abnormal + Boundary**. Thiếu 1 trong 3 phải ghi lý do (VD: quan điểm không có khái niệm biên). Trung bình/Thấp: tối thiểu 1 Normal, khuyến khích thêm Abnormal. |
| **RULE-02** | **EVIDENCE BẮT BUỘC** | Chỉ tick Đạt khi đã đính kèm **đúng loại** bằng chứng ghi ở cột Evidence của quan điểm. Không chấp nhận "đã xem, OK". |
| **RULE-03** | **LÝ DO KHI ĐÁNH ×** | Đánh × (không áp dụng) bắt buộc điền lý do. Quan điểm **Cao** mà lý do mơ hồ → phải có leader approve. |
| **RULE-04** | **XÁC NHẬN PHẠM VI KHI RECOVERY** | Bug làm sai dữ liệu → trước khi đóng ticket phải có query/thống kê **toàn hệ thống** xác nhận phạm vi ảnh hưởng. Không recovery 1 tài khoản rồi kết luận cảm tính "hiếm gặp". |
| **RULE-05** | **NGUỒN SPEC BÊN THỨ 3** | Trước khi viết TC cho tính năng tích hợp **LINE / Google / Stripe / UnivaPay**, phải tra tài liệu chính thức **MỚI NHẤT** của bên đó. Không dựa trí nhớ. |
| **RULE-06** | **OUTPUT CUỐI CHUỖI** | Không dừng ở màn admin. Mọi quan điểm có output ra ngoài (LINE app, mobile app, Google, payment gateway, file export, email) phải verify **tại output cuối trên thiết bị/hộp thư thật**. |
| **RULE-07** | **VERIFY 3 TẦNG** | Với mọi CRUD: khớp 3 nơi — (1) DB, (2) màn hình, (3) output/thông báo. Kiểm tra DB là **bắt buộc**, không thay bằng UI. Tạo bản ghi trùng tên ở 2 tài khoản để kiểm chứng `WHERE`. |
| **RULE-08** | **MÔI TRƯỜNG** | Trước khi kết luận "đã test xong", đối chiếu [Catalog D](catalog-lme.md#catalog-d--khác-biệt-dev--staging--production). Hạng mục **media / domain / job / loadbalance / bill tiền** **không được** kết luận từ staging. |
| **RULE-09** | **CŨ & MỚI SONG SONG** | Mọi tính năng đã từng version-up phải test **cả nhánh cũ và mới** (template group, form `s.lmes.jp` vs `step3.lmes.jp`, remind cũ/mới, header spread cũ/mới). |
| **RULE-10** | **VÒNG ĐỜI CHECKLIST** | Mỗi bug **lọt ra production** bắt buộc sinh 1 dòng quan điểm hoặc 1 dòng catalog mới, có ID + ngày thêm + nguồn bug. Leader review hàng tháng. |
| **RULE-11** | **NGUỒN DỮ LIỆU KHI CẬP NHẬT BẢNG** | Dùng Redmine: tracker Bug KH + toàn bộ ticket con của ticket tổng hợp hàng tháng `[SNSLine] CHECK REPORT FROM CUSTOMER`. **CHỈ** ticket Closed / Resolved / Fix done / Released mới được dùng làm bằng chứng. |
| **RULE-12** | **PHẠM VI REGRESSION** | Không chạy lại toàn bộ quan điểm Cao mỗi release. Gồm 3 phần: (1) bộ **smoke cố định** do leader định nghĩa (đăng nhập, gửi tin cơ bản, thanh toán, đặt lịch); (2) **vùng ảnh hưởng theo danh sách của DEV** (REG-SHARED-001); (3) **mọi case đã từng Không đạt và được fix**. |

---

## 2. 80 quan điểm test

> Ký hiệu mỗi mục: `MÃ` — quan điểm · **Ưu tiên** · `Catalog cần mở kèm`.
> **Trigger** = cột "Khi nào bắt buộc chọn". **Evidence** = bằng chứng bắt buộc khi tick Đạt (RULE-02).
> `★` = bổ sung mới ở v1.0 (phái sinh từ checklist vận hành cũ hoặc bug history).

### 2.1 Chức năng (Functional)

#### `FUNC-001` — Luồng chính hoàn tất đúng đặc tả · **Cao** · Catalog C
- **Trigger**: mọi chức năng — luôn bắt buộc.
- **Kiểm tra**: chạy input mẫu trong spec từ đầu đến cuối. Xác nhận **3 điểm khớp nhau**: DB / màn hình / thông báo-output. Có output cuối chuỗi (LINE app, mobile app, Google, gateway, file export) → phải kiểm output đó (RULE-06). Kiểm cả nội dung dialog xác nhận + thông báo hoàn tất.
- **Evidence**: screenshot màn hình + bằng chứng output cuối chuỗi (tin LINE thật / file export / bản ghi gateway).

#### `FUNC-002` — Hành vi khi bỏ trống trường bắt buộc · **Cao** · Catalog A
- **Trigger**: mọi chức năng có form nhập liệu.
- **Kiểm tra**: lần lượt bỏ trống **từng** trường bắt buộc → báo lỗi rõ trường nào + chặn lưu. Test **đủ các luồng vào**: tạo mới / sửa / **copy** / import CSV / gọi API trực tiếp (validation thường khác nhau giữa các luồng). Field optional để trống hợp lệ cũng phải test (bug copy/action-unset từng xảy ra ở đây).
- **Evidence**: screenshot thông báo lỗi **từng luồng** (create/edit/copy/import).

#### `FUNC-003` — Nhập dữ liệu sai định dạng · **Trung bình** (→ Cao khi field liên quan URL/LIFF, ngày giờ, số tiền, token, webhook URL, PII) · Catalog A
- **Trigger**: mọi field có định dạng quy định (email, SĐT, URL, ngày tháng).
- **Kiểm tra**: half-width/full-width (半角/全角) lẫn lộn, chỉ ký tự đặc biệt, chuỗi quá dài. **Frontend chặn được nhưng gọi thẳng API vẫn lưu được** = lỗi kinh điển → phải test cả server-side.
- **Evidence**: screenshot lỗi validation frontend **VÀ** kết quả gọi API trực tiếp.

#### `FUNC-004` — Giới hạn trên/dưới về số ký tự, số lượng · **Cao** · Catalog A, C
- **Trigger**: mọi chức năng có giới hạn số lượng / ký tự / dung lượng.
- **Kiểm tra**: **5 pattern** — đúng biên, biên+1, biên−1, 0, chuỗi rỗng. TC phải **ghi rõ nguồn của giới hạn**: spec nội bộ / giới hạn plan / spec LINE-Google-Stripe-UnivaPay / kiểu dữ liệu DB / quy mô khách hàng lớn nhất thực tế. Nhiều lỗi do limit thực tế khác biên lý thuyết (VD cột 1 byte → 127/128).
- **Evidence**: ghi rõ nguồn limit + kết quả test 5 pattern.

#### `FUNC-MULTI-001` — Đa phần tử cùng loại · **Trung bình** · Catalog A
- **Trigger**: chức năng cho phép thêm ≥2 phần tử cùng loại trong 1 đối tượng (nhiều file upload, nhiều URL trong 1 tin, nhiều điều kiện lọc).
- **Kiểm tra**: tạo đối tượng có 2-3 mục cùng loại → tất cả phải hoạt động, **không chỉ mục đầu tiên**. Thử trộn nhiều loại mục khác nhau trong cùng 1 đối tượng.
- **Evidence**: bằng chứng TẤT CẢ phần tử hoạt động.

#### `FUNC-DATE-001` — Ngày giờ sát ranh giới · **Cao** · Catalog A
- **Trigger**: chức năng có tính toán / so sánh ngày giờ (hạn, "N ngày sau", remind).
- **Kiểm tra**: 23:00–23:59, 00:00–00:59, ngày cuối/đầu tháng, 31/12→01/01, timezone (JST/local), **0:00 vs 24:00**, 29/2 năm nhuận, tháng 30 vs 31 ngày, năm quá khứ/tương lai (so sánh ngày bằng **chuỗi** sẽ sai khi khác năm).
- **Evidence**: bảng kết quả test các giá trị biên thời gian đã chạy.

#### `FUNC-DRAFT-001` — Giữ nội dung soạn dở khi chuyển màn · **Trung bình** · Catalog B
- **Trigger**: **chỉ** editor/soạn thảo (chat, template, form builder). KHÔNG áp dụng đại trà.
- **Kiểm tra**: nhập dở → chuyển đối tượng/màn khác → quay lại → nội dung còn nguyên.
- **Evidence**: video/screenshot thao tác chuyển ngữ cảnh và quay lại.

#### `FUNC-UNIQ-001` — Unique check phải loại trừ chính bản ghi đang sửa · **Trung bình** · Catalog A
- **Trigger**: có field bắt buộc duy nhất (email, mã số) và user sửa được bản ghi của mình.
- **Kiểm tra**: update lại chính bản ghi với giá trị giữ nguyên/đổi nhẹ → **không** được báo "đã tồn tại". Kiểm thêm hoa/thường (case-insensitive), space đầu/cuối.
- **Evidence**: screenshot update chính bản ghi của mình thành công, không báo trùng.

#### `FUNC-SEQ-001` ★ — Thao tác liên tiếp & reload · **Trung bình** · Catalog C
- **Trigger**: **BẮT BUỘC** với màn có ≥2 thao tác trên cùng danh sách (đặc biệt có **Sort**), hoặc nhiều tab setting chung 1 nút Save.
- **Kiểm tra**: chạy các chuỗi **không reload giữa chừng** — Add→Add · Xóa→Xóa · Xóa→Add · Sort→sửa trạng thái · Add→Sort · Edit→Sort · Xóa→Sort · Sort→Sort · Edit→Edit. Sau **mỗi** chuỗi: **F5** → dữ liệu + thứ tự sort phải giống hệt trạng thái ngay sau thao tác. Màn nhiều tab: chuyển qua lại các tab rồi mới Save → dữ liệu các tab không đổi/mất.
- **Evidence**: screenshot sau chuỗi thao tác + sau F5 (2 ảnh cạnh nhau). _(Nguồn: CL-Func-2/3/4)_

### 2.2 Đồng thời & Idempotency

#### `CONC-001` — Một hành động logic chỉ được xử lý 1 lần · **Cao** · Catalog C
- **Trigger**: **BẮT BUỘC** khi có nút thực thi hành động quan trọng / nhiều người cùng sửa / batch đa luồng / giới hạn dùng chung.
- **Kiểm tra**: **4 kịch bản** — (1) double-click 1 nút; (2) cùng user thao tác song song trên 2 tab/2 thiết bị; (3) 2 user khác nhau sửa cùng 1 bản ghi gần đồng thời (mỗi bên 1 field); (4) batch đa luồng cùng chạm 1 giới hạn dùng chung → đếm kết quả cuối. Hệ thống phải **khóa hoặc báo xung đột**, không âm thầm xử lý trùng / ghi đè mất dữ liệu.
- **Evidence**: bằng chứng **số lần xử lý thực tế** (log/DB/số tin nhận được) sau khi cố tình thao tác trùng.

#### `CONC-002` — Re-sync toàn bộ vs dữ liệu mới · **Trung bình** (→ Cao với form/payment/chat/friend) · Catalog D
- **Trigger**: có tiến trình re-sync/tính lại **TOÀN BỘ** dữ liệu cũ chạy nền, và dữ liệu mới có thể phát sinh trong lúc đó.
- **Kiểm tra**: xóa sheet đích để kích hoạt re-sync toàn bộ (form nhiều nghìn bản ghi), **đồng thời** gửi thêm 1 câu trả lời mới ngay trong lúc re-sync đang chạy → không trùng, không mất.
- **Evidence**: đối chiếu số bản ghi trước/sau re-sync + bản ghi mới phát sinh giữa chừng.

#### `CONC-003` ★ — Race ở tầng giao diện · **Trung bình** (→ Cao khi màn có loadmore/phân trang + filter, hoặc nhiều tab cùng gọi API) · Catalog B
- **Trigger**: × chỉ khi màn hình chỉ có 1 request tĩnh. _(Khác CONC-001: đây là race tầng **client**, response về không đúng thứ tự gửi.)_
- **Kiểm tra**: (1) chuyển nhanh giữa nhiều tab khi API trước chưa trả về → dữ liệu phải thuộc tab **đang chọn**; (2) loadmore/infinite scroll vừa load vừa scroll/filter → không trùng bản ghi, không nhảy vị trí; (3) DevTools Network throttling (Slow 3G) chạy lại luồng chính; (4) chủ động delay 1 response → UI phải **bỏ qua response cũ**; (5) bấm filter/search liên tiếp → kết quả cuối khớp điều kiện **cuối cùng**.
- **Evidence**: video/GIF thao tác nhanh + screenshot Network tab thể hiện thứ tự response. _(Nguồn: CL-Func-27)_

### 2.3 Toàn vẹn dữ liệu

#### `DATA-001` — Dữ liệu cập nhật phản ánh đủ ở mọi màn liên quan · **Cao** · Catalog C
- **Trigger**: mọi chức năng cập nhật dữ liệu được tham chiếu ở nơi khác.
- **Kiểm tra**: nơi cần đối chiếu — màn tóm tắt / màn chi tiết / export / API / mobile app / LINE app / dịch vụ ngoài (Google) / lịch sử thao tác. VD gán tag → đồng bộ ở 4 nơi: list khách hàng, chi tiết khách hàng, **điều kiện gửi tin**, màn phân tích. Cache làm chậm phản ánh = lỗi (trừ khi spec ghi rõ độ trễ).
- **Evidence**: bảng đối chiếu **từng nơi hiển thị** sau khi cập nhật.

#### `DATA-COUNT-001` — Số đếm & tổng hợp · **Cao** · Catalog C
- **Trigger**: **BẮT BUỘC** khi màn hình có bất kỳ con số đếm / tỷ lệ / tổng hợp nào.
- **Kiểm tra**: (1) chuẩn bị bộ dữ liệu **biết trước kết quả** (gửi 10, mở 3 = 30%) → đối chiếu **phép tính tay**; (2) cùng 1 số liệu phải khớp giữa **4 nguồn**: màn tóm tắt / màn chi tiết / CSV export / API. Chú ý **mẫu số**, timezone theo ngày, và cách xử lý **friend đã block**.
- **Evidence**: bảng đối chiếu 4 nguồn + phép tính tay.
- ⚠️ **Là lỗi lặp nhiều nhất lịch sử bug** — 12 ticket Closed trên 5 tính năng.

#### `DATA-TEXT-001` — Emoji & ký tự đặc biệt · **Trung bình** (→ Cao nếu text được gửi LINE / export CSV) · Catalog A
- **Trigger**: có input text tự do sẽ được lưu / hiển thị / gửi qua LINE / export.
- **Kiểm tra**: emoji, ①②③, ㈱, ký tự kiểu cũ → lưu → hiển thị list → **nhận tin thật trên LINE** để đối chiếu. Màn admin đúng nhưng LINE lỗi font / mất emoji = lỗi.
- **Evidence**: screenshot chuỗi test ở **cả** màn quản trị VÀ LINE app thật / file export.

#### `DATA-REF-001` — Reference integrity (xóa / copy / rename / move) · **Cao** · Catalog C
- **Trigger**: **BẮT BUỘC** khi đối tượng có thao tác xóa/copy/đổi tên/di chuyển VÀ được nơi khác tham chiếu.
- **Kiểm tra**: (1) xóa đối tượng đang được tham chiếu → nơi tham chiếu hiển thị trạng thái đã xóa rõ ràng, **không sập màn**; (2) copy/rename/move → bản sao phải **độc lập**, mọi nơi tham chiếu bản sao hiển thị đúng thông tin bản sao, **không dính bản gốc** (copy action mà code friend info vẫn giữ giá trị bản gốc là bug thật đã xảy ra). Copy khi dữ liệu tham chiếu **đã bị xóa** (tag/template/staff/ảnh) → vẫn hoàn tất, không văng exception.
- **Evidence**: bằng chứng kiểm tra **từng nơi tham chiếu** sau thao tác.

#### `DATA-ID-001` — Định danh bằng ID duy nhất, không bằng tên hiển thị · **Trung bình** (→ Cao với màn chọn đối tượng để thao tác)
- **Trigger**: chức năng hiển thị/chọn/nhóm đối tượng có thể **trùng tên**.
- **Kiểm tra**: tạo 2 đối tượng **trùng tên hiển thị** → thao tác từng cái → không bị gộp/nhầm ở bất kỳ màn nào (list, lịch, báo cáo).
- **Evidence**: bằng chứng 2 bản ghi độc lập.

#### `DATA-MIG-001` — Migration dữ liệu cũ · **Cao** · Catalog D
- **Trigger**: **BẮT BUỘC** khi release đổi cấu trúc dữ liệu và tồn tại dữ liệu cũ. Dấu hiệu trong spec: "tương thích ngược" / "migration" / "移行" / "định dạng mới" / "version-up" / đổi cấu trúc field.
- **Kiểm tra**: lấy mẫu dữ liệu cũ từ **nhiều thời điểm / nhiều nguồn tạo khác nhau** (không chỉ dữ liệu mới sau release) → xem/sửa/lưu không lỗi. Kiểm thêm: so sánh before/after, dry-run, kế hoạch rollback, migration **chạy lại được** (idempotent), path ảnh/file sau migrate (lỗi `//`).
- **Evidence**: kết quả kiểm tra mẫu dữ liệu cũ từ nhiều nguồn/thời điểm sau migration.

#### `DATA-CACHE-001` — Cache / dữ liệu cũ (stale) · **Trung bình** (→ Cao nếu output user-facing) · Catalog D
- **Trigger**: release có đổi JS/asset, hoặc chức năng dùng short link / preview / cache tầng ngoài.
- **Kiểm tra**: (1) trước deploy mở sẵn 1 tab (không refresh) → sau deploy thao tác tiếp trên tab đó (JS cũ đọc data format mới); (2) xóa/đổi dữ liệu gốc đang được cache (short link, URL preview) → gửi lại và kiểm nội dung **thật trên LINE**; (3) popup có cache riêng trên production.
- **Evidence**: bằng chứng test tab cũ sau deploy / nội dung LINE thật sau khi đổi dữ liệu gốc.

#### `DATA-BACKUP-001` ★ — Backup / Copy / Recover · **Cao** · Catalog C
- **Trigger**: **BẮT BUỘC** khi tính năng **thêm/đổi bảng DB**, hoặc chạm backup / copy bot / restore data đã xóa mềm.
- **Kiểm tra**: (1) tạo bản ghi có **đủ setting phụ** (tag, template, action, ảnh, ngày lặp lại); (2) backup → xóa/đổi → recover; (3) **query DB đối chiếu từng field** nguồn↔đích, tập trung: **ngày lần đầu vs ngày tiếp theo (không được trùng)**, path ảnh (không có `//`), foreign key; (4) sau recover mở list/detail/preview không lỗi; (5) recover khi tài khoản đích **thiếu quyền / thiếu route phân quyền**; (6) tính năng mới thêm bảng DB → **verify bảng đó nằm trong phạm vi backup và copy**.
- **Evidence**: kết quả query đối chiếu trước/sau (dán bảng) + screenshot sau recover. _(Nguồn: CL-NonF-10)_

#### `DATA-DB-001` ★ — Xác minh ở tầng DB (WHERE scope + khóa mồ côi) · **Cao** · Catalog C
- **Trigger**: **BẮT BUỘC** với mọi chức năng có UPDATE hoặc DELETE. **Không thay thế được bằng kiểm tra trên UI** (RULE-07).
- **Kiểm tra**: (1) tạo bản ghi **TRÙNG tên/trùng ngày ở 2 tài khoản** (2 bot, 2 staff); (2) update/delete ở tài khoản A → query DB xác nhận **tài khoản B không đổi** (`WHERE` đủ `bot_id`/`master_id`/`staff_id`/`course_id`); (3) xóa hết bản ghi con (VD toàn bộ `action_detail`) → `action_id` ở setting cha **phải bị xóa theo**, không còn ID mồ côi; (4) mở lại list/detail/preview không lỗi.
- **Evidence**: ảnh chụp kết quả query trước/sau (kèm câu query) trên 2 tài khoản. _(Nguồn: CL-Func-11, CL-Func-17)_

#### `DATA-AUDIT-001` — Audit log / Lịch sử thao tác · **Cao**
- **Trigger**: **BẮT BUỘC** khi có thao tác xóa/sửa/đổi trạng thái trên **dữ liệu nhạy cảm** (khách hàng, thanh toán/hợp đồng, phân quyền, tag). Dấu hiệu spec: màn `操作履歴` / lịch sử thao tác / audit / activity log.
- **Kiểm tra**: thực hiện **cùng 1 thao tác từ TỪNG nguồn**: web / app / action job / multi action / campaign → mỗi lần đúng **1 bản ghi lịch sử**, đủ **4 thông tin**: người thực hiện / thời gian / hành động / giá trị cũ→mới. Ghi nhầm loại thao tác (xóa ghi thành thêm mới) = lỗi.
- **Evidence**: screenshot/export bản ghi lịch sử sau **mỗi** thao tác, cho **từng nguồn**.
- ⚠️ Lỗ hổng thật của bộ quan điểm cũ — 10/10 ticket Closed (#33464, #33468, #33469, #33483, #34166, #36459, #36460, #36537, #34151, #33425).

### 2.4 Tích hợp & Đồng bộ

#### `INTG-LINE-001` — Lỗi từ LINE API / LIFF / webhook · **Cao** · Catalog D
- **Trigger**: **BẮT BUỘC** khi chức năng gọi LINE API / LIFF / nhận webhook LINE.
- **Kiểm tra**: giả lập rate limit, timeout, webhook lỗi/mất, LIFF init lỗi, user block/unblock. Không chỉ `send` API — **LIFF, follow event, webhook nhận, rich menu API** cũng phải xét. Lỗi kinh điển: **vẫn hiện "đã gửi thành công" dù thực tế chưa gửi được**.
- **Evidence**: log lỗi + hành vi hệ thống khi giả lập **từng loại** lỗi LINE.

#### `INTG-HOOK-001` — Webhook trễ / trùng / mất thứ tự · **Cao** · Catalog D
- **Trigger**: **BẮT BUỘC** khi nhận webhook từ bên ngoài (thanh toán, LINE, Google).
- **Kiểm tra**: gửi trùng 1 webhook 2 lần → chỉ được xử lý **1 lần** (dựa event ID / idempotency key). Thêm: đến trễ, sai thứ tự, mất hẳn, retry từ phía gửi, gửi lại thủ công.
- **Evidence**: webhook payload/log gốc + idempotency key + **SỐ LẦN XỬ LÝ THỰC TẾ** (đếm từ log/DB) + trạng thái cuối. **Không chấp nhận** "đã thử gửi trùng, thấy bình thường" — phải có log chứng minh lần thứ 2 bị bỏ qua.

#### `INTG-HOOK-002` — Callback/webhook KHÔNG tới · **Trung bình** · Catalog D
- **Trigger**: luồng nghiệp vụ chỉ hoàn tất khi nhận callback/webhook từ bên ngoài.
- **Kiểm tra**: chạy luồng ở môi trường test/staging (nơi webhook **có thể chưa cấu hình**) → phải có timeout / retry / thông báo, **không treo vô thời hạn**. Không được bỏ qua với lý do "production webhook luôn tới".
- **Evidence**: hành vi hệ thống (timeout/retry/thông báo) khi chặn callback.

#### `INTG-CAL-001` — Đồng bộ 2 chiều lịch ngoài · **Cao** · Catalog C
- **Trigger**: **BẮT BUỘC** khi đồng bộ lịch/sự kiện 2 chiều với dịch vụ ngoài (Google Calendar).
- **Kiểm tra**: **3 hướng riêng biệt** — (1) LME→ngoài (tạo/hủy/đổi); (2) ngoài→LME; (3) thao tác **gần như đồng thời từ cả 2 phía** → xử lý conflict.
- **Evidence**: bằng chứng đủ 3 hướng.
- ⚠️ 10 ticket Closed — điểm yếu lặp lại nhiều nhất của Salon.

#### `INTG-SHEET-001` — Đồng bộ spreadsheet ngoài · **Cao** · Catalog C
- **Trigger**: **BẮT BUỘC** khi ghi dữ liệu khách hàng (câu trả lời form...) ra spreadsheet ngoài.
- **Kiểm tra**: đổi định dạng cột trong file đích rồi tiếp tục ghi; di chuyển/đổi tên file; flow nhiều nhánh/nhiều trang; ghi **nhiều bản ghi liên tiếp nhanh**; quyền truy cập bị đổi; rate limit API; recovery khi sync đứt giữa chừng.
- **Evidence**: đối chiếu bản ghi hệ thống vs sheet sau **từng kịch bản phá**.

#### `SYNC-APP-001` — Đồng bộ Web ⇔ Mobile app ⇔ LINE app · **Trung bình** (→ Cao với flow critical user-facing) · Catalog C, E
- **Trigger**: tính năng có mặt trên cả web và app.
- **Kiểm tra**: đổi dữ liệu ở web → kiểm app (không restart, pull-to-refresh) và ngược lại. Nghiệp vụ **dùng chung web↔app** → thay đổi phải release **đồng bộ cả hai bên**, hoặc ghi rõ bên nào không áp dụng + **ai xác nhận**. Bug kinh điển: sửa Web nhưng quên triển khai sang app.
- **Evidence**: screenshot cùng thao tác trên **cả** web và app.

### 2.5 Phân quyền

#### `PERM-001` — Menu/nút hiện đúng theo role · **Cao** · Catalog C
- **Trigger**: **BẮT BUỘC** khi chức năng có phân biệt quyền.
- **Kiểm tra**: **phải có role matrix trong spec trước khi test** (không có → không bắt đầu test được). Đăng nhập từng role (owner/admin/staff + role không hợp lệ), liệt kê menu/nút hiện-ẩn → đối chiếu ma trận.
- **Evidence**: ma trận role đã test đủ + screenshot từng role.

#### `PERM-002` — Không được bypass quyền bằng API / URL trực tiếp · **Cao** · Catalog C
- **Trigger**: **BẮT BUỘC** khi có thao tác nhạy cảm (xóa / thanh toán / export / PII).
- **Kiểm tra**: gọi thẳng API / dán URL của thao tác đã bị **ẩn trên UI** → phải trả **403**. Lập mapping màn hình × API endpoint. Đường truy cập cần thử: menu chính / menu favourite / gõ thẳng URL / hyperlink dẫn tới màn đó.
- **Evidence**: kết quả gọi API trực tiếp bằng role không đủ quyền (mã lỗi trả về).

#### `PERM-003` — Cách ly dữ liệu đa tài khoản LINE OA · **Cao** · Catalog C
- **Trigger**: **BẮT BUỘC** khi tổ chức vận hành nhiều LINE OA hoặc có chức năng **change bot**.
- **Kiểm tra**: chuyển qua lại giữa các tài khoản → friend list / lịch sử gửi tin / tag phải độc lập. Kiểm before/after khi **change bot**, lấy friend cũ (既存友だち取得), webhook / provider / rich menu / greeting sau khi switch.
- **Evidence**: bằng chứng dữ liệu tách biệt sau switch/change bot.

#### `PERM-004` — Thu hồi/đổi quyền có hiệu lực đúng thời điểm · **Trung bình** (→ Cao khi quyền liên quan PII hoặc thanh toán)
- **Trigger**: **BẮT BUỘC** khi có thao tác mời/xóa/đổi quyền thành viên.
- **Kiểm tra**: đổi quyền của thành viên **đang đăng nhập** → session cũ còn thao tác được không; gọi API trực tiếp bằng session cũ; giới hạn số staff.
- **Evidence**: hành vi session đang mở ngay sau khi bị thu hồi quyền.

### 2.6 Gửi tin / LINE đặc thù

#### `MSG-001` — Điều kiện lọc người nhận phải gửi ĐÚNG đối tượng · **Cao** · Catalog C
- **Trigger**: **BẮT BUỘC** với mọi chức năng gửi tin có điều kiện lọc.
- **Kiểm tra**: kết hợp AND/OR, **đếm tay số người khớp trước** → đối chiếu số người nhận thực tế. **Bắt buộc xác nhận nhận thật trên LINE app**, không chỉ nhìn số đếm. Thêm: include/exclude kết hợp; filter **bị mất sau copy/sort**; tag trong điều kiện bị xóa/đổi tên.
- **Evidence**: danh sách người nhận thật (LINE app) khớp **100%** điều kiện lọc.
- ⚠️ **Gửi nhầm đối tượng = lỗi nghiêm trọng nhất**, luôn ưu tiên cao nhất.

#### `MSG-002` — Tin đặt lịch / step gửi đúng thời điểm · **Cao** · Catalog C
- **Trigger**: **BẮT BUỘC** với gửi tin đặt lịch / step theo thời gian.
- **Kiểm tra**: **không bấm rồi kết luận ngay** — phải chờ thời gian thật trôi qua hoặc chỉnh giờ server. Kiểm timezone, 23:00–00:00, cuối tháng, **đổi giờ sau khi job đã lên lịch**, độ trễ batch.
- **Evidence**: log giờ gửi thực tế vs giờ cấu hình (kèm sai số).

#### `MSG-003` — Xử lý blocked user · **Cao** · Catalog C
- **Trigger**: **BẮT BUỘC** với mọi chức năng gửi tin hàng loạt.
- **Kiểm tra**: trong đối tượng gửi có người **đã block OA** → cả lượt gửi vẫn hoàn tất, **số đếm/tính phí không tính nhầm**.
- **Evidence**: kết quả gửi khi danh sách có user đã block (không lỗi, đếm đúng).

#### `MSG-004` — Preview admin phải khớp nội dung nhận thật trên LINE · **Cao** · Catalog C, E
- **Trigger**: **BẮT BUỘC** khi output là nội dung user cuối nhìn thấy trên LINE.
- **Kiểm tra**: gửi tin có emoji, xuống dòng, rich menu, ảnh → **nhận thật trên LINE app** rồi so với preview admin. **KHÔNG được chỉ test ở màn preview rồi cho Đạt.**
- **Evidence**: screenshot LINE app thật **iOS VÀ Android**.

#### `MSG-005` — Giới hạn số tin theo tháng · **Cao** · Catalog C
- **Trigger**: **BẮT BUỘC** khi chức năng tiêu thụ quota tin nhắn.
- **Kiểm tra**: test limit−1 / limit / limit+1. **Phân biệt rõ limit của LME theo plan và limit của LINE OA**. Nội dung cảnh báo phải ghi **đúng tên plan thực tế** (từng có bug hiện sai tên plan Lite/Standard).
- **Evidence**: hành vi tại limit−1/limit/limit+1 + nội dung cảnh báo đúng plan.

#### `MSG-USER-001` — LINE user lifecycle · **Cao** · Catalog C
- **Trigger**: **BẮT BUỘC** khi chức năng tương tác với friend LINE ở bất kỳ dạng nào.
- **Kiểm tra**: từng trạng thái — friend **mới add**; friend **cũ lấy về qua 既存友だち取得**; friend **block rồi unblock**; **LINE user not exists** (đã xóa tài khoản); **follow event đến trễ/trùng**. Với mỗi trạng thái: friend list / rich menu / greeting / lịch sử / action có chạy đúng không. Bug thật: action chỉ chạy với friend mới add; rich menu không hiện lại sau unblock; QR scan **trước khi** action được tạo.
- **Evidence**: bảng kết quả từng trạng thái lifecycle (screenshot LINE app + màn quản trị).

#### `LIFF-ENTRY-001` ★ — Điểm vào của link phía LINE user · **Cao** · Catalog C
- **Trigger**: **BẮT BUỘC** khi tính năng phát sinh URL cho LINE user access (form, item, event, salon, lesson, conversion, QR code, popup).
- **Kiểm tra**: **ma trận bắt buộc** cho từng loại link —
  - **Trạng thái user**: CHƯA là bạn của OA → phải **redirect sang màn kết bạn**; ĐÃ là bạn → vào thẳng.
  - **Điểm vào**: mở trong app LINE (in-app browser) / trình duyệt ngoài / từ button trong tin nhắn / từ PC.
  - **Loại link**: link mới (`s.lmes.jp`) và link cũ (`step3.lmes.jp`) — **cả hai** phải access được.
  - Sau khi vào: hoàn tất luồng **tới output cuối** (lưu result, ghi spreadsheet, chạy action form).
- **Evidence**: screenshot trên máy thật: 1 ảnh in-app LINE + 1 ảnh trình duyệt ngoài + 1 ảnh case chưa kết bạn. _(Nguồn: CL-Func-13)_

### 2.7 Output & Preview

#### `OUT-PREVIEW-001` — Preview / test-send vs output THẬT · **Cao** · Catalog C, E
- **Trigger**: **BẮT BUỘC** khi chức năng có chế độ preview hoặc test send.
- **Kiểm tra**: preview/test-send pass **chưa đủ** (preview và luồng thật dùng code path khác nhau) → bắt buộc chạy thêm 1 lần **luồng thật**: gửi thật cho tài khoản test, mở **URL gửi thật** (không phải URL preview). So từng điểm: spacing, media, tên người gửi, biến `[name]`, action gắn kèm. Upload file: path + preview **trước** khi save và **sau** khi save phải giống nhau.
- **Evidence**: cặp screenshot preview vs thật, cùng nội dung.

#### `OUT-TRUTH-001` — UI/message khớp trạng thái THẬT · **Cao**
- **Trigger**: **BẮT BUỘC** với mọi thao tác lưu/gửi/đồng bộ **có thông báo kết quả**.
- **Kiểm tra**: báo "thành công" thì dữ liệu phải **THẬT SỰ** được lưu/đồng bộ/gửi; báo lỗi thì phải **đúng nguyên nhân**. Đổi cấu hình hiển thị (tên người gửi, avatar) → kiểm **cả 2 phía độc lập**: UI hiển thị đúng cấu hình mới **VÀ** hành động thực tế (tin gửi đi) cũng dùng cấu hình mới.
- **Evidence**: đối chiếu thông báo UI với dữ liệu thật trong DB / màn khác / log job.

#### `OUT-EXPORT-001` ★ — CSV / Spreadsheet export · **Trung bình → BẮT BUỘC (nâng Cao)** với mọi chức năng export CSV / ghi Google Spreadsheet / sinh file cho khách tải · Catalog C, A
- **Kiểm tra**: (1) **từng cột** trong file == giá trị trên màn hình (đặc biệt cột enum/phân loại — test **từng giá trị riêng biệt**); (2) format datetime đúng spec (**có giờ nếu spec ghi có giờ**); (3) tên file chứa ký tự đặc biệt / tiếng Nhật / dài sát **255 byte** → vẫn tải được; (4) encoding **UTF-8 và Shift-JIS** → mở Excel không mojibake; (5) dữ liệu chứa dấu phẩy → phải bọc trong `"`; (6) export vượt ngưỡng (>500 bản ghi form answer) và ở quy mô khách lớn nhất; (7) **giá trị 0 vs bỏ trống** phân biệt rõ, không mất số 0 đầu; (8) tiêu đề cột spreadsheet có xuống dòng.
- **Evidence**: file export thật (đính kèm) + screenshot màn hình tương ứng. _(Nguồn: TC-05, TC-23)_

#### `NOTI-MAIL-001` ★ — Gửi email · **Trung bình → BẮT BUỘC (nâng Cao)** khi mail chứa link xác thực / thanh toán / khôi phục mật khẩu · Catalog C
- **Kiểm tra**: gửi tới **đủ ma trận nhà cung cấp** — Gmail · Yahoo (`@yahoo.ne.jp` **và** `@yahoo.co.jp`) · iCloud · Hotmail · Outlook · domain riêng (`@wssj.co.jp`, `@watermelon.vn`). Với mỗi hộp thư: (1) nhận đủ mail; (2) **Sender = `noreply@lmes.jp` (L Message公式)**; (3) tiêu đề + nội dung đúng spec; (4) **KHÔNG nằm trong Spam/Junk**. Gửi nhiều lần liên tiếp → không mất, không trùng.
- **Evidence**: screenshot hộp thư đến của tối thiểu Gmail + Yahoo + 1 domain riêng. _(Nguồn: CL-Func-26)_

### 2.8 Giao diện / UX

#### `UI-001` — Responsive theo surface · **Trung bình** (→ Cao với flow critical user-facing) · Catalog B
- **Trigger**: mọi chức năng có UI.
- **Kiểm tra**: mở trên **đúng các surface áp dụng**: admin web (PC), mobile app, LINE LIFF. Mỗi surface có bằng chứng riêng: không vỡ layout, thao tác chính **bấm được**. Bắt buộc kiểm ở **1366×768** (độ phân giải thấp nhất hỗ trợ).
- **Evidence**: screenshot từng surface (PC / app / LIFF).

#### `UI-002` — Khác biệt trình duyệt / thiết bị · **Trung bình** · Catalog B
- **Trigger**: mọi chức năng có UI user-facing.
- **Kiểm tra**: danh sách tối thiểu — **Mac Safari + Chrome** (user chính là chủ salon/cửa hàng nhỏ, dùng Safari nhiều), Windows Chrome, Android file picker, LINE app iOS/Android. Đặc biệt input ngày giờ.
- **Evidence**: kết quả test trên danh sách trình duyệt/thiết bị tối thiểu.

#### `UI-003` — Loading / rỗng / lỗi · **Trung bình** (→ Cao khi có rủi ro **false success**) · Catalog B
- **Trigger**: mọi màn danh sách / xử lý bất đồng bộ.
- **Kiểm tra**: giả lập mạng chậm / dữ liệu 0 kết quả / ngắt kết nối → cả 3 trạng thái có hiển thị rõ, **không trắng màn**, **không loading vô hạn**. Thông báo phải khớp trạng thái job/dữ liệu thật — **không hiện "thành công" khi job nền chưa xong hoặc thất bại**.
- **Evidence**: screenshot 3 trạng thái + đối chiếu trạng thái job thật.

#### `UI-004` — Usability người mới · **Thấp**
- **Trigger**: **chỉ** onboarding hoặc flow phức tạp — KHÔNG phải release gate chung.
- **Evidence**: ghi chú các điểm gây lạc lối + feedback cho spec.

#### `UI-FIELD-001` — Field con theo field cha · **Trung bình** · Catalog B
- **Trigger**: form/settings có field phụ thuộc lựa chọn cha (loại điều kiện, loại action).
- **Kiểm tra**: chọn lần lượt **từng** giá trị field cha → field con đổi đúng, **không giữ lại field con của lựa chọn trước**. Ghi rõ hành vi mong đợi khi đổi cha: field con **reset hay giữ giá trị**? ⚠️ Field con sai có thể khiến user cấu hình nhầm **điều kiện gửi tin** hoặc **số tiền**.
- **Evidence**: screenshot field con đổi đúng theo từng lựa chọn cha.

#### `UI-INPUT-001` ★ — Hành vi ô nhập liệu · **Trung bình** · Catalog A, B
- **Trigger**: **BẮT BUỘC** với mọi màn có ô nhập text / area text.
- **Kiểm tra**: (1) paste bằng **Ctrl+V** VÀ bằng **chuột phải > Paste**, trên **cả Windows và Mac** → button đang disable phải **enable**, validate phải chạy (JS thường chỉ nghe keyboard event → paste chuột phải không kích hoạt validate); (2) trim space đầu/cuối → **kiểm tra DB**; (3) area text: enter / multi-enter → hiển thị đúng, auto-resize hoặc có scroll; (4) maxlength / maxlength+1: **đếm ký tự đúng** cho latinh, full-width JP, half-width JP, symbol, enter, space; (5) nhập đúng maxlength → **không vỡ layout**.
- **Evidence**: screenshot trạng thái button sau khi paste **bằng chuột phải** (Win + Mac) + giá trị lưu trong DB. _(Nguồn: CL-Func-24)_

### 2.9 Thanh toán & Gói cước

> **PHÂN BIỆT**: `PAY-STATE-001` kiểm **TRẠNG THÁI** (đã/chưa thanh toán, hủy, refund) + tính nhất quán 3 nơi. `PAY-AMOUNT-001` kiểm **SỐ TIỀN** cụ thể (pro-rate, thuế, giảm giá). Hai quan điểm **khác bản chất — phải test ĐỘC LẬP**, không thay thế nhau.

#### `PAY-STATE-001` — Nhất quán trạng thái 3 nơi · **Cao** · Catalog C
- **Trigger**: **BẮT BUỘC** với mọi chức năng có giao dịch tiền hoặc đổi trạng thái hợp đồng. Dấu hiệu spec: sơ đồ trạng thái thanh toán, bảng trạng thái đơn hàng, `決済ステータス` / `入金確認中`.
- **Kiểm tra**: dùng thẻ test chạy **từng kịch bản** (thành công / thất bại / hủy / refund / recurring); sau **mỗi** kịch bản mở **cả 3 màn** đối chiếu: admin nội bộ / màn user / dashboard cổng thanh toán (Stripe / UnivaPay) — khớp **tên gói + trạng thái + số tiền**. Thất bại thì **không trừ tiền**.
- **Evidence**: screenshot 3 nơi sau từng kịch bản + log giao dịch.
- 👉 Danh sách error type bắt buộc cover khi fix chạm payment gateway: xem [§3 Phụ lục](#3-phụ-lục-nội-bộ--error-scenarios-payment-gateway).

#### `PAY-PLAN-001` — Đổi gói: reset trạng thái & quyền · **Cao** · Catalog C
- **Trigger**: **BẮT BUỘC** với mọi thao tác thay đổi gói/hợp đồng.
- **Kiểm tra**: đổi gói cho tài khoản **có lịch sử trạng thái cũ** (từng đạt ngưỡng, từng bỏ không dùng lâu) → giới hạn mới + **mọi cảnh báo/modal liên quan ngưỡng** phải tính lại theo **số liệu hiện tại**, không theo lịch sử. Hạ gói khi có dữ liệu **vượt ngưỡng gói thấp** → xử lý đúng spec.
- **Evidence**: bằng chứng trạng thái + giới hạn + cảnh báo sau đổi gói (đặc biệt tài khoản có lịch sử cũ).

#### `PAY-AMOUNT-001` — Độ chính xác số tiền · **Cao** · Catalog C
- **Trigger**: **BẮT BUỘC** khi có tính tiền: pro-rate, đổi chu kỳ, thuế, giảm giá.
- **Kiểm tra**: đổi gói **giữa tháng** → so số hệ thống với **số tính tay**. Thêm: recurring, refund, chuyển khoản ngân hàng, đối soát gateway, đổi chu kỳ tháng/năm, khuyến mãi đang áp dụng.
- **Evidence**: phép tính tay đối chiếu số hệ thống + hóa đơn/receipt thực tế.

#### `PAY-BATCH-001` — Batch re-check trạng thái mới nhất · **Cao** · Catalog C
- **Trigger**: **BẮT BUỘC** khi có xử lý batch/định kỳ tác động **tiền hoặc gửi tin**.
- **Kiểm tra**: cho user **hủy hợp đồng ngay trong lúc batch đang chạy** (giữa lúc lấy danh sách và lúc thực thi) → không được trừ tiền. Batch phải lấy trạng thái **MỚI NHẤT ngay trước khi thực thi**, không dùng trạng thái lấy từ đầu batch.
- **Evidence**: kết quả test hủy/đổi trạng thái **GIỮA** lúc batch lấy danh sách và lúc thực thi.

#### `PAY-CONFIRM-001` — Tạm tính → chính thức · **Cao** · Catalog C
- **Trigger**: **BẮT BUỘC** khi có dữ liệu 2 giai đoạn (tạm → chính thức): hoa hồng affiliate tạm tính, thanh toán tạm giữ, booking tạm, import chờ duyệt.
- **Kiểm tra**: đăng ký gia hạn qua chuyển khoản **nhưng không thanh toán** → dữ liệu tạm tính **không được tự chuyển thành chính thức theo lịch**. Bước chuyển phải **verify lại điều kiện thực tế** tại đúng thời điểm chuyển.
- **Evidence**: bằng chứng bước chuyển có verify lại điều kiện (chưa thanh toán → không confirm).

#### `PAY-ABANDON-001` — Rời luồng thanh toán giữa chừng · **Cao** · Catalog C
- **Trigger**: **BẮT BUỘC** với mọi luồng thanh toán / subscription.
- **Kiểm tra**: **đóng tab ngay sau khi bấm thanh toán**, trước khi nhận kết quả (luồng không có webhook) → phải có cơ chế **đối soát lại** (reconciliation), không để đơn treo vô thời hạn. Nếu khôi phục thủ công → dữ liệu phải đúng **định dạng hiện hành** (đừng lưu theo format cũ khiến không hiển thị được).
- **Evidence**: trạng thái cuối của đơn sau khi bỏ ngang + cơ chế đối soát hoạt động.

#### `PAY-LIMIT-001` — Giới hạn chức năng theo gói · **Cao** · Catalog C
- **Trigger**: **BẮT BUỘC** khi chức năng bị giới hạn theo gói.
- **Kiểm tra**: cần **bảng plan-limit chính thức** làm nguồn. Test **5 case** (xem Catalog C, khối MAP-PLAN): tạo mới / **copy** / **khôi phục data xóa mềm** / **mở 2 tab thao tác tại ngưỡng** / **double click ở lần limit cuối**. Test **cả tài khoản cũ** (tạo trước khi đổi giá/spec) **và mới**. Chức năng **KHÔNG phụ thuộc gói** vẫn phải test trên nhiều gói (bug external link từng lọt vì chỉ test gói Standard).
- **Evidence**: bảng đối chiếu giới hạn từng gói vs hành vi thực tế (cả account cũ/mới).

### 2.10 Trạng thái & Lifecycle

#### `STATE-001` — Quy trình nhiều bước bị gián đoạn · **Cao** · Catalog C
- **Trigger**: **BẮT BUỘC** khi nghiệp vụ gồm **≥2 bước ghi dữ liệu tuần tự** (đổi gói, tạo đơn, connect bot, copy).
- **Kiểm tra**: chủ động **đóng tab / tắt mạng giữa bước 1 và bước 2** → không được để dữ liệu **nửa vời** (bước 1 xong, bước 2 chưa chạy → hiển thị sai vĩnh viễn). Phải có rollback hoặc cơ chế tự phát hiện & hoàn tất phần thiếu.
- **Evidence**: trạng thái dữ liệu sau khi cố tình ngắt giữa **từng cặp bước**.

#### `STATE-CLEAN-001` — Dọn dẹp khi hủy / ngắt kết nối / hạ gói · **Cao** · Catalog C
- **Trigger**: **BẮT BUỘC** khi có thao tác hủy hợp đồng / ngắt kết nối bot-OA / gỡ tích hợp / hạ gói.
- **Kiểm tra** (danh sách dọn dẹp bắt buộc — xem Catalog C khối MAP-CANCEL): (1) **clear toàn bộ richmenu** của LINE user; (2) **hủy hết schedule**: broadcast / step message / remind (event, lesson, salon, form) / action schedule / schedule send từ chat 1:1 / schedule send từ message error / schedule hiển thị-stop richmenu; (3) **QR code không được chạy action nữa**; (4) mọi background job đang chạy phải dừng. Mọi tính năng khi **version-up** phải test lại luồng hủy hợp đồng.
- **Evidence**: bằng chứng cấu hình + job tự động đã **dừng hẳn** sau khi hủy. _(Nguồn: CL-Func-20)_

#### `STATE-DEP-001` — Hành động phụ thuộc khi gốc thay đổi · **Cao** · Catalog C
- **Trigger**: **BẮT BUỘC** khi sự kiện có hành động phụ thuộc **đã lên lịch** (remind / gửi tin / thanh toán) và gốc có thể bị đổi.
- **Kiểm tra**: đổi thời gian/điều kiện gốc (VD giờ tổ chức event) → **TẤT CẢ** job đã nằm trong queue phải được **tính lại (recalc)** theo giá trị mới, không chạy theo giờ cũ.
- **Evidence**: bằng chứng hành động phụ thuộc chạy theo giá trị **MỚI** sau khi đổi gốc.

### 2.11 Regression & Phạm vi ảnh hưởng

#### `REG-SHARED-001` — Shared code / logic · **Cao** · Catalog D
- **Trigger**: **BẮT BUỘC** với mọi release sửa code dùng chung hoặc fix bug **có thể tồn tại ở chức năng tương tự**. Dấu hiệu: "dùng chung" / "shared" / "component chung" / `共通`.
- **Kiểm tra**: yêu cầu **dev cung cấp danh sách** nơi ảnh hưởng — shared component, bảng DB, batch, API, app, brand (**Lme / Lwaka / Saruwaka / Lgram**) → test lại **từng mục**. Fix bug ở chức năng A → **rà chức năng B có logic tương tự** (cặp Salon / Lesson / Booking Event là điểm lặp lại).
- **Evidence**: danh sách nơi ảnh hưởng (dev cung cấp) + kết quả test từng nơi.

#### `REG-RUN-001` — Dữ liệu / job đang chạy dở khi release · **Cao** · Catalog D
- **Trigger**: **BẮT BUỘC** với mọi release khi hệ thống có job/dữ liệu đang chạy dở.
- **Kiểm tra**: chuẩn bị step gửi tin / đặt lịch / batch / thanh toán pending / sync / action đã lên lịch / migration **đang chạy dở TỪ TRƯỚC release** → sau release phải tiếp tục đúng: **không chạy lại từ đầu** (khách nhận tin trùng), không mất, không dừng sai.
- **Evidence**: bằng chứng job/dữ liệu chạy dở từ trước release vẫn tiếp tục đúng sau release.

#### `REG-SPEC-001` — Spec thay đổi giữa chừng · **Cao**
- **Trigger**: **BẮT BUỘC** với mọi thay đổi spec/requirement xảy ra **SAU** khi đã có test case (kể cả thay đổi nhỏ).
- **Kiểm tra**: rà **TỪNG** TC thuộc phần spec bị đổi, gán 1 trong 4 trạng thái kèm lý do: `[Giữ nguyên]` / `[Cần sửa]` / `[Cần thêm mới]` / `[Hết hiệu lực]`. Case `[Hết hiệu lực]` **đánh dấu, KHÔNG xóa** (giữ vết). Rà lại cột "Áp dụng?" của quan điểm — spec mới có thể **kích hoạt quan điểm chưa từng chọn**.
- **Evidence**: danh sách TC cũ kèm 4 trạng thái + lý do từng dòng.

#### `REG-URL-001` ★ — URL đo lường conversion KHÔNG được đổi · **Trung bình → BẮT BUỘC (nâng Cao)** khi CR chạm màn đăng ký / login / overview / thanh toán / kết nối bot · Catalog D
- **Kiểm tra**: sau release, access và xác nhận từng URL trả đúng màn hình (200, không redirect lạ):
  - `https://step.lme.jp/register/success` · `https://step.lme.jp/admin/home` · `https://step.lme.jp/basic/overview`
  - `https://step.lme.jp/monthly/standard_success` · `/yearly/standard_success` · `/monthly/pro_success` · `/yearly/pro_success`
  - `https://step.lme.jp/admin/bot-add-v2?status=successful`
  - Test thêm biến thể **có/không dấu `/` ở cuối** và **param thừa** → không được treo spinner vô hạn.
- **Evidence**: screenshot/curl status code của toàn bộ URL sau release. _(Nguồn: CL-NonF-12)_

### 2.12 Bảo mật

#### `SEC-001` — Chặn truy cập trái phép PII · **Cao** · Catalog C
- **Trigger**: **BẮT BUỘC** khi chức năng chạm dữ liệu cá nhân khách hàng.
- **Kiểm tra**: đổi ID trong URL / tham số API sang **tổ chức khác** → phải bị chặn. Thử cross-account qua **URL trực tiếp, API, VÀ file EXPORT**.
- **Evidence**: kết quả thử truy cập chéo tài khoản (URL/API/export) đều bị chặn.

#### `SEC-002` — Không lộ token / mật khẩu / thông tin thanh toán · **Cao**
- **Trigger**: **BẮT BUỘC** khi chức năng xử lý credential / token / payment.
- **Kiểm tra**: chủ động tạo lỗi → quét màn lỗi, console DevTools, **server log**, log callback bên ngoài. Danh mục cần quét: token, payment ID, email, LINE user ID, API secret.
- **Evidence**: kết quả quét log + màn lỗi không chứa thông tin nhạy cảm.

#### `SEC-ISO-001` — Cách ly dữ liệu đa phiên · **Cao** · Catalog C
- **Trigger**: **BẮT BUỘC** khi UI tải/hiển thị **nhiều đối tượng dữ liệu đồng thời** (nhiều cuộc trò chuyện, nhiều tab).
- **Kiểm tra**: mở nhiều đối tượng cùng lúc, **tải nhanh liên tiếp** → không dính chéo dữ liệu. Phân biệt 2 tầng: multi-session cùng user (2 tab, app+web) và cross-account (2 user trên cùng trình duyệt).
- **Evidence**: bằng chứng dữ liệu từng đối tượng/phiên độc lập khi tải nhanh liên tiếp.

### 2.13 Hiệu năng & Dữ liệu lớn

#### `PERF-LARGE-001` — Dữ liệu lớn theo ngưỡng THỰC TẾ · **Trung bình** (→ Cao với gửi tin / export / sync / phân tích) · Catalog D
- **Trigger**: mọi chức năng xử lý danh sách / khối lượng dữ liệu. Dấu hiệu spec: `大規模` / `大量` / `一括`.
- **Kiểm tra**: **hỏi/tra số liệu khách hàng lớn nhất hiện tại** cho thực thể liên quan → tạo test data **bằng hoặc lớn hơn** → đo thời gian + đếm kết quả đủ. Không test bằng vài chục bản ghi mẫu. Bug thật: 1.000 staff không lưu được; CSV chỉ export 500 dòng đầu; màn phân tích 3 phút mới mở.
- **Evidence**: số liệu quy mô test data (nguồn: khách lớn nhất) + thời gian chạy + số kết quả.

### 2.14 Hạ tầng & Môi trường

#### `ENV-001` — Fail-safe khi sự cố hạ tầng · **Cao** · Catalog D
- **Trigger**: chức năng có bước validate quan trọng (slot, tồn kho, tiền) chạy qua nhiều server.
- **Kiểm tra**: ngắt 1 server giữa lúc user đang thao tác → bước validate **không được bị bỏ qua** (VD: check slot đã đầy). Không chắc chắn về trạng thái → **chặn an toàn hoặc đưa vào queue retry**.
- **Evidence**: hành vi khi giả lập đứt 1 server giữa thao tác.

#### `ENV-002` — Đồng bộ thời điểm cấu hình hạ tầng · **Trung bình** · Catalog D
- **Trigger**: release có đổi cấu hình hạ tầng (CDN / security rule) **kèm ngoại lệ** cần cấu hình riêng.
- **Kiểm tra**: rule siết chặt và **danh sách ngoại lệ** phải áp dụng **CÙNG THỜI ĐIỂM** — khoảng lệch vài phút sẽ chặn nhầm tiến trình hợp lệ (ảnh không hiện, real-time không cập nhật).
- **Evidence**: kiểm tra ngay sau release, tiến trình phụ thuộc hoạt động bình thường.

#### `ENV-003` ★ — Khác biệt dev / staging / production · **Cao** · Catalog D
- **Trigger**: **BẮT BUỘC** khi tính năng chạm **media/file, URL/domain, job nền, thanh toán**, hoặc khi **thêm server mới**. **Không được đánh × với lý do "staging đã pass"** (RULE-08).
- **Kiểm tra**: rà toàn bộ [Catalog D](catalog-lme.md#catalog-d--khác-biệt-dev--staging--production). Tóm tắt điểm khác:
  - **Job**: dev/staging chạy 1 job all; production tách **3 job độc lập** (callback / broadcast / scenario) + job download media.
  - **Media**: production dùng **server riêng qua `p.lmes.jp`**, ảnh lưu tạm ~1 ngày rồi **sync lên B2** → sau đó access thẳng B2. Media có update **BẮT BUỘC check trên production**.
  - **Domain**: production tách `step.lmes.jp` (admin, link form cũ, popup, conversion cũ) và `s.lmes.jp` (shorten, form/LIFF mới). **Link cũ và mới đều phải access được.** Access media qua link step/shorten phải **redirect sang `p.lmes.jp`**.
  - **Path media**: thừa dấu `//`; file không có phần mở rộng → dev/staging vẫn nhận diện type, production qua B2 tính là file.
  - **Loadbalance**: production có **2 server** → lưu router id, chạy bộ case cơ bản theo **từng router**.
  - **Bill tiền**: dev/staging account test, production **account thật**.
  - **Thêm server mới**: bắt buộc **疎通テスト** (test kết nối tới server đích) + test cấu hình **bảo mật**.
- **Evidence**: bảng đối chiếu môi trường đã tick + screenshot/log lấy **trên production** (hoặc phiếu xác nhận không thể verify + phương án giám sát).

#### `JOB-001` ★ — Job nền / batch gọi API ngoài · **Cao** · Catalog D (+ D2)
- **Trigger**: **BẮT BUỘC** khi tính năng thêm/sửa job nền, hoặc gọi API bên thứ 3 theo lô. × chỉ khi **hoàn toàn không có xử lý nền**.
- **Kiểm tra**: (1) tra tài liệu chính thức **MỚI NHẤT** của bên thứ 3 để lấy rate limit hiện hành (RULE-05); (2) tạo dữ liệu request **lớn và liên tục vượt ngưỡng**; (3) job **không dừng**, có **retry + backoff**, log ghi rõ lần retry; (4) **số bản ghi vào = số xử lý thành công + số vào hàng đợi lỗi** — không bản ghi nào biến mất; (5) job đã có retry sẵn (sync Google của Salon/Lesson/Form) → **verify lại sau mỗi lần tính năng thay đổi**; (6) cân nhắc load test (k6 / Gatling) cho tính năng cải thiện hiệu năng / xử lý hàng loạt.
- **Evidence**: log job (thấy retry + backoff) + bảng đối chiếu số bản ghi vào/ra. _(Nguồn: CLJ01, TC-10, TC-11)_

### 2.15 List & Thao tác hàng loạt

#### `LIST-001` — Search / filter / pagination / drill-down · **Trung bình** · Catalog B
- **Trigger**: **BẮT BUỘC** với mọi màn danh sách có search/filter/pagination.
- **Kiểm tra**: **4 góc** — (1) search bằng **mọi loại tên** hệ thống cho phép đặt: **tên LINE** và **tên quản lý / system name**; exact/partial/no result; (2) filter **vẫn được giữ** khi sort / chuyển trang / đổi tab; (3) pagination đúng với dữ liệu nhiều trang; **xóa hết bản ghi ở trang cuối → tự lùi trang hợp lý**; (4) **click vào số đếm** phải mở đúng danh sách tương ứng với số đó (liên kết `DATA-COUNT-001`).
- **Evidence**: kết quả test 4 góc.

#### `BULK-001` — Phạm vi thao tác hàng loạt sau lọc · **Cao** · Catalog C
- **Trigger**: **BẮT BUỘC** mỗi khi có tổ hợp **bộ lọc + thao tác hàng loạt** (gửi tin / gắn tag / đổi richmenu / đổi cấu hình).
- **Kiểm tra**: áp bộ lọc thu hẹp còn 1 phần nhỏ (đếm số rõ ràng) → thao tác hàng loạt → **đếm lại số đối tượng thực sự bị tác động**. Phải khớp **100%** số đã lọc, tuyệt đối không rơi về toàn bộ đối tượng.
- **Evidence**: số bản ghi THẬT SỰ bị tác động (đếm từ DB/danh sách) khớp 100% số đã lọc.

### 2.16 Media / File

#### `MEDIA-001` — Định dạng file/ảnh upload · **Trung bình** (→ Cao nếu output hiển thị cho khách cuối) · Catalog E
- **Trigger**: **BẮT BUỘC** khi chức năng có upload file/ảnh.
- **Kiểm tra**: bộ file test **đa nguồn thật** (ảnh từ điện thoại, Google Drive, máy scan, **MIME type không chuẩn**, PDF từ iOS vs Android) + file **sát giới hạn chính thức** (LINE/bên thứ 3 — xem Catalog E). **PNG nền trong suốt phải giữ alpha** sau xử lý ở mọi nơi. Bug thật: PDF không hiện trong picker Android do MIME lạ; ảnh 23100px gây lỗi; richmenu >1MB không hiển thị; PNG trong suốt thành nền trắng.
- **Evidence**: kết quả upload bộ file test đa nguồn + screenshot hiển thị thật.

#### `MEDIA-CLEAN-001` ★ — Dọn file trên server (local + B2) · **Trung bình → BẮT BUỘC (nâng Cao)** khi chức năng cho phép **xóa hoặc thay thế** file/ảnh đã upload · Catalog E, D
- **Kiểm tra**: (1) upload ảnh A → lưu URL; (2) đổi sang ảnh B → save; (3) access URL ảnh A **kèm `?v=1`** (bỏ qua cache) → **phải trả 404**. VD `https://p.lmes.jp/ext-media-step/.../xxx.png?v=1`; (4) tương tự với thao tác **Xóa bản ghi**; (5) trên production kiểm **cả link local và link `p.lmes.jp` (B2)** — chờ qua chu kỳ sync nếu file mới upload. Không để **file rác** (rủi ro lộ nội dung).
- **Evidence**: screenshot response **404** khi access link file cũ kèm `?v=x`, trên **cả 2 domain**. _(Nguồn: CL-Func-16)_

#### `MEDIA-IMG-001` ★ — Resize / tỉ lệ / kích thước khuyến nghị · **Trung bình → BẮT BUỘC (nâng Cao)** khi ảnh gửi ra phía LINE user hoặc dùng cho richmenu/imagemap · Catalog E, B
- **Kiểm tra**: (1) upload ảnh 3000×1500 → **tự resize còn 2048×1024** (cạnh lớn ÷ 2048 làm hệ số, nhân sang cạnh còn lại, **giữ nguyên tỉ lệ**); (2) ảnh **> 10.000px → chặn upload**; (3) ảnh vuông/dọc/ngang → rule **fix chiều rộng, giãn chiều cao**; (4) nơi ghi kích thước khuyến nghị (VD `推奨 1,000×500`) → upload đúng size và soi hiển thị ở **TẤT CẢ** chỗ dùng lại (list, detail, preview, chat 1:1, **LINE app thật**); (5) PNG nền trong suốt không chuyển đen/trắng, JPG không mất nền; (6) đối chiếu giới hạn chính thức LINE (richmenu ≤ 1MB) theo **RULE-05**.
- **Evidence**: ảnh gốc + ảnh sau upload **kèm số đo px**; screenshot hiển thị trên LINE app thật. _(Nguồn: CL-Func-6, TC-25)_

### 2.17 Friend info

#### `FRIEND-001` — Friend info end-to-end theo TYPE · **Cao** · Catalog C
- **Trigger**: **BẮT BUỘC** khi chức năng đọc/ghi friend info hoặc dùng nó làm **điều kiện / biến**.
- **Kiểm tra**: friend info là thực thể xuyên suốt LME (form liên kết, action job, remind, biến trong tin, point, CSV/list count). Với **từng type** (text / point / select / date / image / pdf / tên hệ thống / ngày sinh / email / SĐT / 5 trường địa chỉ): đủ vòng đời **tạo → sửa → xóa → thêm lại**, kiểm tác động ở: màn chi tiết, **tổng số đếm** (`total_user_has_value`), action job có chạy, tin nhắn/remind dùng biến có đúng, lịch sử ghi đúng loại thao tác, export/history. Bug thật: xóa value nhưng click vào count vẫn hiện tên friend cũ; add lại bằng action job không update count; action type `年月日` gửi message sai thời điểm; point 上書き chạy sai.
- **Evidence**: bảng kết quả vòng đời từng type + screenshot count/detail/LINE app.
- 👉 9 nơi hiển thị + 11 nơi update: xem Catalog C khối `MAP-FI-*`.

### 2.18 Release & Deploy

#### `DEPLOY-ASSET-001` ★ — Version asset (JS/CSS/font/icon) · **Cao** · Catalog D
- **Trigger**: **BẮT BUỘC** khi release có sửa file JS/CSS/font/icon hoặc đổi cấu trúc dữ liệu mà GUI render. **Cao tuyệt đối** nếu file bị sửa nằm trong luồng **thanh toán / hủy hợp đồng**.
- **Kiểm tra**: (1) mở màn bằng bản cũ để browser cache asset; (2) release bản mới; (3) **chỉ F5 thường** (KHÔNG Ctrl+F5) → chạy lại luồng critical (mua plan, hủy hợp đồng, gửi tin); (4) DevTools > Network: JS/CSS/font trả **200 với query version mới**, không có 404; (5) font **không fallback**, glyph kanji/kana + dấu tiếng Việt đủ (không tofu ロ); (6) icon-font sau merge: load lại nhiều lần, **không lúc có lúc mất**.
- **Evidence**: screenshot DevTools Network (query version + 200) + screenshot màn sau **F5 thường** trên browser còn cache bản cũ.

#### `DEPLOY-LIVE-001` ★ — Release KHÔNG lock maintain · **Cao** · Catalog D
- **Trigger**: **BẮT BUỘC** với mọi release lên production **không bật maintain**, đặc biệt khi đổi **payload API / field form / cấu trúc request**.
- **Kiểm tra**: (1) mở sẵn màn hình (VD form phía LINE user) **TRƯỚC** khi release; (2) release code mới; (3) **không reload**, bấm submit; (4) xác nhận đầy đủ: lưu result, ghi Google Spread, chạy action form; (5) lặp lại với màn có payload đổi cấu trúc → phải **báo lỗi rõ ràng, không exception 500, không lưu nửa vời**.
- **Evidence**: screenshot màn hình cũ + kết quả sau submit (bản ghi DB / dòng Google Spread / tin LINE) + log request. _(Nguồn: CL-Func-18. Khác REG-RUN-001: đây là **client cũ gọi server mới**.)_

#### `COMPAT-LEGACY-001` ★ — Dữ liệu / link / định dạng đời cũ chạy song song · **Cao** · Catalog C, D
- **Trigger**: **BẮT BUỘC** khi tính năng chạm template, form, remind, richmenu, google spread, hoặc **bất kỳ đối tượng nào đã từng version-up**. **Không được đánh × chỉ vì "dữ liệu mới chạy ổn"** (RULE-09).
- **Kiểm tra** — test song song **từng cặp**, mỗi cặp 1 bộ case:
  - Template **không có group** ⇄ template **có group template**
  - Form cũ (`step3.lmes.jp`) ⇄ form mới (`s.lmes.jp`) — **link cũ vẫn phải access được**
  - Remind cũ ⇄ remind mới (salon / lesson / form)
  - Google Spread **header cũ** (1 cột tên người trả lời) ⇄ **header mới** (Tên LINE + `システム表示名`)
  - Copy richmenu / copy template / copy button: bản mới ⇄ bản cũ
  - Bản ghi tạo **trước** migration ⇄ **sau** migration: mở → sửa → **lưu lại**
- **Evidence**: screenshot kết quả của **CẢ hai nhánh** cũ/mới (tối thiểu 1 bản ghi tạo trước version-up + 1 bản ghi tạo mới). _(Nguồn: CL-Func-23)_

---

## 3. Phụ lục nội bộ — Error scenarios payment gateway

> ⚠️ **Bổ sung nội bộ của team — KHÔNG có trong sheet gốc.** Giữ lại khi sync sheet. Phái sinh từ quy tắc **generic-fix detection**: khi cách fix là **generic error handler** ("set error message" / "return error" / "handle exception" tại payment controller) → bắt buộc cover **≥ 4 error type** dưới đây + **1 unknown-error fallback**. Dùng test card của Univapay/Stripe sandbox để trigger. Gắn với `PAY-STATE-001`.

- [ ] **Card declined** (`card_declined`)
- [ ] **Insufficient funds** (`insufficient_funds`)
- [ ] **Expired card** (`expired_card`)
- [ ] **3D Secure fail** (`three_ds_failed`)
- [ ] **Amount exceeded max** (`amount_exceeded` / `amount_too_large`)
- [ ] **Amount below min** (`amount_too_small`)
- [ ] **Network timeout / API 5xx** (gateway down)
- [ ] **Unknown error code** — mock gateway trả code chưa handle riêng → **verify fallback generic message hiển thị**
- [ ] **Duplicate transaction** (cùng `order_id` submit 2 lần) → liên kết `CONC-001`, `INTG-HOOK-001`
- [ ] **Account suspended / 不正利用検知**

**Verify chung**: mỗi error type → frontend hiển thị **message business-friendly** (không phải raw API error), **KHÔNG silent fail** (không tự đóng màn / không quay về talklist im lặng), có **UX recovery** (nút quay lại / thử lại).

---

## 4. Quan điểm CHƯA đủ bằng chứng — chưa đưa vào quy trình

> Sheet 10. Bằng chứng duy nhất là ticket **New / đợi khách xác nhận** → theo **RULE-11** chưa được dùng. **KHÔNG** dùng các mục này để flag BLOCKER/MAJOR khi review; chỉ được nêu ở mục "gợi ý / NIT".

| Mã | Tính năng | Quan điểm đề xuất | Ticket |
|---|---|---|---|
| FORM-01 | Form | Sửa nội dung từ màn "lịch sử gửi" không được làm đổi ngược bản ghi lịch sử gốc | #35779 |
| CHAT-01 | Chat 1:1 | Tin loại đặc biệt (sticker, file, location) phải đồng bộ đầy đủ từ LINE OA lên tool | #34536 |
| ADM-01 | Admin | Bộ lọc/tìm kiếm phải đúng ngay lần đầu thao tác (không cần bấm lại lần 2) | #35793 |
| ADM-03 | Admin | Export CSV giá trị enum phải khớp mapping UI, test **từng giá trị riêng biệt** | #27141 |
| ADM-04 | Admin | Bộ lọc theo tháng/năm ở màn thống kê phải đúng qua ranh giới đầu/cuối tháng | #26876 |
| TPL-01 | Template | Giá trị tĩnh đã cấu hình sẵn (VD location) phải gửi đúng như đã lưu, không bị ghi đè bởi giá trị runtime | #32364 |
