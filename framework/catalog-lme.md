# Catalog LME — Tầng 2 (tri thức miền)

> **Nguồn**: [Bảng quan điểm test — HỢP NHẤT ELME v1.0](https://docs.google.com/spreadsheets/d/1IijLnq0gLZDFxOMWOYxXafz1Wnzv3W0g/edit?gid=1184713662#gid=1184713662) — sheet 2→6. Ngày fetch: 2026-07-13.
>
> Tầng 2 trả lời: **"ở đâu trong LME, nhập dữ liệu gì"**. Đây là **tri thức miền KHÔNG suy ra được từ đặc tả** — bỏ qua tầng này là chỗ bug lọt.
>
> Tầng 1 (quan điểm + 12 RULE): [checklist-lme.md](checklist-lme.md). Mỗi dòng ở đây ghi **Quan điểm liên kết** để tra ngược.

**Cách dùng**: tick ◯ một quan điểm ở tầng 1 → mở **đúng catalog** ghi ở dòng quan điểm đó → lấy dữ liệu và vị trí cụ thể để viết TC.

| Catalog | Nội dung | Khi nào mở |
|---|---|---|
| [A](#catalog-a--ma-trận-dữ-liệu-nhập-theo-kiểu-input) | 21 kiểu input × Normal/Abnormal/Boundary | Màn hình có ô nhập liệu |
| [B](#catalog-b--checklist-giao-diện-theo-thành-phần) | 15 thành phần giao diện | Màn hình có UI |
| [C](#catalog-c--bản-đồ-tính-năng-dùng-chung) | Bản đồ 21 đường gửi tin, friend info, tag, spread, sort, plan, bill, hủy hợp đồng, LIFF, phân quyền | Quan điểm nhóm MSG / FRIEND / DATA / PAY |
| [D](#catalog-d--khác-biệt-dev--staging--production) | Khác biệt môi trường (RULE-08) | Trước khi kết luận "đã test xong" |
| [D2](#catalog-d2--checklist-tầng-job-nền) | Checklist tầng job nền | Tính năng có xử lý nền |
| [E](#catalog-e--giới-hạn-và-ma-trận-media) | Giới hạn media + ma trận tính năng × thao tác | Tính năng chạm file/ảnh |

---

## Catalog A — Ma trận dữ liệu nhập theo kiểu input

> Ba cột case tương ứng đúng **pattern tối thiểu của RULE-01**. Màn hình có kiểu input nào thì **bê nguyên ba cột đó thành test case**.
> Dùng kèm: `FUNC-002` / `FUNC-003` / `FUNC-004`, `UI-INPUT-001`, `DATA-TEXT-001`, `OUT-EXPORT-001`, `MEDIA-001`.

### `DI-01` Text (1 dòng)
- **Normal**: latinh thường; tiếng Nhật **full-width và half-width**; ký tự đặc biệt / symbol / emoji; paste bằng **Ctrl+V và bằng chuột phải** (Win + Mac).
- **Abnormal**: bỏ trống khi bắt buộc → báo lỗi, chặn lưu. Bỏ trống khi KHÔNG bắt buộc → lưu được; **kiểm DB lưu NULL hay chuỗi rỗng** (phải thống nhất toàn hệ thống). Chỉ nhập space → sau trim thành rỗng, xử lý như bỏ trống.
- **Boundary**: min−1 / min / max / max+1 ký tự. **Đếm ký tự phải đúng** cho: latinh, full-width JP, half-width JP, symbol, space. Nhập đúng max → **không vỡ layout**.
- **Quan điểm**: FUNC-002, FUNC-003, FUNC-004, UI-INPUT-001, DATA-TEXT-001

### `DI-02` Textarea (nhiều dòng)
- **Normal**: có/không ký tự xuống dòng; nhiều xuống dòng liên tiếp; tiếng Nhật có xuống dòng; paste text nhiều dòng.
- **Abnormal**: bỏ trống (như DI-01). Chỉ có ký tự xuống dòng. Xuống dòng ở đầu và cuối → **có bị trim không, spec quy định thế nào**.
- **Boundary**: nhập đúng max → scroll hoặc auto-resize. **Ký tự xuống dòng có được tính vào maxlength không** (phải khớp spec).
- **Quan điểm**: FUNC-002, FUNC-004, UI-INPUT-001

### `DI-03` Rich text (CKEditor / TinyMCE / Quill)
- **Normal**: định dạng (font, size, màu chữ, màu nền, bold/italic/underline/strikethrough, sup/sub, heading); căn lề (left/right/center/justify, tăng giảm lề); action (cut, copy, paste, paste special, undo, redo, find & replace, select all, xuống dòng, trích dẫn).
- **Abnormal**: bỏ trống nhưng editor tự sinh **thẻ rỗng** (`<p><br></p>`) → hệ thống phải coi là rỗng, **không lưu HTML rác**. Paste nội dung có định dạng từ **Word / Google Docs / trang web** → không mang theo style lạ, **không chèn script**.
- **Boundary**: maxlength tính theo **ký tự hiển thị hay độ dài HTML**? Phải xác nhận với spec — nguồn sai lệch thường gặp.
- **Quan điểm**: FUNC-003, FUNC-004, SEC-002, DATA-TEXT-001

### `DI-04` Số
- **Normal**: số dương; **số 0**; số thập phân đúng số chữ số sau dấu phẩy theo spec.
- **Abnormal**: nhập chữ / ký tự đặc biệt / **số Nhật** (không phải latinh). Số âm khi spec chỉ cho dương. **Số 0 ở đầu** (`0123`) → không được mất nếu là mã, phải chuẩn hóa nếu là số lượng. Dấu phân cách nghìn khi paste (`1,000`).
- **Boundary**: min−1 / min / max / max+1. **Số 0 phải test riêng** — bị nhầm với "bỏ trống" rất thường xuyên. Vượt giới hạn kiểu dữ liệu (cột 1 byte → **127/128**).
- **Quan điểm**: FUNC-003, FUNC-004, DATA-COUNT-001

### `DI-05` URL
> LME **lưu và phát lại URL cho LINE user** nên phải giữ nguyên vẹn.
- **Normal**: URL chứa **tiếng Nhật** (phải tự percent-encoding); chứa `@ # ~ ? & - [ ] /`; URL Google Map có tọa độ; nhiều query param; **placeholder động của LME** (`[FRIEND_INFO_xxx]`).
- **Abnormal**: chuỗi không phải URL; thiếu scheme (`https://`); **`javascript:` → phải bị chặn**; URL có khoảng trắng ở giữa.
- **Boundary**: URL dài sát giới hạn cột DB và giới hạn của LINE. **Có dấu `/` ở cuối và không có** → cả hai đều phải hoạt động.
- **Quan điểm**: FUNC-003, SEC-002, REG-URL-001, LIFF-ENTRY-001

### `DI-06` Email
- **Normal**: định dạng chuẩn; domain nhiều cấp (`@yahoo.ne.jp`); dấu `+` trong phần local.
- **Abnormal**: thiếu `@` / thiếu domain / 2 dấu `@` / có khoảng trắng. Email tiếng Nhật (không chấp nhận nếu spec không nói).
- **Boundary**: độ dài sát giới hạn cột DB. Sau khi lưu → **phải gửi mail thật để verify** (`NOTI-MAIL-001`).
- **Quan điểm**: FUNC-003, NOTI-MAIL-001

### `DI-07` Số điện thoại Nhật
> 10 hoặc 11 số bắt đầu bằng `0`; hoặc bắt đầu bằng `+81`.
- **Normal**: 10 số bắt đầu `0`; 11 số bắt đầu `0`; 11-12 số bắt đầu `+81`; có khoảng trắng 2 đầu → tự trim.
- **Abnormal**: 10 số không bắt đầu `0`; 11 số không bắt đầu `0`/`+81`; 12 số không bắt đầu `+81`; **số Nhật** (không latinh); có dấu gạch ngang; khoảng trắng ở giữa; có ký tự chữ.
- **Boundary**: 9 số (dưới min); 13 số (trên max).
- **Quan điểm**: FUNC-003, FUNC-004, SEC-001

### `DI-08` Ngày / Date picker
- **Normal**: chọn ngày trong tháng hiện tại. Next/back tháng → ngày khớp đúng **thứ trong tuần**. Ngày của tháng trước/sau hiển thị chờm sang lịch tháng hiện tại (30, 31, 1, 2) → **xác nhận có được phép chọn không**.
- **Abnormal**: nhập tay ngày không tồn tại (**31/02**); nhập ngày quá khứ khi spec chỉ cho tương lai; định dạng ngày sai.
- **Boundary**: **29/02 năm nhuận và năm không nhuận**; ngày cuối tháng của tháng 30 và 31 ngày; qua ranh giới năm (**31/12 → 01/01**); năm quá khứ và tương lai (**so sánh ngày bằng chuỗi sẽ sai khi khác năm**).
- **Quan điểm**: FUNC-DATE-001, DATA-COUNT-001

### `DI-09` Giờ / Time
- **Normal**: giờ trong ngày làm việc.
- **Abnormal**: giờ kết thúc **trước** giờ bắt đầu; nhập tay `25:00`.
- **Boundary**: **`00:00` và `24:00`** — hệ thống quy đổi thế nào, phải thống nhất. **Ca qua ngày** (23:00 → 01:00 hôm sau). Biên **23:59 → 00:01**.
- **Quan điểm**: FUNC-DATE-001

### `DI-10` Khoảng ngày (range)
- **Normal**: khoảng trong cùng tháng; xuyên tuần / xuyên tháng / **xuyên năm**.
- **Abnormal**: ngày kết thúc trước ngày bắt đầu; chỉ nhập 1 trong 2 đầu.
- **Boundary**: bắt đầu = kết thúc (1 ngày); khoảng dài nhất spec cho phép, và dài hơn 1 đơn vị.
- **Quan điểm**: FUNC-DATE-001, FUNC-004

### `DI-11` Checkbox
- **Normal**: danh sách hiển thị **đủ và đúng thứ tự** theo spec. Tạo mới: giá trị check mặc định; chọn từng giá trị; chọn nhiều; **chọn tất cả** — mỗi lần **verify DB**. Edit: mặc định tick đúng lựa chọn trước đó; chuyển check ↔ uncheck. Check rồi uncheck qua lại → DB lưu đúng trạng thái **lần cuối**.
- **Abnormal**: không chọn gì khi spec bắt buộc tối thiểu N mục → báo lỗi.
- **Boundary**: chọn đúng số lượng tối thiểu, và ít hơn 1. Chọn tất cả khi danh sách dài nhất.
- **Quan điểm**: FUNC-002, FUNC-MULTI-001, UI-FIELD-001

### `DI-12` Checkbox "Chọn tất cả"
> **Nguồn lỗi thường xuyên khi kết hợp phân trang.**
- **Normal**: check-all → mọi mục trên trang được chọn (kể cả chính ô check-all). Check all → uncheck all → mọi mục bỏ chọn. Check all → bỏ chọn vài mục → **ô check-all tự bỏ chọn**. Chọn tay đủ hết mục → ô check-all **tự động được chọn**.
- **Abnormal**: thao tác check-all ở **trang 2, 3** → phạm vi ảnh hưởng là **trang hiện tại hay toàn bộ kết quả lọc**? Phải khớp spec **và khớp với thao tác hàng loạt sau đó** (`BULK-001`).
- **Boundary**: danh sách rỗng → ô check-all phải **disable**. Danh sách chỉ có 1 mục.
- **Quan điểm**: BULK-001, LIST-001, FUNC-MULTI-001

### `DI-13` Radio button
- **Normal**: danh sách đủ và đúng thứ tự. Tạo mới: giá trị mặc định theo spec. Edit: hiển thị giá trị đã chọn trước. Chọn giá trị đầu / bất kỳ / cuối → **verify DB**. Chuyển đổi qua lại → lưu đúng lựa chọn cuối.
- **Abnormal**: không chọn khi bắt buộc → báo lỗi. **Hai radio khác nhau bị đặt trùng `value`** → chọn cái này lại tick cái kia.
- **Boundary**: danh sách chỉ có 1 lựa chọn.
- **Quan điểm**: FUNC-002, UI-FIELD-001

### `DI-14` Dropdown (chọn 1)
- **Normal**: hiển thị đủ và đúng thứ tự; giá trị mặc định đúng spec; chọn giá trị đầu/bất kỳ/cuối; chọn rồi đổi sang giá trị khác; **hành vi tap/click khi đã có giá trị mặc định** (dễ bị sót).
- **Abnormal**: không chọn khi bắt buộc → báo lỗi. Giá trị nạp từ DB/màn khác: **thêm/sửa/xóa giá trị ở nguồn** → dropdown phải cập nhật theo. **Giá trị nguồn bị xóa trong khi bản ghi đang tham chiếu nó.**
- **Boundary**: danh sách rỗng; giá trị dài nhất → không vỡ layout; danh sách dài → có scroll, xem được hết.
- **Quan điểm**: FUNC-002, DATA-REF-001, UI-FIELD-001

### `DI-15` Select box (chọn nhiều)
- **Normal**: như DI-14, thêm: chọn 2 giá trị; chọn >2; chọn tất cả; chọn rồi bỏ chọn qua lại.
- **Abnormal**: không chọn khi spec bắt buộc tối thiểu N mục. **Giá trị nguồn bị xóa/đổi tên trong lúc đang được chọn.**
- **Boundary**: chọn đúng số lượng tối đa cho phép, và nhiều hơn 1.
- **Quan điểm**: FUNC-MULTI-001, DATA-REF-001

### `DI-16` Upload ảnh
> Dùng cho template, richmenu, imagemap, friend info, QR.
- **Normal**: upload bằng **nút và kéo-thả**; định dạng theo spec (jpg, jpeg, png, gif, tiff); tỉ lệ vuông/dọc/ngang; **upload ảnh A rồi thay bằng ảnh B**; tên file tiếng Nhật hoặc có khoảng trắng; ảnh đúng **kích thước khuyến nghị** ghi trên GUI (`推奨 1,000×500`) → kiểm hiển thị ở **MỌI nơi dùng lại**, không co giãn; **PNG nền trong suốt** → nền không chuyển đen/trắng.
- **Abnormal**: định dạng ngoài spec; **file đổi đuôi giả** (`.exe` → `.png`); **file không có phần mở rộng** (production qua B2 nhận diện MIME khác staging); **double click nút upload**; không upload khi bắt buộc.
- **Boundary**: dưới min / trên max (size + dimension). **Cạnh > 2048px → tự resize giữ tỉ lệ** (cạnh lớn ÷ 2048 làm hệ số). **> 10.000px → chặn upload.** **Richmenu: ảnh vượt 1MB → LINE không hiển thị.**
- **Quan điểm**: MEDIA-001, MEDIA-IMG-001, MEDIA-CLEAN-001, ENV-003

### `DI-17` Upload video / audio / PDF
- **Normal**: định dạng theo spec (video mp4/avi/wmv; audio m4a/mp3/wav; pdf). Upload rồi mở xem lại — **preview trước khi save và sau khi save phải giống nhau**. Video có thumbnail → thumbnail sinh đúng.
- **Abnormal**: định dạng ngoài spec; file hỏng; **MIME khác nhau giữa thiết bị** (PDF từ iOS vs Android); **xóa bản ghi → file vật lý phải bị xóa trên cả server local và B2**.
- **Boundary**: giới hạn theo surface — xem [Catalog E khối E1](#khối-e1--giới-hạn-dung-lượng-theo-nơi-sử-dụng). Test tại đúng ngưỡng và vượt ngưỡng 1 đơn vị.
- **Quan điểm**: MEDIA-001, MEDIA-CLEAN-001, SYNC-APP-001

### `DI-18` Import CSV
- **Normal**: upload bằng nút và kéo-thả; import 1 dòng; import nhiều dòng; dữ liệu tiếng Nhật không lỗi font; encoding **UTF-8 và Shift-JIS**; sau import dữ liệu đủ và lưu DB đúng.
- **Abnormal**: sai định dạng file (docx, pdf, zip); **sai cấu trúc** (không header / sai tên cột / thiếu cột / thiếu dữ liệu cột bắt buộc); file rỗng (chỉ header); **vi phạm validate** (quá maxlength, trùng ở cột unique, sai kiểu dữ liệu, **số có 0 ở đầu bị mất**, ô chứa dấu phẩy hoặc ký tự đặc biệt); **nhiều người import cùng lúc**; double click nút upload.
- **Boundary**: số dòng đúng giới hạn spec và vượt 1 dòng; file đúng max size và vượt max size.
- **Quan điểm**: FUNC-002, FUNC-004, CONC-001, DATA-TEXT-001

### `DI-19` Export CSV / Google Spreadsheet
- **Normal**: **từng cột** trong file khớp giá trị trên màn hình — đặc biệt **cột enum/phân loại, test từng giá trị**. Định dạng ngày-giờ đúng spec (**có giờ nếu spec ghi có giờ**). Ô chứa dấu phẩy → bọc trong `"`. Tiêu đề cột **có xuống dòng** vẫn đúng. Mở được bằng Excel với **cả UTF-8 và Shift-JIS**.
- **Abnormal**: tên file chứa ký tự đặc biệt hoặc tiếng Nhật; **giá trị 0 vs bỏ trống phải phân biệt được**; SĐT / mã số **không được mất số 0 ở đầu**; spreadsheet **mất quyền truy cập giữa chừng**.
- **Boundary**: tên file dài sát **255 byte**; export vượt ngưỡng nghiệp vụ (form answer **> 500 bản ghi**); export ở **quy mô dữ liệu lớn nhất của khách hàng thật**.
- **Quan điểm**: OUT-EXPORT-001, INTG-SHEET-001, PERF-LARGE-001

### `DI-20` Ô tìm kiếm
- **Normal**: từ khóa latinh và tiếng Nhật (full-width, half-width); tìm đúng một phần chuỗi; kết quả đúng khi có **phân trang / loadmore**.
- **Abnormal**: từ khóa chỉ có space; **ký tự đặc biệt dùng trong SQL hoặc regex** (`%`, `_`, `'`, `\`); **bấm tìm liên tiếp nhiều lần** → kết quả cuối khớp từ khóa **cuối cùng**, không phải lần bấm trước.
- **Boundary**: từ khóa dài sát maxlength; không có kết quả → **hiển thị trạng thái rỗng, không phải màn trắng**.
- **Quan điểm**: LIST-001, CONC-003, DATA-TEXT-001, SEC-002

### `DI-21` Toggle / Switch
- **Normal**: bật rồi tắt, **kiểm DB sau mỗi lần**; trạng thái mặc định đúng spec.
- **Abnormal**: **bật tắt liên tiếp thật nhanh** → chỉ ghi nhận trạng thái cuối, không gửi trùng request. **Tắt một thiết lập đang được job nền sử dụng → job phải dừng theo.**
- **Boundary**: không áp dụng (chỉ có 2 trạng thái) — **ghi lý do này vào Ghi chú** (RULE-01).
- **Quan điểm**: CONC-001, STATE-DEP-001

---

## Catalog B — Checklist giao diện theo thành phần

> Tra theo thành phần **có mặt trên màn hình đang test**. Dùng kèm: `UI-001`…`UI-004`, `UI-FIELD-001`, `UI-INPUT-001`, `LIST-001`, `CONC-003`, `DEPLOY-ASSET-001`.

| ID | Thành phần | Thuộc tính & hành vi phải kiểm | Lỗi hay gặp | Quan điểm |
|---|---|---|---|---|
| **UIC-01** | Text | Đúng nội dung; font (kiểm 1 màn đại diện); font-size; font-weight; màu; vị trí; gạch chân nếu có. Text dài 2 dòng: **điểm ngắt dòng đúng, không cắt giữa từ tiếng Nhật**. | Text 2 dòng xuống dòng sai vị trí. Font fallback về font hệ thống sau release. | UI-001, DEPLOY-ASSET-001 |
| **UIC-02** | Button | Vị trí; nội dung chữ; chữ căn giữa; kích thước; bo góc; màu nền/viền; đổ bóng; độ mờ. **Hiệu ứng hover.** **Con trỏ đổi thành bàn tay** khi rê vào. Trạng thái **disable**: màu phân biệt rõ, không click được. | Quên hiệu ứng hover. **Nút disable vẫn bấm được bằng Enter.** | UI-001, UI-003 |
| **UIC-03** | Hyperlink | **Mặc định mở tab mới** nếu khách không yêu cầu khác. Điểm đến đúng. Toàn bộ hyperlink trong design đã hiển thị đủ. | Link mở đè lên tab hiện tại → **mất dữ liệu đang nhập**. | UI-001, REG-URL-001 |
| **UIC-04** | Ô nhập liệu | Placeholder đủ/đúng. Viền lúc chưa focus và lúc focus. **Tự trim space đầu/cuối.** Nhập đúng maxlength không vỡ layout. Textarea: xuống dòng đúng, tự giãn hoặc có scroll. **Paste bằng chuột phải phải kích hoạt validate giống paste bằng phím tắt** (Windows **và** Mac). | Paste chuột phải xong nút Lưu vẫn disable (JS chỉ nghe keyboard event). Space thừa lưu vào DB → tìm kiếm không ra. | UI-INPUT-001, FUNC-003 |
| **UIC-05** | Modal / Dialog | Vị trí; kích thước; bo góc; nền; đổ bóng; sidebar. **Đóng bằng X / Esc / click ra ngoài** — hành vi phải khớp spec. Nội dung dialog xác nhận khớp spec. **Dữ liệu đang nhập dở khi đóng modal: giữ hay xóa, phải nhất quán.** | Đóng modal bằng Esc **làm mất dữ liệu mà không hỏi**. | UI-001, FUNC-DRAFT-001 |
| **UIC-06** | Box / Card | Kích thước; bo góc; màu nền và viền; đổ bóng; độ mờ. | — | UI-001 |
| **UIC-07** | Tooltip | Icon; kích thước; màu; nội dung; vị trí; độ mờ. **Tooltip ở hàng đầu bảng không bị bảng che.** **Tooltip dài hiển thị hết chữ.** Màn có phân trang: **tooltip vẫn hiện sau khi sang trang khác**. **Không có khoảng hở giữa tooltip và nút** khiến không click được. | Tooltip đầu bảng bị che. Tooltip biến mất sau next page. Khoảng hở tooltip–nút chặn click. | UI-001, REG-SHARED-001 |
| **UIC-08** | Bảng / Danh sách | Hiển thị đủ cột theo design. Dữ liệu dài nhất không vỡ layout. Sắp xếp theo cột đúng. **Không có giới hạn ngầm về số bản ghi hiển thị.** | Modal chỉ hiển thị **25 bản ghi** do giới hạn ngầm. Vỡ layout khi khách có hàng trăm trang. | LIST-001, PERF-LARGE-001 |
| **UIC-09** | Phân trang & Scroll | Nhiều bản ghi: **cố định header bảng**, chỉ scroll vùng dữ liệu. **Chuyển trang → tự động scroll lên đầu trang.** Loadmore/infinite scroll: vừa load vừa scroll không trùng, không nhảy vị trí. | Sang trang mới nhưng vẫn ở giữa trang. Loadmore khi mạng chậm gây **ghi trùng bản ghi**. | LIST-001, CONC-003 |
| **UIC-10** | Tab | **Chuyển qua lại giữa các tab rồi Save → dữ liệu các tab không đổi/mất.** Chuyển tab nhanh khi API tab trước chưa trả về → hiển thị dữ liệu của **tab đang chọn**. | Hiện dữ liệu của **tab vừa rời khỏi**. | CONC-003, FUNC-SEQ-001 |
| **UIC-11** | Loading / Rỗng / Lỗi | Loading có chỉ báo rõ, **không màn trắng**. Danh sách rỗng có thông báo. Lỗi hiển thị thông báo cụ thể, **không báo thành công giả**. | Xử lý thất bại nhưng **UI báo thành công**. Màn trắng khi API chậm. | UI-003, OUT-TRUTH-001 |
| **UIC-12** | Layout & khoảng cách | Các khối thẳng hàng. Padding/margin đúng design. | — | UI-001 |
| **UIC-13** | Độ phân giải & Trình duyệt | **Bắt buộc kiểm ở 1366×768** (độ phân giải thấp nhất được hỗ trợ). Chrome và Safari; máy **Windows và Mac**. App: **Android và iOS**. **LIFF trong app LINE.** | Bố cục chỉ đúng ở 1920, **vỡ ở 1366**. | UI-001, UI-002, SYNC-APP-001 |
| **UIC-14** | Bàn phím & Focus | Thứ tự **Tab** đi qua các trường theo trình tự đọc. **Enter trong form submit đúng nút mặc định.** Esc đóng modal. | **Enter submit nhầm nút Xóa.** | UI-004 |
| **UIC-15** | Icon / Font / Asset | Sau merge, icon-font và thư viện UI dùng chung hiển thị đủ **qua nhiều lần load**. File font tải thành công, **không 404**. Glyph đủ cho **kanji, kana và dấu tiếng Việt** (không hiện ô vuông). | Xung đột version thư viện icon → **mất icon lúc có lúc không**. Font 404 trên production (media server riêng). | DEPLOY-ASSET-001, ENV-003 |

---

## Catalog C — Bản đồ tính năng dùng chung

> **Tri thức miền không suy ra được từ đặc tả**: mọi nơi một đối tượng được **gửi / hiển thị / cập nhật**.
> Khi tick ◯ một quan điểm nhóm **MSG / FRIEND / DATA / PAY** → lọc đúng khối dưới đây và **duyệt hết**.

### C.1 Send message — 21 đường gửi tin

| ID | Kênh | Điểm phát sinh | Điều phải xác nhận | Quan điểm |
|---|---|---|---|---|
| MAP-SEND-01 | Job | **Broadcast** | Gửi đúng đối tượng theo filter; đúng thứ tự; không trùng; không gửi nhầm sang tài khoản khác. | MSG-001, MSG-002 |
| MAP-SEND-02 | Job | **Scenario (step message)** | Đúng thứ tự bước; đúng thời điểm; send test từng bước. | MSG-002 |
| MAP-SEND-03 | Job | **Event remind — loại cũ** | Cả hai loại remind cùng tồn tại, **phải test cả hai**. | MSG-002, COMPAT-LEGACY-001 |
| MAP-SEND-04 | Job | **Event remind — loại mới** (salon, lesson, form) | Như trên. | MSG-002, COMPAT-LEGACY-001 |
| MAP-SEND-05 | Job | **Action khi có callback**: kết bạn thường, kết bạn qua landing | **Thứ tự chạy: action kết bạn trước, action QR sau.** | MSG-001, STATE-DEP-001 |
| MAP-SEND-06 | Job | Action: **auto reply** | | MSG-001 |
| MAP-SEND-07 | Job | **Delay message** của template (random message) | | MSG-002 |
| MAP-SEND-08 | Job | **Send schedule cho message lỗi** (resend message error) | Lưu đúng lỗi; resend thành công. | MSG-002, STATE-001 |
| MAP-SEND-09 | Job | **Send schedule từ chat 1:1** (user đặt lịch gửi) | | MSG-002 |
| MAP-SEND-10 | Job | **Action schedule** | | MSG-002, STATE-DEP-001 |
| MAP-SEND-11 | Job | **Postback**: button, rich menu, image map, video | | MSG-001 |
| MAP-SEND-12 | Job | **Action từ tính năng khác**: form, booking calendar, booking event, tag, friend info, item, URL, conversion | **Mỗi tính năng là một đường gửi riêng.** | MSG-001, STATE-DEP-001 |
| MAP-SEND-13 | Web | **Chat 1:1** | | MSG-004 |
| MAP-SEND-14 | Web | **Add tag** | | MSG-001 |
| MAP-SEND-15 | Web | **Send test**: màn template, broadcast, scenario, remind | **Preview phải khớp tin nhận thật trên LINE.** | OUT-PREVIEW-001, MSG-004 |
| MAP-SEND-16 | Web | **Reply ở màn talklist** | | MSG-004 |
| MAP-SEND-17 | Web | **Remind kiểu gửi ngay** | | MSG-002 |
| MAP-SEND-18 | Web | **Action text độc lập** của: salon, lesson, kết bạn, QR, form | | MSG-001 |
| MAP-SEND-19 | App admin | Chat 1:1; add tag; **duyệt/từ chối booking salon**; **duyệt/từ chối booking lesson** | | SYNC-APP-001, MSG-004 |
| MAP-SEND-20 | LINE user | **Friend đã block bot / bot bị block** | **KHÔNG gửi message, KHÔNG chạy action, KHÔNG gửi remind, không làm sai số đếm.** | MSG-003 |
| MAP-SEND-21 | Chung | **Nội dung tin nhắn** | Thay thế biến động (tên, friend info) đúng. **Profile người gửi** đúng. Cập nhật `last_message` + `last_time_message` đúng logic. **Trigger hiển thị đủ trên chat 1:1 của cả web và app.** Format ngày-giờ và **dấu cách phải là ký tự Nhật** theo design. **Format khi gửi từ web / send test / job send phải giống hệt nhau.** | MSG-004, OUT-PREVIEW-001, DATA-TEXT-001 |

### C.2 Friend info

| ID | Kênh | Điểm phát sinh | Ghi chú | Quan điểm |
|---|---|---|---|---|
| MAP-FI-01 | — | **Ba loại folder** | Folder **chưa phân loại**; **2 folder mặc định**; folder do **admin tạo**. Mọi tính năng chạm friend info phải phủ **đủ ba loại**. | FRIEND-001 |
| MAP-FI-02 | — | **Ma trận kiểu dữ liệu** | Tên hệ thống; ngày sinh; email; SĐT; **5 trường địa chỉ**; kiểu do user tạo: text, **point**, select, date, image, pdf. | FRIEND-001, DI-16, DI-17 |
| MAP-FI-03 | Web — hiển thị | **9 nơi**: quản lý friend info; danh sách friend theo info; chat 1:1 right bar; My page tab `基本情報`; export CSV; phân tích cross (trục `友だち情報`); modal action; modal filter | **Sửa một trường phải kiểm cả chín.** | FRIEND-001, DATA-001 |
| MAP-FI-04 | LINE user — hiển thị | Booking event; booking lesson; booking salon; mua item; trả lời form | | FRIEND-001 |
| MAP-FI-05 | App — hiển thị | Màn My page | | SYNC-APP-001 |
| MAP-FI-06 | Web — cập nhật | Chat 1:1 right bar; My page; **import CSV**; **multi action** | | FRIEND-001, DATA-001 |
| MAP-FI-07 | Job — cập nhật | **QR landing có set import param** → cập nhật sau khi kết bạn | | FRIEND-001, STATE-DEP-001 |
| MAP-FI-08 | LINE user — cập nhật | Form nhập thông tin do admin tạo trong: booking event, lesson, salon, item, form | | FRIEND-001 |
| MAP-FI-09 | App — cập nhật | Màn My page | | SYNC-APP-001 |
| MAP-FI-10 | Chung | **Chèn mã friend info + thay thế dữ liệu động** | Trong: modal **multi action** (action text), **template text**, **remind**. Mỗi trường hợp kiểm **ba nơi**: phía LINE user / chat 1:1 web / chat 1:1 app. | FRIEND-001, MSG-004, SYNC-APP-001 |

### C.3 Tag

| ID | Kênh | Điểm phát sinh | Quan điểm |
|---|---|---|---|
| MAP-TAG-01 | Web — hiển thị | Quản lý tag; chat 1:1 right bar; My page tab `タグ`; export CSV; **form (item gắn tag: radio, droplist, checkbox)**; cross analysis; modal multi action; modal filter | DATA-001, DATA-REF-001 |
| MAP-TAG-02 | App — hiển thị | Chat 1:1; My page | SYNC-APP-001 |
| MAP-TAG-03 | Web — cập nhật | Chat 1:1 right bar; My page; **import CSV**; trả lời form (item gắn tag); modal multi action | DATA-001 |
| MAP-TAG-04 | App — cập nhật | Chat 1:1; My page | SYNC-APP-001 |
| MAP-TAG-05 | Chung | **Tag bị xóa hoặc đổi tên khi đang được điều kiện gửi tin tham chiếu** → nơi tham chiếu không được hỏng; **đối tượng gửi không được sai**. | DATA-REF-001, MSG-001 |

### C.4 Google Spreadsheet

| ID | Kênh | Điểm phát sinh | Quan điểm |
|---|---|---|---|
| MAP-GS-01 | Web | Tính năng có liên kết: **form answer, salon, lesson, QR code** | INTG-SHEET-001 |
| MAP-GS-02 | Web | Liên kết khi **chưa cấp quyền** → báo lỗi, không cho liên kết | INTG-SHEET-001, UI-003 |
| MAP-GS-03 | Web | **Mất quyền / mất liên kết sau khi đã liên kết** → hiện cảnh báo để user liên kết lại | INTG-SHEET-001, OUT-TRUTH-001 |
| MAP-GS-04 | Web | Tên file sinh tự động có **ký tự đặc biệt** | OUT-EXPORT-001 |
| MAP-GS-05 | Web | **Tiêu đề cột có ký tự xuống dòng** | OUT-EXPORT-001 |
| MAP-GS-06 | Job | **Job retry khi sync lỗi** (hiện có ở salon, lesson, form) — mỗi lần tính năng đổi **phải test lại job retry** | JOB-001, INTG-SHEET-001 |
| MAP-GS-07 | Chung | **Form có 2 loại header spreadsheet**: header cũ = 1 cột tên người trả lời; header mới = 2 cột **Tên LINE + `システム表示名`**. **Phải test cả hai.** | COMPAT-LEGACY-001, OUT-EXPORT-001 |

### C.5 Sort — 25 màn

| ID | Điểm phát sinh | Điều phải xác nhận | Quan điểm |
|---|---|---|---|
| MAP-SORT-01 | **Các màn có sort**: folder (nhiều màn) · bot ở overview · chat 1:1 (info friend, trạng thái chat) · My page (info friend) · richmenu · image richmenu · scenario · auto reply · form answer · template · tag · QR code · friend info · action schedule · remind · popup · booking event · salon (course, staff, item form) · lesson (course, item form) · quản lý CSV · quản lý item · quản lý staff · conversion · URL | Với **mỗi** màn: chạy chuỗi thao tác liên tiếp **không reload** — thêm→sort, sửa→sort, xóa→sort, sort→sort. Sau mỗi chuỗi **F5**, thứ tự phải giữ nguyên. | FUNC-SEQ-001 |

### C.6 Giới hạn theo gói

| ID | Điểm phát sinh | Điều phải xác nhận | Quan điểm |
|---|---|---|---|
| MAP-PLAN-01 | Giới hạn lúc **tạo mới** | Bảng giới hạn theo gói do PM quản lý; đối chiếu trước khi viết case. | PAY-LIMIT-001, FUNC-004 |
| MAP-PLAN-02 | Giới hạn lúc **copy / nhân bản** | **Copy phải bị chặn khi đã đạt giới hạn — thường bị bỏ sót.** | PAY-LIMIT-001 |
| MAP-PLAN-03 | Giới hạn lúc **khôi phục dữ liệu đã xóa mềm** | | PAY-LIMIT-001, DATA-BACKUP-001 |
| MAP-PLAN-04 | **Mở 2 tab** rồi cùng thao tác tại ngưỡng giới hạn | Chỉ **1 thao tác** được phép thành công. | CONC-001, PAY-LIMIT-001 |
| MAP-PLAN-05 | **Double click** ở lần tạo cuối cùng trước khi chạm giới hạn | Không được vượt giới hạn. | CONC-001, PAY-LIMIT-001 |
| MAP-PLAN-06 | Chức năng **KHÔNG phụ thuộc gói** vẫn phải test trên **nhiều gói** | Bug external link từng lọt vì chỉ test trên gói Standard. | PAY-LIMIT-001 |

### C.7 Bill tiền

| ID | Kênh | Điểm phát sinh | Điều phải xác nhận | Quan điểm |
|---|---|---|---|---|
| MAP-PAY-01 | Web | Các luồng: **bill bot · item mua 1 lần · item chu kỳ · salon · lesson · event booking** | Mỗi luồng test đủ: **thành công / thất bại rồi retry / hủy giữa chừng / thanh toán lại / thanh toán trùng / charge sau khi đã hủy**. | PAY-STATE-001, PAY-ABANDON-001 |
| MAP-PAY-02 | Job | **Callback về trễ** | Trạng thái phải đúng khi callback đến **sau khi user đã rời màn hình**. | INTG-HOOK-001, PAY-ABANDON-001 |

### C.8 Hủy hợp đồng — danh sách dọn dẹp bắt buộc

| ID | Kênh | Điểm phát sinh | Quan điểm |
|---|---|---|---|
| MAP-CANCEL-01 | Job | **Xóa toàn bộ richmenu của LINE user** | STATE-CLEAN-001 |
| MAP-CANCEL-02 | Job | **Hủy toàn bộ schedule**: broadcast · step message · remind (event, lesson, salon, form) · action schedule · schedule gửi từ chat 1:1 · schedule gửi từ message error · schedule hiển thị và dừng richmenu | STATE-CLEAN-001 |
| MAP-CANCEL-03 | LINE user | **QR code không được chạy action nữa** | STATE-CLEAN-001 |
| MAP-CANCEL-04 | Chung | **Mọi tính năng khi version-up phải test lại luồng hủy hợp đồng** — hết hạn hợp đồng thì tính năng phải ngừng chạy. | STATE-CLEAN-001, PAY-PLAN-001 |

### C.9 Link phía LINE user

| ID | Điểm phát sinh | Điều phải xác nhận | Quan điểm |
|---|---|---|---|
| MAP-LIFF-01 | **Loại link**: form, item, event, salon, lesson, conversion, QR code, popup | | LIFF-ENTRY-001 |
| MAP-LIFF-02 | **Trạng thái kết bạn** | **Chưa là bạn → chuyển sang màn kết bạn.** Đã là bạn → vào thẳng. | LIFF-ENTRY-001 |
| MAP-LIFF-03 | **Điểm vào** | Mở trong app LINE · mở bằng **trình duyệt ngoài** · mở từ **nút trong tin nhắn** · mở từ **PC**. | LIFF-ENTRY-001 |
| MAP-LIFF-04 | **Link cũ và link mới** | Form cũ trỏ `step3.lmes.jp`, form mới trỏ `s.lmes.jp` — **cả hai phải truy cập được**. | COMPAT-LEGACY-001, ENV-003 |

### C.10 Phân quyền

| ID | Điểm phát sinh | Điều phải xác nhận | Quan điểm |
|---|---|---|---|
| MAP-PERM-01 | **Ma trận tài khoản** | Chỉ là **owner** của bot · **staff của 1 bot** · **staff của nhiều bot** · vừa là owner vừa là staff của bot khác. | PERM-001, PERM-003 |
| MAP-PERM-02 | **Đường truy cập khi staff không có quyền** | Từ **menu chính** · từ **menu favourite** · **gõ thẳng URL** · từ **hyperlink** dẫn tới màn đó. | PERM-002 |
| MAP-PERM-03 | **Đổi param ID trên URL** sang bot khác hoặc user khác | Từ chối truy cập. | PERM-002, PERM-003 |

---

## Catalog D — Khác biệt Dev / Staging / Production

> **RULE-08 bắt buộc đối chiếu bảng này trước khi kết luận "đã test xong".**
> Hạng mục **media · domain · job · cân bằng tải · bill tiền** **KHÔNG** được kết luận từ staging.

| ID | Hạng mục | Dev / Staging | **Production** | Rủi ro nếu chỉ kết luận từ staging | Việc phải làm | Quan điểm |
|---|---|---|---|---|---|---|
| **ENV-JOB** | Job nền | 1 job chạy tất cả, gồm cả callback | **3 job độc lập**: callback / broadcast / scenario. Thêm **job download media**. | Lỗi tranh chấp giữa các job chỉ lộ ra khi chạy tách tiến trình. | Chạy lại luồng gửi tin trên production sau release; theo dõi log của **cả 3 job**. | JOB-001, ENV-003 |
| **ENV-MEDIA-STORE** | Lưu trữ media | Chung server với ứng dụng | **Server riêng.** Ảnh lưu tạm ~1 ngày rồi **sync lên B2**; sau đó truy cập thẳng B2. | Xóa file, đổi path, cache ảnh **chỉ sai trên production**. | Tính năng sửa media **BẮT BUỘC verify trên production**. Kiểm file cũ đã xóa bằng `?v=x` → kỳ vọng **404**. | MEDIA-CLEAN-001, ENV-003 |
| **ENV-MEDIA-DOMAIN** | Domain media | Domain chính | **`p.lmes.jp`** | Nút download **mở tab mới thay vì tải file**; ảnh 404. | Truy cập media qua link step hoặc shorten phải **redirect sang `p.lmes.jp`**. | ENV-003, MEDIA-001 |
| **ENV-DOMAIN** | Domain ứng dụng | Chung 1 domain | **`step.lmes.jp`** (admin, link form cũ, popup, conversion cũ) + **`s.lmes.jp`** (shorten, form/LIFF mới) | **Link cũ của khách hàng chết sau release.** | Cả link cũ và link mới đều phải truy cập được. | COMPAT-LEGACY-001, REG-URL-001 |
| **ENV-PATH** | Path media | Dễ dãi | **Đi qua B2, nghiêm ngặt hơn** | Path thừa dấu `//` vẫn chạy ở dev nhưng **hỏng ở production**. File **không có phần mở rộng**: dev/staging vẫn nhận diện kiểu, production qua B2 tính là file. | Đổi path media sau release phải **kiểm tra lại toàn bộ ảnh cũ**. | ENV-003, DATA-MIG-001 |
| **ENV-LB** | Cân bằng tải | Không có | **2 server** | Lỗi chỉ xuất hiện ở **một** server; session không đồng bộ. | **Lưu lại router id** và chạy bộ case cơ bản trên **từng router**. | ENV-001, ENV-003 |
| **ENV-PAY** | Bill tiền | Tài khoản test | **Tài khoản thật** | Không thể tái hiện lỗi cổng thanh toán ở môi trường test. | **Đối soát với bản ghi của cổng thanh toán** sau mỗi release chạm luồng tiền. | PAY-STATE-001 |
| **ENV-HOOK** | Webhook | **Có thể không nhận được** | Nhận đầy đủ | Tính năng phụ thuộc webhook **bị bỏ qua không test** vì "không tái hiện được". | **Liệt kê và giả lập đủ pattern**: bình thường / bất thường / ngoại lệ / không đến / trùng / sai thứ tự. | INTG-HOOK-001, INTG-HOOK-002 |
| **ENV-ASSET** | Cache & asset | Ít ảnh hưởng | **User giữ cache lâu**; font + icon tải từ media server riêng | Sau release user phải **Ctrl+F5** mới dùng được; mất icon; sai font. | Gắn **version/hash** cho mọi JS/CSS/font. Nghiệm thu bằng **F5 thường** trên browser còn cache bản cũ. | DEPLOY-ASSET-001 |
| **ENV-NEWSRV** | Thêm server mới | — | — | Webhook không tới; **thiếu thiết lập bảo mật**. | Bắt buộc **疎通テスト** (test kết nối tới server đích) + kiểm cấu hình bảo mật **trước khi** đưa vào vận hành. | ENV-001, ENV-003 |
| **ENV-POPUP** | Cache popup | — | **Có cache riêng** | Popup hiển thị **nội dung cũ** sau khi admin sửa. | Kiểm popup sau khi đổi nội dung, trên browser **đã từng xem popup cũ**. | DATA-CACHE-001 |

---

## Catalog D2 — Checklist tầng job nền

> Dùng kèm: `JOB-001`, `INTG-HOOK-001`, `CONC-002`, `REG-RUN-001`, `MEDIA-CLEAN-001`.

| ID | Loại job | Mục kiểm | Chi tiết | Quan điểm |
|---|---|---|---|---|
| **JOB-01** | Job sync (Java) | **Rate limit** của API bên thứ 3 | Tra **tài liệu chính thức mới nhất** để lấy ngưỡng hiện hành (RULE-05). Tạo dữ liệu request **lớn và liên tục vượt ngưỡng**, xác nhận job có retry. | JOB-001 |
| **JOB-02** | Job sync (Java) | **Retry và backoff** | Job lỗi phải retry **có backoff**, ghi log từng lần. **Số bản ghi vào = số xử lý thành công + số vào hàng đợi lỗi.** | JOB-001 |
| **JOB-03** | Job callback | Callback đến **trễ / trùng / sai thứ tự** | Không được xử lý sai hoặc **ghi trùng bản ghi**. | INTG-HOOK-001, CONC-001 |
| **JOB-04** | Job broadcast / scenario | **Release khi job đang chạy dở** | Job đang chạy không bị gián đoạn; dữ liệu dở dang không bị mất. | REG-RUN-001 |
| **JOB-05** | Job download media | **Sync lên B2** | File mới upload **chưa kịp sync**; file đã xóa **phải mất ở cả hai nơi**. | MEDIA-CLEAN-001, ENV-003 |
| **JOB-06** | Mọi job | **Re-sync toàn bộ** trong lúc có dữ liệu mới phát sinh | Không làm mất và **không nhân đôi** dữ liệu mới. | CONC-002 |

---

## Catalog E — Giới hạn và ma trận media

> Tra **ngưỡng chính thức của LINE theo RULE-05** trước khi chốt case.

### Khối E1 — Giới hạn dung lượng theo nơi sử dụng

> ⚠️ **Giới hạn khác nhau giữa chat 1:1 và friend info — đây là chỗ hay nhầm.**

| ID | Nơi sử dụng | Loại file | Giới hạn chính thức | Ghi chú |
|---|---|---|---|---|
| MED-L01 | Chat 1:1 (web & app) | Ảnh | **10 MB** | |
| MED-L02 | Chat 1:1 (web & app) | PDF | **10 MB** | |
| MED-L03 | Chat 1:1 (web & app) | Audio | **25 MB** | Cần xác nhận lại validate phía web trước khi viết case. |
| MED-L04 | Chat 1:1 (web & app) | Video | **200 MB** | |
| MED-L05 | **Friend info** | Ảnh | **1 MB** | ⚠️ **Khác giới hạn của chat 1:1 — dễ nhầm.** |
| MED-L06 | Friend info | PDF | **10 MB** | |
| MED-L07 | Template | Ảnh | **10 MB** | |
| MED-L08 | Template | Audio / Video | **200 MB** | |
| MED-L09 | Richmenu | Ảnh | Theo giới hạn của LINE (**ảnh quá lớn không hiển thị**) | Tra tài liệu LINE mới nhất (RULE-05). |
| MED-L10 | **Mọi nơi upload ảnh** | Ảnh | Cạnh **> 2048px: tự resize giữ tỉ lệ**. Cạnh **> 10.000px: chặn upload**. | |

### Khối E2 — Ma trận tính năng × thao tác

| ID | Tính năng | Thao tác | Loại media | Điều phải xác nhận | Quan điểm |
|---|---|---|---|---|---|
| MED-01 | **Chat 1:1** | Upload | Ảnh (album, camera), PDF, audio (mp3, m4a), video | File sai định dạng bị chặn. **File media cũ vẫn hiển thị bình thường.** | MEDIA-001, SYNC-APP-001 |
| MED-02 | **Friend info** | Upload, sửa | Ảnh, PDF | **Đổi file → file cũ bị xóa trên server.** | MEDIA-CLEAN-001, FRIEND-001 |
| MED-03 | **Profile người gửi** | Upload, sửa | Ảnh | Ảnh profile áp dụng đúng khi gửi template. | MEDIA-001, MSG-004 |
| MED-04 | **Template** | Tạo, sửa, **copy**, preview, send test, backup | Ảnh, video (có thumbnail), audio, imagemap, button (standard/color/image), PDF trong template text | **6 kiểu template × 6 thao tác.** **Copy phải cập nhật toàn bộ field phụ thuộc, không giữ giá trị bản gốc.** Video clone phải có thumbnail. | MEDIA-001, DATA-REF-001, OUT-PREVIEW-001 |
| MED-05 | **Richmenu** | Tạo, sửa, copy, preview | Ảnh | Sau khi sửa, **richmenu của friend hiện có cũng phải cập nhật sang ảnh mới**. Sau copy, ảnh phải hiển thị. | MEDIA-IMG-001, STATE-DEP-001 |
| MED-06 | **Image richmenu** | Tạo | Ảnh (`背景` toàn bộ, khung nền) | **Cả hai vùng upload ảnh trong design đều phải kiểm.** | MEDIA-IMG-001 |
| MED-07 | **Scenario** | Clone template, copy message & action, copy toàn bộ step, copy scenario | Ảnh, video | **Copy sang filter khác vẫn giữ đúng media.** | DATA-REF-001, MEDIA-001 |
| MED-08 | **Broadcast (send all)** | Thêm ảnh trực tiếp, clone template, copy từ màn danh sách, preview, send test | Ảnh | | MEDIA-001, OUT-PREVIEW-001 |
| MED-09 | **Remind** | Thêm ảnh trực tiếp, clone template, copy, preview | Ảnh | | MEDIA-001 |
| MED-10 | **QR code** | Tạo khi thêm bot, tạo khi đổi bot, QR kết bạn | Ảnh | **Nút download phải tải file thật, không mở tab mới.** Kiểm tra **trên production** (domain `p.lmes.jp`). | ENV-003, MEDIA-001 |
| MED-11 | **Mọi tính năng upload** | Xóa, thay file | Mọi loại | **File cũ trả 404 ở cả server local và B2** khi truy cập kèm `?v=x`. | MEDIA-CLEAN-001 |
| MED-12 | **Mọi tính năng upload** | Lưu | Mọi loại | **Path trước và sau khi save giống nhau.** Preview mở được **cả trước khi bấm save và sau khi save**. | MEDIA-001, OUT-PREVIEW-001 |
