<!-- AUTO-GENERATED bởi scripts/build_indexes.py từ framework/checklist-lme.md — KHÔNG sửa tay. Sửa file gốc rồi chạy lại script. -->

# Index quan điểm test LME — tầng 1 (80 quan điểm)

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
> **12 RULE bắt buộc** — đọc đủ, rẻ: `sed -n '58,73p' framework/checklist-lme.md`.
> **§4 "Quan điểm chưa đủ bằng chứng"** (FORM-01, CHAT-01, ADM-01/03/04, TPL-01) KHÔNG có trong bảng này — theo **RULE-11** chỉ được nêu ở mức `[NIT]`.

| Mã | Ưu tiên | Catalog | Nhóm | Trigger | Dòng |
|---|---|---|---|---|---|
| `FUNC-001` | Cao | C | 2.1 Chức năng (Functional) | mọi chức năng — luôn bắt buộc. | 85,88 |
| `FUNC-002` | Cao | A | 2.1 Chức năng (Functional) | mọi chức năng có form nhập liệu. | 90,93 |
| `FUNC-003` | Trung bình (→ Cao khi field liên quan URL/LIFF, ngày giờ, số tiền, token, webhook URL, PII) | A | 2.1 Chức năng (Functional) | mọi field có định dạng quy định (email, SĐT, URL, ngày tháng). | 95,98 |
| `FUNC-004` | Cao | A, C | 2.1 Chức năng (Functional) | mọi chức năng có giới hạn số lượng / ký tự / dung lượng. | 100,103 |
| `FUNC-MULTI-001` | Trung bình | A | 2.1 Chức năng (Functional) | chức năng cho phép thêm ≥2 phần tử cùng loại trong 1 đối tượng (nhiều file upload, nhiều URL trong 1 tin, nhiều điều kiện lọc). | 105,108 |
| `FUNC-DATE-001` | Cao | A | 2.1 Chức năng (Functional) | chức năng có tính toán / so sánh ngày giờ (hạn, "N ngày sau", remind). | 110,113 |
| `FUNC-DRAFT-001` | Trung bình | B | 2.1 Chức năng (Functional) | **chỉ** editor/soạn thảo (chat, template, form builder). KHÔNG áp dụng đại trà. | 115,118 |
| `FUNC-UNIQ-001` | Trung bình | A | 2.1 Chức năng (Functional) | có field bắt buộc duy nhất (email, mã số) và user sửa được bản ghi của mình. | 120,123 |
| `FUNC-SEQ-001` ★ | Trung bình | C | 2.1 Chức năng (Functional) | **BẮT BUỘC** với màn có ≥2 thao tác trên cùng danh sách (đặc biệt có **Sort**), hoặc nhiều tab setting chung 1 nút Save. | 125,128 |
| `CONC-001` | Cao | C | 2.2 Đồng thời & Idempotency | **BẮT BUỘC** khi có nút thực thi hành động quan trọng / nhiều người cùng sửa / batch đa luồng / giới hạn dùng chung. | 132,135 |
| `CONC-002` | Trung bình (→ Cao với form/payment/chat/friend) | D | 2.2 Đồng thời & Idempotency | có tiến trình re-sync/tính lại **TOÀN BỘ** dữ liệu cũ chạy nền, và dữ liệu mới có thể phát sinh trong lúc đó. | 137,140 |
| `CONC-003` ★ | Trung bình (→ Cao khi màn có loadmore/phân trang + filter, hoặc nhiều tab cùng gọi API) | B | 2.2 Đồng thời & Idempotency | × chỉ khi màn hình chỉ có 1 request tĩnh. _(Khác CONC-001: đây là race tầng **client**, response về không đúng thứ tự gửi.)_ | 142,145 |
| `DATA-001` | Cao | C | 2.3 Toàn vẹn dữ liệu | mọi chức năng cập nhật dữ liệu được tham chiếu ở nơi khác. | 149,152 |
| `DATA-COUNT-001` | Cao | C | 2.3 Toàn vẹn dữ liệu | **BẮT BUỘC** khi màn hình có bất kỳ con số đếm / tỷ lệ / tổng hợp nào. | 154,158 |
| `DATA-TEXT-001` | Trung bình (→ Cao nếu text được gửi LINE / export CSV) | A | 2.3 Toàn vẹn dữ liệu | có input text tự do sẽ được lưu / hiển thị / gửi qua LINE / export. | 160,163 |
| `DATA-REF-001` | Cao | C | 2.3 Toàn vẹn dữ liệu | **BẮT BUỘC** khi đối tượng có thao tác xóa/copy/đổi tên/di chuyển VÀ được nơi khác tham chiếu. | 165,168 |
| `DATA-ID-001` | Trung bình (→ Cao với màn chọn đối tượng để thao tác) | — | 2.3 Toàn vẹn dữ liệu | chức năng hiển thị/chọn/nhóm đối tượng có thể **trùng tên**. | 170,173 |
| `DATA-MIG-001` | Cao | D | 2.3 Toàn vẹn dữ liệu | **BẮT BUỘC** khi release đổi cấu trúc dữ liệu và tồn tại dữ liệu cũ. Dấu hiệu trong spec: "tương thích ngược" / "migration" / "移行" / "định dạng mới" / "version-up" / đổi cấu trúc field. | 175,178 |
| `DATA-CACHE-001` | Trung bình (→ Cao nếu output user-facing) | D | 2.3 Toàn vẹn dữ liệu | release có đổi JS/asset, hoặc chức năng dùng short link / preview / cache tầng ngoài. | 180,183 |
| `DATA-BACKUP-001` ★ | Cao | C | 2.3 Toàn vẹn dữ liệu | **BẮT BUỘC** khi tính năng **thêm/đổi bảng DB**, hoặc chạm backup / copy bot / restore data đã xóa mềm. | 185,188 |
| `DATA-DB-001` ★ | Cao | C | 2.3 Toàn vẹn dữ liệu | **BẮT BUỘC** với mọi chức năng có UPDATE hoặc DELETE. **Không thay thế được bằng kiểm tra trên UI** (RULE-07). | 190,193 |
| `DATA-AUDIT-001` | Cao | — | 2.3 Toàn vẹn dữ liệu | **BẮT BUỘC** khi có thao tác xóa/sửa/đổi trạng thái trên **dữ liệu nhạy cảm** (khách hàng, thanh toán/hợp đồng, phân quyền, tag). Dấu hiệu spec: màn `操作履歴` / lịch sử thao tác / audit / activity log. | 195,199 |
| `INTG-LINE-001` | Cao | D | 2.4 Tích hợp & Đồng bộ | **BẮT BUỘC** khi chức năng gọi LINE API / LIFF / nhận webhook LINE. | 203,206 |
| `INTG-HOOK-001` | Cao | D | 2.4 Tích hợp & Đồng bộ | **BẮT BUỘC** khi nhận webhook từ bên ngoài (thanh toán, LINE, Google). | 208,211 |
| `INTG-HOOK-002` | Trung bình | D | 2.4 Tích hợp & Đồng bộ | luồng nghiệp vụ chỉ hoàn tất khi nhận callback/webhook từ bên ngoài. | 213,216 |
| `INTG-CAL-001` | Cao | C | 2.4 Tích hợp & Đồng bộ | **BẮT BUỘC** khi đồng bộ lịch/sự kiện 2 chiều với dịch vụ ngoài (Google Calendar). | 218,222 |
| `INTG-SHEET-001` | Cao | C | 2.4 Tích hợp & Đồng bộ | **BẮT BUỘC** khi ghi dữ liệu khách hàng (câu trả lời form...) ra spreadsheet ngoài. | 224,227 |
| `SYNC-APP-001` | Trung bình (→ Cao với flow critical user-facing) | C, E | 2.4 Tích hợp & Đồng bộ | tính năng có mặt trên cả web và app. | 229,232 |
| `PERM-001` | Cao | C | 2.5 Phân quyền | **BẮT BUỘC** khi chức năng có phân biệt quyền. | 236,239 |
| `PERM-002` | Cao | C | 2.5 Phân quyền | **BẮT BUỘC** khi có thao tác nhạy cảm (xóa / thanh toán / export / PII). | 241,244 |
| `PERM-003` | Cao | C | 2.5 Phân quyền | **BẮT BUỘC** khi tổ chức vận hành nhiều LINE OA hoặc có chức năng **change bot**. | 246,249 |
| `PERM-004` | Trung bình (→ Cao khi quyền liên quan PII hoặc thanh toán) | — | 2.5 Phân quyền | **BẮT BUỘC** khi có thao tác mời/xóa/đổi quyền thành viên. | 251,254 |
| `MSG-001` | Cao | C | 2.6 Gửi tin / LINE đặc thù | **BẮT BUỘC** với mọi chức năng gửi tin có điều kiện lọc. | 258,262 |
| `MSG-002` | Cao | C | 2.6 Gửi tin / LINE đặc thù | **BẮT BUỘC** với gửi tin đặt lịch / step theo thời gian. | 264,267 |
| `MSG-003` | Cao | C | 2.6 Gửi tin / LINE đặc thù | **BẮT BUỘC** với mọi chức năng gửi tin hàng loạt. | 269,272 |
| `MSG-004` | Cao | C, E | 2.6 Gửi tin / LINE đặc thù | **BẮT BUỘC** khi output là nội dung user cuối nhìn thấy trên LINE. | 274,277 |
| `MSG-005` | Cao | C | 2.6 Gửi tin / LINE đặc thù | **BẮT BUỘC** khi chức năng tiêu thụ quota tin nhắn. | 279,282 |
| `MSG-USER-001` | Cao | C | 2.6 Gửi tin / LINE đặc thù | **BẮT BUỘC** khi chức năng tương tác với friend LINE ở bất kỳ dạng nào. | 284,287 |
| `LIFF-ENTRY-001` ★ | Cao | C | 2.6 Gửi tin / LINE đặc thù | **BẮT BUỘC** khi tính năng phát sinh URL cho LINE user access (form, item, event, salon, lesson, conversion, QR code, popup). | 289,296 |
| `OUT-PREVIEW-001` | Cao | C, E | 2.7 Output & Preview | **BẮT BUỘC** khi chức năng có chế độ preview hoặc test send. | 300,303 |
| `OUT-TRUTH-001` | Cao | — | 2.7 Output & Preview | **BẮT BUỘC** với mọi thao tác lưu/gửi/đồng bộ **có thông báo kết quả**. | 305,308 |
| `OUT-EXPORT-001` ★ | Trung bình → BẮT BUỘC (nâng Cao) | C, A | 2.7 Output & Preview | với mọi chức năng export CSV / ghi Google Spreadsheet / sinh file cho khách tải | 310,312 |
| `NOTI-MAIL-001` ★ | Trung bình → BẮT BUỘC (nâng Cao) | C | 2.7 Output & Preview | khi mail chứa link xác thực / thanh toán / khôi phục mật khẩu | 314,316 |
| `UI-001` | Trung bình (→ Cao với flow critical user-facing) | B | 2.8 Giao diện / UX | mọi chức năng có UI. | 320,323 |
| `UI-002` | Trung bình | B | 2.8 Giao diện / UX | mọi chức năng có UI user-facing. | 325,328 |
| `UI-003` | Trung bình (→ Cao khi có rủi ro **false success**) | B | 2.8 Giao diện / UX | mọi màn danh sách / xử lý bất đồng bộ. | 330,333 |
| `UI-004` | Thấp | — | 2.8 Giao diện / UX | **chỉ** onboarding hoặc flow phức tạp — KHÔNG phải release gate chung. | 335,337 |
| `UI-FIELD-001` | Trung bình | B | 2.8 Giao diện / UX | form/settings có field phụ thuộc lựa chọn cha (loại điều kiện, loại action). | 339,342 |
| `UI-INPUT-001` ★ | Trung bình | A, B | 2.8 Giao diện / UX | **BẮT BUỘC** với mọi màn có ô nhập text / area text. | 344,347 |
| `PAY-STATE-001` | Cao | C | 2.9 Thanh toán & Gói cước | **BẮT BUỘC** với mọi chức năng có giao dịch tiền hoặc đổi trạng thái hợp đồng. Dấu hiệu spec: sơ đồ trạng thái thanh toán, bảng trạng thái đơn hàng, `決済ステータス` / `入金確認中`. | 353,357 |
| `PAY-PLAN-001` | Cao | C | 2.9 Thanh toán & Gói cước | **BẮT BUỘC** với mọi thao tác thay đổi gói/hợp đồng. | 359,362 |
| `PAY-AMOUNT-001` | Cao | C | 2.9 Thanh toán & Gói cước | **BẮT BUỘC** khi có tính tiền: pro-rate, đổi chu kỳ, thuế, giảm giá. | 364,367 |
| `PAY-BATCH-001` | Cao | C | 2.9 Thanh toán & Gói cước | **BẮT BUỘC** khi có xử lý batch/định kỳ tác động **tiền hoặc gửi tin**. | 369,372 |
| `PAY-CONFIRM-001` | Cao | C | 2.9 Thanh toán & Gói cước | **BẮT BUỘC** khi có dữ liệu 2 giai đoạn (tạm → chính thức): hoa hồng affiliate tạm tính, thanh toán tạm giữ, booking tạm, import chờ duyệt. | 374,377 |
| `PAY-ABANDON-001` | Cao | C | 2.9 Thanh toán & Gói cước | **BẮT BUỘC** với mọi luồng thanh toán / subscription. | 379,382 |
| `PAY-LIMIT-001` | Cao | C | 2.9 Thanh toán & Gói cước | **BẮT BUỘC** khi chức năng bị giới hạn theo gói. | 384,387 |
| `STATE-001` | Cao | C | 2.10 Trạng thái & Lifecycle | **BẮT BUỘC** khi nghiệp vụ gồm **≥2 bước ghi dữ liệu tuần tự** (đổi gói, tạo đơn, connect bot, copy). | 391,394 |
| `STATE-CLEAN-001` | Cao | C | 2.10 Trạng thái & Lifecycle | **BẮT BUỘC** khi có thao tác hủy hợp đồng / ngắt kết nối bot-OA / gỡ tích hợp / hạ gói. | 396,399 |
| `STATE-DEP-001` | Cao | C | 2.10 Trạng thái & Lifecycle | **BẮT BUỘC** khi sự kiện có hành động phụ thuộc **đã lên lịch** (remind / gửi tin / thanh toán) và gốc có thể bị đổi. | 401,404 |
| `REG-SHARED-001` | Cao | D | 2.11 Regression & Phạm vi ảnh hưởng | **BẮT BUỘC** với mọi release sửa code dùng chung hoặc fix bug **có thể tồn tại ở chức năng tương tự**. Dấu hiệu: "dùng chung" / "shared" / "component chung" / `共通`. | 408,411 |
| `REG-RUN-001` | Cao | D | 2.11 Regression & Phạm vi ảnh hưởng | **BẮT BUỘC** với mọi release khi hệ thống có job/dữ liệu đang chạy dở. | 413,416 |
| `REG-SPEC-001` | Cao | — | 2.11 Regression & Phạm vi ảnh hưởng | **BẮT BUỘC** với mọi thay đổi spec/requirement xảy ra **SAU** khi đã có test case (kể cả thay đổi nhỏ). | 418,421 |
| `REG-URL-001` ★ | Trung bình → BẮT BUỘC (nâng Cao) | D | 2.11 Regression & Phạm vi ảnh hưởng | khi CR chạm màn đăng ký / login / overview / thanh toán / kết nối bot | 423,429 |
| `SEC-001` | Cao | C | 2.12 Bảo mật | **BẮT BUỘC** khi chức năng chạm dữ liệu cá nhân khách hàng. | 433,436 |
| `SEC-002` | Cao | — | 2.12 Bảo mật | **BẮT BUỘC** khi chức năng xử lý credential / token / payment. | 438,441 |
| `SEC-ISO-001` | Cao | C | 2.12 Bảo mật | **BẮT BUỘC** khi UI tải/hiển thị **nhiều đối tượng dữ liệu đồng thời** (nhiều cuộc trò chuyện, nhiều tab). | 443,446 |
| `PERF-LARGE-001` | Trung bình (→ Cao với gửi tin / export / sync / phân tích) | D | 2.13 Hiệu năng & Dữ liệu lớn | mọi chức năng xử lý danh sách / khối lượng dữ liệu. Dấu hiệu spec: `大規模` / `大量` / `一括`. | 450,453 |
| `ENV-001` | Cao | D | 2.14 Hạ tầng & Môi trường | chức năng có bước validate quan trọng (slot, tồn kho, tiền) chạy qua nhiều server. | 457,460 |
| `ENV-002` | Trung bình | D | 2.14 Hạ tầng & Môi trường | release có đổi cấu hình hạ tầng (CDN / security rule) **kèm ngoại lệ** cần cấu hình riêng. | 462,465 |
| `ENV-003` ★ | Cao | D | 2.14 Hạ tầng & Môi trường | **BẮT BUỘC** khi tính năng chạm **media/file, URL/domain, job nền, thanh toán**, hoặc khi **thêm server mới**. **Không được đánh × với lý do "staging đã pass"** (RULE-08). | 467,477 |
| `JOB-001` ★ | Cao | D (+ D2) | 2.14 Hạ tầng & Môi trường | **BẮT BUỘC** khi tính năng thêm/sửa job nền, hoặc gọi API bên thứ 3 theo lô. × chỉ khi **hoàn toàn không có xử lý nền**. | 479,482 |
| `LIST-001` | Trung bình | B | 2.15 List & Thao tác hàng loạt | **BẮT BUỘC** với mọi màn danh sách có search/filter/pagination. | 486,489 |
| `BULK-001` | Cao | C | 2.15 List & Thao tác hàng loạt | **BẮT BUỘC** mỗi khi có tổ hợp **bộ lọc + thao tác hàng loạt** (gửi tin / gắn tag / đổi richmenu / đổi cấu hình). | 491,494 |
| `MEDIA-001` | Trung bình (→ Cao nếu output hiển thị cho khách cuối) | E | 2.16 Media / File | **BẮT BUỘC** khi chức năng có upload file/ảnh. | 498,501 |
| `MEDIA-CLEAN-001` ★ | Trung bình → BẮT BUỘC (nâng Cao) | E, D | 2.16 Media / File | khi chức năng cho phép **xóa hoặc thay thế** file/ảnh đã upload | 503,505 |
| `MEDIA-IMG-001` ★ | Trung bình → BẮT BUỘC (nâng Cao) | E, B | 2.16 Media / File | khi ảnh gửi ra phía LINE user hoặc dùng cho richmenu/imagemap | 507,509 |
| `FRIEND-001` | Cao | C | 2.17 Friend info | **BẮT BUỘC** khi chức năng đọc/ghi friend info hoặc dùng nó làm **điều kiện / biến**. | 513,517 |
| `DEPLOY-ASSET-001` ★ | Cao | D | 2.18 Release & Deploy | **BẮT BUỘC** khi release có sửa file JS/CSS/font/icon hoặc đổi cấu trúc dữ liệu mà GUI render. **Cao tuyệt đối** nếu file bị sửa nằm trong luồng **thanh toán / hủy hợp đồng**. | 521,524 |
| `DEPLOY-LIVE-001` ★ | Cao | D | 2.18 Release & Deploy | **BẮT BUỘC** với mọi release lên production **không bật maintain**, đặc biệt khi đổi **payload API / field form / cấu trúc request**. | 526,529 |
| `COMPAT-LEGACY-001` ★ | Cao | C, D | 2.18 Release & Deploy | **BẮT BUỘC** khi tính năng chạm template, form, remind, richmenu, google spread, hoặc **bất kỳ đối tượng nào đã từng version-up**. **Không được đánh × chỉ vì "dữ liệu mới chạy ổn"** (RULE-09). | 531,540 |

## Phân bố theo ưu tiên nền

> Đếm theo mức **nền**. `(→ Cao khi ...)` / `→ BẮT BUỘC (nâng Cao)` ở cột `Ưu tiên` là **điều kiện nâng lên Cao** — khớp điều kiện thì xử lý như quan điểm ưu tiên Cao (thiếu TC = `[BLOCKER]`, và RULE-01 bắt buộc đủ 3 loại case).

| Ưu tiên nền | Số quan điểm |
|---|---|
| Cao | 52 |
| Trung bình | 27 |
| Thấp | 1 |
