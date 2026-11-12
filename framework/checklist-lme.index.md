<!-- AUTO-GENERATED bởi scripts/build_indexes.py từ framework/checklist-lme.md — KHÔNG sửa tay. Sửa file gốc rồi chạy lại script. -->

# Index quan điểm test LME — tầng 1 (81 quan điểm)

> Bảng tra nhanh cho **BƯỚC 3b** của `/review-tc` và `/write-tc`.
> Chọn quan điểm có **Trigger khớp task** ở bảng dưới, rồi đọc chi tiết (`Kiểm tra` + `Evidence`) **chỉ của các mã đã chọn**:
>
> ```
> sed -n '<Dòng>p' framework/checklist-lme.md
> ```
>
> **KHÔNG nạp toàn văn** [checklist-lme.md](checklist-lme.md) (574 dòng ≈ 23k token).
> Nguồn sự thật vẫn là file gốc — file này là output tự sinh.
>
> **13 RULE bắt buộc** (kèm bảng mã HTTP của RULE-13) — đọc đủ, rẻ: `sed -n '58,89p' framework/checklist-lme.md`.
> **§4 "Quan điểm chưa đủ bằng chứng"** (FORM-01, CHAT-01, ADM-01/03/04, TPL-01) KHÔNG có trong bảng này — theo **RULE-11** chỉ được nêu ở mức `[NIT]`.

