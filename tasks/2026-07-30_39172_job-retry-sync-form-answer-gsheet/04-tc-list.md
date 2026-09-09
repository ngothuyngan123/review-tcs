# 04 — TC List (nguồn: lme-test-studio, task 39 — read-only)

> ⚠️ TC do **lme-test-studio** sinh (link ở journal Redmine #39172: `lme-test-studio.melonglobal.net/?screen=task-wizard&task=39&wtab=testcase`). Đã tự review (`[review-bổ-sung]`). File này là **index đã decode từ bản attach** (bản gốc mojibake UTF-8) để `/review-tc` bám coverage — **chi tiết đầy đủ (steps/expected/dữ liệu) ở lme-test-studio là bản authoritative**, không sửa ở đây.
>
> 観点 chuẩn LME: `FUNC-*`, `CONC-*`, `INTG-SHEET-*`, `JOB-*`, `REG-*`, `DATA-*`, `STATE-CLEAN-*`, `MSG-USER-*`, `ENV-*`, `COMPAT-LEGACY-*`, `FUNC-DATE/004`. Mã `TOOL-*` (TOOL-OLDREC/AXIS/NEGCTRL/APPENDANCHOR/ERRHYG) là taxonomy riêng của tool, **không có trong** `framework/checklist-lme.md`.

## Index 49 TC

| No. | 観点 | Loại | Tên case (rút gọn) | KQ | Chạy | Env | ⚠ |
|---|---|---|---|---|---|---|---|
| NEW-1 | TOOL-OLDREC-001 | Normal | Retry bản ghi cũ `result_error_google_id = NULL` | pass | auto | local/dev/stg | |
| NEW-2 | TOOL-OLDREC-001 | Normal | Retry bản ghi cũ `result_error_google_id != NULL` | pass | auto | | |
| NEW-11 | TOOL-OLDREC-001 | Normal | **TC TRUNG TÂM** — bản ghi lỗi đời cũ chưa có ID retry → phải kết thúc, không treo | pass | auto | local/dev/stg | ⚠ finding |
| NEW-12 | TOOL-OLDREC-001 | Normal | Bản ghi đời mới đã có ID retry → đồng bộ lại + đóng (mốc so sánh, RULE-09) | pass | auto | local/dev/stg | |
| NEW-3 | INTG-SHEET-001 | Normal | Retry xóa dữ liệu Google Sheet | pass | auto | | |
| NEW-13 | TOOL-AXIS-001 | Normal | Retry luồng XÓA → reset đúng cột trạng thái xóa | pass | auto | local/dev/stg | |
| NEW-14 | DATA-REF-001 | Normal | Câu trả lời gốc đã xóa → đóng bản ghi lỗi ngay | pass | auto | local/dev/stg | |
| NEW-15 | JOB-001 | Normal | Retry đồng loạt nhiều bản ghi/nhiều biểu mẫu → đếm vào/ra (thay NEW-7) | pass | auto | local/dev/stg | |
| NEW-16 | TOOL-NEGCTRL-001 | Normal | Đối chứng âm: bản ghi salon/lesson không bị job form answer chạm | pass | auto | local/dev/stg | |
| NEW-17 | DATA-DB-001 | Normal | Đối chứng âm: retry 1 bản ghi không đổi trạng thái câu trả lời khác (2 bot trùng tên) | pass | auto | local/dev/stg | |
| NEW-4 | CONC-001 | Normal | Cập nhật đồng thời status + result_error_google_id (atomic) | pass | auto | | |
| NEW-5 | CONC-001 | Normal | ResultErrorGoogle = RUNNING **trước** khi reset về NEW | pass | auto | | |
| NEW-9 | REG-SHARED-001 | Normal | Chức năng sync mới không bị ảnh hưởng | pass | auto | | |
| NEW-10 | REG-SHARED-001 | Normal | Chức năng delete mới không bị ảnh hưởng | pass | auto | | |
| NEW-48 | REG-SHARED-001 | Normal | Lệnh xử lý lỗi Google phía **web** phải bỏ qua bản ghi form answer (bảng dùng chung) | blocked | auto | local/dev/stg | ⚠ |
| NEW-37 | COMPAT-LEGACY-001 | Normal | Retry ghi sheet header đời cũ + đời mới → đúng cột (RULE-09, MAP-GS-07) | pass | manual | local/dev/stg | |
| NEW-39 | TOOL-AXIS-001 | Normal | Retry biểu mẫu nhiều trang → tiếp từ đúng trang lỗi, không trùng | pass | manual | local/dev/stg | |
| NEW-43 | TOOL-APPENDANCHOR-001 | Normal | (Static) Ghi thêm dòng luôn neo ô đích đúng sheet | pass | auto | Tất cả | |
| NEW-45 | ENV-003 | Normal | Verify lại trên **production** (job tách tiến trình) | *(chưa chạy)* | manual | **prd** | ⚠ |
| NEW-46 | DATA-MIG-001 | Normal | (Static) Cột ID retry / status nullable → thống kê lượng bản ghi cũ trống (migration 2026-03-30) | skip | auto | Tất cả | |
| NEW-18 | FUNC-001 | Abnormal | Bản ghi đang "đang xử lý" (treo từ trước) → job không tự nhặt (selectListNeedRun chỉ lấy status 0) | pass | auto | local/dev/stg | |
| NEW-19 | FUNC-001 | Abnormal | Câu trả lời đang dở luồng xóa → job bỏ qua nhưng không được treo | **blocked** | auto | local/dev/stg | ⚠ pending |
| NEW-25 | FUNC-001 | Abnormal | Biểu mẫu đã xóa / hủy liên kết sheet → đánh dấu bỏ qua + đóng (nhánh fix 6065e70b sửa) | pass | auto | local/dev/stg | |
| NEW-28 | FUNC-001 | Abnormal | Bot mất liên kết Google → bỏ qua + đóng (+SEC-002 không lộ token) | pass | auto | local/dev/stg | |
| NEW-26 | STATE-CLEAN-001 | Abnormal | Bot đã xóa → bỏ qua + đóng | pass | auto | local/dev/stg | |
| NEW-27 | STATE-CLEAN-001 | Abnormal | Hợp đồng bot hết hạn >7 ngày → bỏ qua + đóng | pass | auto | local/dev/stg | |
| NEW-30 | STATE-CLEAN-001 | Abnormal | Luồng XÓA khi bot hết hạn / mất liên kết → bỏ qua + đóng | pass | auto | local/dev/stg | |
| NEW-31 | DATA-REF-001 | Abnormal | Luồng XÓA khi biểu mẫu/liên kết không còn → bỏ qua + đóng | pass | auto | local/dev/stg | |
| NEW-29 | MSG-USER-001 | Abnormal | LINE user của câu trả lời cũ đã xóa → bỏ qua bản ghi, không treo | pass | auto | local/dev/stg | ⚠ pending |
| NEW-20 | CONC-001 | Abnormal | Song song job retry + job ghi sheet → mỗi câu trả lời 1 dòng (thay NEW-8) | pass | auto | local/dev/stg | |
| NEW-8 | CONC-001 | Abnormal | Xử lý đồng thời (bị thay bởi NEW-20) | pass | auto | | |
| NEW-21 | REG-RUN-001 | Abnormal | Job restart giữa lúc retry → tự hồi phục, không treo/nhân đôi | **blocked** | manual | local/dev/stg | |
| NEW-44 | REG-RUN-001 | Abnormal | Phát hành khi job đang chạy dở → không mất/trùng | *(chưa chạy)* | manual | staging/prd | ⚠ |
| NEW-32 | TOOL-ERRHYG-001 | Abnormal | Lỗi bất thường lúc SYNC → đóng bản ghi ở "thất bại", không treo | pass | auto | local/dev/stg | |
| NEW-33 | TOOL-ERRHYG-001 | Abnormal | Lỗi bất thường lúc XÓA → đóng "thất bại", không treo | pass | auto | local/dev/stg | |
| NEW-34 | JOB-001 | Abnormal | Google trả lỗi tạm thời → tăng retry + hẹn lại backoff (thay NEW-6) | pass | auto | local/dev/stg | |
| NEW-6 | JOB-001 | Abnormal | Sync tiếp tục thất bại (bị thay bởi NEW-34) | pass | auto | | |
| NEW-35 | INTG-SHEET-001 | Abnormal | Google lỗi vĩnh viễn → thất bại ngay, không retry tiếp (3 biến thể) | pass | auto | local/dev/stg | |
| NEW-36 | INTG-SHEET-001 | Abnormal | Google lỗi xác thực → hạ trạng thái liên kết bot + thất bại | pass | auto | local/dev/stg | |
| NEW-38 | INTG-SHEET-001 | Abnormal | User sửa/xóa cột mã câu trả lời trên sheet → không ghi lệch cột | pass | manual | local/dev/stg | |
| NEW-40 | DATA-REF-001 | Abnormal | Trang bị lỗi đã xóa khỏi biểu mẫu → chạy lại từ trang đầu | pass | manual | local/dev/stg | |
| NEW-41 | DATA-DB-001 | Abnormal | Retry xóa nhiều dòng cùng biểu mẫu → xóa đúng dòng, không lệch | pass | manual | local/dev/stg | |
| NEW-42 | CONC-002 | Abnormal | Sheet đích rỗng, retry ghi lại toàn bộ cũ + có câu trả lời mới giữa chừng | pass | manual | local/dev/stg | |
| NEW-49 | OUT-TRUTH-001 | Normal | (UI) Sau lỗi xác thực Google, màn cài đặt liên kết hiện cảnh báo liên kết lại | pass | manual | local/dev/stg | |
| NEW-23 | FUNC-DATE-001 | Boundary | Mốc hẹn retry: quá khứ / hiện tại / tương lai / **NULL** | pass | auto | local/dev/stg | ⚠ finding |
| NEW-24 | FUNC-004 | Boundary | Số lần retry biên 4 và 5 (ngưỡng từ code, chưa có spec) | pass | auto | local/dev/stg | |
| NEW-22 | ENV-003 | Abnormal | (Static) Xác nhận nơi đăng ký/khởi động job retry | pass | auto | Tất cả | ⚠ pending |
| NEW-47 | DATA-MIG-001 | Abnormal | Bản ghi treo "đang xử lý" tồn đọng trước phát hành → **cần phương án dọn** | skip | auto | local/dev/stg | ⚠ finding |

<!-- Source: attach của user (39172.md, mojibake UTF-8), nguồn gốc lme-test-studio task 39. Decode 2026-07-30. Chi tiết steps/expected đầy đủ ở lme-test-studio — file này chỉ index để review coverage. KHÔNG sửa TC. -->