| Mã | Ưu tiên | Catalog | Nhóm | Trigger | Dòng |
|---|---|---|---|---|---|
| `FUNC-001` | Cao | C | 2.1 Chức năng (Functional) | mọi chức năng — luôn bắt buộc. | 101,104 |
| `FUNC-002` | Cao | A | 2.1 Chức năng (Functional) | mọi chức năng có form nhập liệu. | 106,109 |
| `FUNC-003` | Trung bình (→ Cao khi field liên quan URL/LIFF, ngày giờ, số tiền, token, webhook URL, PII) | A | 2.1 Chức năng (Functional) | mọi field có định dạng quy định (email, SĐT, URL, ngày tháng). | 111,114 |
| `FUNC-004` | Cao | A, C | 2.1 Chức năng (Functional) | mọi chức năng có giới hạn số lượng / ký tự / dung lượng. | 116,119 |
| `FUNC-MULTI-001` | Trung bình | A | 2.1 Chức năng (Functional) | chức năng cho phép thêm ≥2 phần tử cùng loại trong 1 đối tượng (nhiều file upload, nhiều URL trong 1 tin, nhiều điều kiện lọc). | 121,124 |
| `FUNC-DATE-001` | Cao | A | 2.1 Chức năng (Functional) | chức năng có tính toán / so sánh ngày giờ (hạn, "N ngày sau", remind). | 126,129 |
| `FUNC-DRAFT-001` | Trung bình | B | 2.1 Chức năng (Functional) | **chỉ** editor/soạn thảo (chat, template, form builder). KHÔNG áp dụng đại trà. | 131,134 |
| `FUNC-UNIQ-001` | Trung bình | A | 2.1 Chức năng (Functional) | có field bắt buộc duy nhất (email, mã số) và user sửa được bản ghi của mình. | 136,139 |
| `FUNC-SEQ-001` ★ | Trung bình | C | 2.1 Chức năng (Functional) | **BẮT BUỘC** với màn có ≥2 thao tác trên cùng danh sách (đặc biệt có **Sort**), hoặc nhiều tab setting chung 1 nút Save. | 141,144 |
| `CONC-001` | Cao | C | 2.2 Đồng thời & Idempotency | **BẮT BUỘC** khi có nút thực thi hành động quan trọng / nhiều người cùng sửa / batch đa luồng / giới hạn dùng chung. | 148,151 |
| `CONC-002` | Trung bình (→ Cao với form/payment/chat/friend) | D | 2.2 Đồng thời & Idempotency | có tiến trình re-sync/tính lại **TOÀN BỘ** dữ liệu cũ chạy nền, và dữ liệu mới có thể phát sinh trong lúc đó. | 153,156 |
| `CONC-003` ★ | Trung bình (→ Cao khi màn có loadmore/phân trang + filter, hoặc nhiều tab cùng gọi API) | B | 2.2 Đồng thời & Idempotency | × chỉ khi màn hình chỉ có 1 request tĩnh. _(Khác CONC-001: đây là race tầng **client**, response về không đúng thứ tự gửi.)_ | 158,161 |
| `DATA-001` | Cao | C | 2.3 Toàn vẹn dữ liệu | mọi chức năng cập nhật dữ liệu được tham chiếu ở nơi khác. | 165,168 |
| `DATA-COUNT-001` | Cao | C | 2.3 Toàn vẹn dữ liệu | **BẮT BUỘC** khi màn hình có bất kỳ con số đếm / tỷ lệ / tổng hợp nào. | 170,174 |
| `DATA-TEXT-001` | Trung bình (→ Cao nếu text được gửi LINE / export CSV) | A | 2.3 Toàn vẹn dữ liệu | có input text tự do sẽ được lưu / hiển thị / gửi qua LINE / export. | 176,179 |
| `DATA-REF-001` | Cao | C | 2.3 Toàn vẹn dữ liệu | **BẮT BUỘC** khi đối tượng có thao tác xóa/copy/đổi tên/di chuyển VÀ được nơi khác tham chiếu. | 181,184 |
| `DATA-ID-001` | Trung bình (→ Cao với màn chọn đối tượng để thao tác) | — | 2.3 Toàn vẹn dữ liệu | chức năng hiển thị/chọn/nhóm đối tượng có thể **trùng tên**. | 186,189 |
| `DATA-MIG-001` | Cao | D | 2.3 Toàn vẹn dữ liệu | **BẮT BUỘC** khi release đổi cấu trúc dữ liệu và tồn tại dữ liệu cũ. Dấu hiệu trong spec: "tương thích ngược" / "migration" / "移行" / "định dạng mới" / "version-up" / đổi cấu trúc field. | 191,194 |
| `DATA-CACHE-001` | Trung bình (→ Cao nếu output user-facing) | D | 2.3 Toàn vẹn dữ liệu | release có đổi JS/asset, hoặc chức năng dùng short link / preview / cache tầng ngoài. | 196,199 |
| `DATA-BACKUP-001` ★ | Cao | C | 2.3 Toàn vẹn dữ liệu | **BẮT BUỘC** khi tính năng **thêm/đổi bảng DB**, hoặc chạm backup / copy bot / restore data đã xóa mềm. | 201,204 |
| `DATA-DB-001` ★ | Cao | C | 2.3 Toàn vẹn dữ liệu | **BẮT BUỘC** với mọi chức năng có UPDATE hoặc DELETE. **Không thay thế được bằng kiểm tra trên UI** (RULE-07). | 206,209 |
| `DATA-AUDIT-001` | Cao | — | 2.3 Toàn vẹn dữ liệu | **BẮT BUỘC** khi có thao tác xóa/sửa/đổi trạng thái trên **dữ liệu nhạy cảm** (khách hàng, thanh toán/hợp đồng, phân quyền, tag). Dấu hiệu spec: màn `操作履歴` / lịch sử thao tác / audit / activity log. | 211,215 |
| `INTG-LINE-001` | Cao | D | 2.4 Tích hợp & Đồng bộ | **BẮT BUỘC** khi chức năng gọi LINE API / LIFF / nhận webhook LINE. | 219,222 |
| `INTG-HOOK-001` | Cao | D | 2.4 Tích hợp & Đồng bộ | **BẮT BUỘC** khi nhận webhook từ bên ngoài (thanh toán, LINE, Google). | 224,227 |
| `INTG-HOOK-002` | Trung bình | D | 2.4 Tích hợp & Đồng bộ | luồng nghiệp vụ chỉ hoàn tất khi nhận callback/webhook từ bên ngoài. | 229,232 |
| `INTG-CAL-001` | Cao | C | 2.4 Tích hợp & Đồng bộ | **BẮT BUỘC** khi đồng bộ lịch/sự kiện 2 chiều với dịch vụ ngoài (Google Calendar). | 234,238 |
| `INTG-SHEET-001` | Cao | C | 2.4 Tích hợp & Đồng bộ | **BẮT BUỘC** khi ghi dữ liệu khách hàng (câu trả lời form...) ra spreadsheet ngoài. | 240,243 |
| `SYNC-APP-001` | Trung bình (→ Cao với flow critical user-facing) | C, E | 2.4 Tích hợp & Đồng bộ | tính năng có mặt trên cả web và app. | 245,248 |
| `PERM-001` | Cao | C | 2.5 Phân quyền | **BẮT BUỘC** khi chức năng có phân biệt quyền. | 252,255 |
| `PERM-002` | Cao | C | 2.5 Phân quyền | **BẮT BUỘC** khi có thao tác nhạy cảm (xóa / thanh toán / export / PII). | 257,260 |
| `PERM-003` | Cao | C | 2.5 Phân quyền | **BẮT BUỘC** khi tổ chức vận hành nhiều LINE OA hoặc có chức năng **change bot**. | 262,265 |
| `PERM-004` | Trung bình (→ Cao khi quyền liên quan PII hoặc thanh toán) | — | 2.5 Phân quyền | **BẮT BUỘC** khi có thao tác mời/xóa/đổi quyền thành viên. | 267,270 |
| `MSG-001` | Cao | C | 2.6 Gửi tin / LINE đặc thù | **BẮT BUỘC** với mọi chức năng gửi tin có điều kiện lọc. | 274,278 |
| `MSG-002` | Cao | C | 2.6 Gửi tin / LINE đặc thù | **BẮT BUỘC** với gửi tin đặt lịch / step theo thời gian. | 280,283 |
| `MSG-003` | Cao | C | 2.6 Gửi tin / LINE đặc thù | **BẮT BUỘC** với mọi chức năng gửi tin hàng loạt. | 285,288 |
| `MSG-004` | Cao | C, E | 2.6 Gửi tin / LINE đặc thù | **BẮT BUỘC** khi output là nội dung user cuối nhìn thấy trên LINE. | 290,293 |
| `MSG-005` | Cao | C | 2.6 Gửi tin / LINE đặc thù | **BẮT BUỘC** khi chức năng tiêu thụ quota tin nhắn. | 295,298 |
| `MSG-USER-001` | Cao | C | 2.6 Gửi tin / LINE đặc thù | **BẮT BUỘC** khi chức năng tương tác với friend LINE ở bất kỳ dạng nào. | 300,303 |
| `LIFF-ENTRY-001` ★ | Cao | C | 2.6 Gửi tin / LINE đặc thù | **BẮT BUỘC** khi tính năng phát sinh URL cho LINE user access (form, item, event, salon, lesson, conversion, QR code, popup). | 305,312 |
| `OUT-PREVIEW-001` | Cao | C, E | 2.7 Output & Preview | **BẮT BUỘC** khi chức năng có chế độ preview hoặc test send. | 316,319 |
| `OUT-TRUTH-001` | Cao | — | 2.7 Output & Preview | **BẮT BUỘC** với mọi thao tác lưu/gửi/đồng bộ **có thông báo kết quả**. | 321,324 |
| `TOOL-KNOW-005` | Cao | C, E | 2.7 Output & Preview | **BẮT BUỘC** khi thêm/sửa **MCP tool · API · service dùng chung** có chức năng **tạo / cập nhật / sao chép** message hoặc action; hoặc khi đổi **media, vùng tap, button, liên kết, cấu hình** được dùng lúc gửi tin. | 326,329 |
| `OUT-EXPORT-001` ★ | Trung bình → BẮT BUỘC (nâng Cao) | C, A | 2.7 Output & Preview | với mọi chức năng export CSV / ghi Google Spreadsheet / sinh file cho khách tải | 331,333 |
| `NOTI-MAIL-001` ★ | Trung bình → BẮT BUỘC (nâng Cao) | C | 2.7 Output & Preview | khi mail chứa link xác thực / thanh toán / khôi phục mật khẩu | 335,337 |
| `UI-001` | Trung bình (→ Cao với flow critical user-facing) | B | 2.8 Giao diện / UX | mọi chức năng có UI. | 341,344 |
| `UI-002` | Trung bình | B | 2.8 Giao diện / UX | mọi chức năng có UI user-facing. | 346,349 |
| `UI-003` | Trung bình (→ Cao khi có rủi ro **false success**) | B | 2.8 Giao diện / UX | mọi màn danh sách / xử lý bất đồng bộ. | 351,354 |
| `UI-004` | Thấp | — | 2.8 Giao diện / UX | **chỉ** onboarding hoặc flow phức tạp — KHÔNG phải release gate chung. | 356,358 |
| `UI-FIELD-001` | Trung bình | B | 2.8 Giao diện / UX | form/settings có field phụ thuộc lựa chọn cha (loại điều kiện, loại action). | 360,363 |
| `UI-INPUT-001` ★ | Trung bình | A, B | 2.8 Giao diện / UX | **BẮT BUỘC** với mọi màn có ô nhập text / area text. | 365,368 |
| `PAY-STATE-001` | Cao | C | 2.9 Thanh toán & Gói cước | **BẮT BUỘC** với mọi chức năng có giao dịch tiền hoặc đổi trạng thái hợp đồng. Dấu hiệu spec: sơ đồ trạng thái thanh toán, bảng trạng thái đơn hàng, `決済ステータス` / `入金確認中`. | 374,378 |
| `PAY-PLAN-001` | Cao | C | 2.9 Thanh toán & Gói cước | **BẮT BUỘC** với mọi thao tác thay đổi gói/hợp đồng. | 380,383 |
| `PAY-AMOUNT-001` | Cao | C | 2.9 Thanh toán & Gói cước | **BẮT BUỘC** khi có tính tiền: pro-rate, đổi chu kỳ, thuế, giảm giá. | 385,388 |
| `PAY-BATCH-001` | Cao | C | 2.9 Thanh toán & Gói cước | **BẮT BUỘC** khi có xử lý batch/định kỳ tác động **tiền hoặc gửi tin**. | 390,393 |
| `PAY-CONFIRM-001` | Cao | C | 2.9 Thanh toán & Gói cước | **BẮT BUỘC** khi có dữ liệu 2 giai đoạn (tạm → chính thức): hoa hồng affiliate tạm tính, thanh toán tạm giữ, booking tạm, import chờ duyệt. | 395,398 |
| `PAY-ABANDON-001` | Cao | C | 2.9 Thanh toán & Gói cước | **BẮT BUỘC** với mọi luồng thanh toán / subscription. | 400,403 |
| `PAY-LIMIT-001` | Cao | C | 2.9 Thanh toán & Gói cước | **BẮT BUỘC** khi chức năng bị giới hạn theo gói. | 405,408 |
| `STATE-001` | Cao | C | 2.10 Trạng thái & Lifecycle | **BẮT BUỘC** khi nghiệp vụ gồm **≥2 bước ghi dữ liệu tuần tự** (đổi gói, tạo đơn, connect bot, copy). | 412,415 |
| `STATE-CLEAN-001` | Cao | C | 2.10 Trạng thái & Lifecycle | **BẮT BUỘC** khi có thao tác hủy hợp đồng / ngắt kết nối bot-OA / gỡ tích hợp / hạ gói. | 417,420 |
| `STATE-DEP-001` | Cao | C | 2.10 Trạng thái & Lifecycle | **BẮT BUỘC** khi sự kiện có hành động phụ thuộc **đã lên lịch** (remind / gửi tin / thanh toán) và gốc có thể bị đổi. | 422,425 |
| `REG-SHARED-001` | Cao | D | 2.11 Regression & Phạm vi ảnh hưởng | **BẮT BUỘC** với mọi release sửa code dùng chung hoặc fix bug **có thể tồn tại ở chức năng tương tự**. Dấu hiệu: "dùng chung" / "shared" / "component chung" / `共通`. | 429,432 |
| `REG-RUN-001` | Cao | D | 2.11 Regression & Phạm vi ảnh hưởng | **BẮT BUỘC** với mọi release khi hệ thống có job/dữ liệu đang chạy dở. | 434,437 |
| `REG-SPEC-001` | Cao | — | 2.11 Regression & Phạm vi ảnh hưởng | **BẮT BUỘC** với mọi thay đổi spec/requirement xảy ra **SAU** khi đã có test case (kể cả thay đổi nhỏ). | 439,442 |
| `REG-URL-001` ★ | Trung bình → BẮT BUỘC (nâng Cao) | D | 2.11 Regression & Phạm vi ảnh hưởng | khi CR chạm màn đăng ký / login / overview / thanh toán / kết nối bot | 444,450 |
| `SEC-001` | Cao | C | 2.12 Bảo mật | **BẮT BUỘC** khi chức năng chạm dữ liệu cá nhân khách hàng. | 454,457 |
| `SEC-002` | Cao | — | 2.12 Bảo mật | **BẮT BUỘC** khi chức năng xử lý credential / token / payment. | 459,462 |
| `SEC-ISO-001` | Cao | C | 2.12 Bảo mật | **BẮT BUỘC** khi UI tải/hiển thị **nhiều đối tượng dữ liệu đồng thời** (nhiều cuộc trò chuyện, nhiều tab). | 464,467 |
| `PERF-LARGE-001` | Trung bình (→ Cao với gửi tin / export / sync / phân tích) | D | 2.13 Hiệu năng & Dữ liệu lớn | mọi chức năng xử lý danh sách / khối lượng dữ liệu. Dấu hiệu spec: `大規模` / `大量` / `一括`. | 471,474 |
| `ENV-001` | Cao | D | 2.14 Hạ tầng & Môi trường | chức năng có bước validate quan trọng (slot, tồn kho, tiền) chạy qua nhiều server. | 478,481 |
| `ENV-002` | Trung bình | D | 2.14 Hạ tầng & Môi trường | release có đổi cấu hình hạ tầng (CDN / security rule) **kèm ngoại lệ** cần cấu hình riêng. | 483,486 |
| `ENV-003` ★ | Cao | D | 2.14 Hạ tầng & Môi trường | **BẮT BUỘC** khi tính năng chạm **media/file, URL/domain, job nền, thanh toán**, hoặc khi **thêm server mới**. **Không được đánh × với lý do "staging đã pass"** (RULE-08). | 488,498 |
| `JOB-001` ★ | Cao | D (+ D2) | 2.14 Hạ tầng & Môi trường | **BẮT BUỘC** khi tính năng thêm/sửa job nền, hoặc gọi API bên thứ 3 theo lô. × chỉ khi **hoàn toàn không có xử lý nền**. | 500,503 |
| `LIST-001` | Trung bình | B | 2.15 List & Thao tác hàng loạt | **BẮT BUỘC** với mọi màn danh sách có search/filter/pagination. | 507,510 |
| `BULK-001` | Cao | C | 2.15 List & Thao tác hàng loạt | **BẮT BUỘC** mỗi khi có tổ hợp **bộ lọc + thao tác hàng loạt** (gửi tin / gắn tag / đổi richmenu / đổi cấu hình). | 512,515 |
| `MEDIA-001` | Trung bình (→ Cao nếu output hiển thị cho khách cuối) | E | 2.16 Media / File | **BẮT BUỘC** khi chức năng có upload file/ảnh. | 519,522 |
| `MEDIA-CLEAN-001` ★ | Trung bình → BẮT BUỘC (nâng Cao) | E, D | 2.16 Media / File | khi chức năng cho phép **xóa hoặc thay thế** file/ảnh đã upload | 524,526 |
| `MEDIA-IMG-001` ★ | Trung bình → BẮT BUỘC (nâng Cao) | E, B | 2.16 Media / File | khi ảnh gửi ra phía LINE user hoặc dùng cho richmenu/imagemap | 528,530 |
| `FRIEND-001` | Cao | C | 2.17 Friend info | **BẮT BUỘC** khi chức năng đọc/ghi friend info hoặc dùng nó làm **điều kiện / biến**. | 534,538 |
| `DEPLOY-ASSET-001` ★ | Cao | D | 2.18 Release & Deploy | **BẮT BUỘC** khi release có sửa file JS/CSS/font/icon hoặc đổi cấu trúc dữ liệu mà GUI render. **Cao tuyệt đối** nếu file bị sửa nằm trong luồng **thanh toán / hủy hợp đồng**. | 542,545 |
| `DEPLOY-LIVE-001` ★ | Cao | D | 2.18 Release & Deploy | **BẮT BUỘC** với mọi release lên production **không bật maintain**, đặc biệt khi đổi **payload API / field form / cấu trúc request**. | 547,550 |
| `COMPAT-LEGACY-001` ★ | Cao | C, D | 2.18 Release & Deploy | **BẮT BUỘC** khi tính năng chạm template, form, remind, richmenu, google spread, hoặc **bất kỳ đối tượng nào đã từng version-up**. **Không được đánh × chỉ vì "dữ liệu mới chạy ổn"** (RULE-09). | 552,561 |

## Phân bố theo ưu tiên nền

> Đếm theo mức **nền**. `(→ Cao khi ...)` / `→ BẮT BUỘC (nâng Cao)` ở cột `Ưu tiên` là **điều kiện nâng lên Cao** — khớp điều kiện thì xử lý như quan điểm ưu tiên Cao (thiếu TC = `[BLOCKER]`, và RULE-01 bắt buộc đủ 3 loại case).

| Ưu tiên nền | Số quan điểm |
|---|---|
| Cao | 53 |
| Trung bình | 27 |
| Thấp | 1 |
