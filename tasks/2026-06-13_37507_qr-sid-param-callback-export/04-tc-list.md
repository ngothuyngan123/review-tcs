<!-- sync-target: https://docs.google.com/spreadsheets/d/15QEYkgp3OhzQyA5CLADvpQu_CAGovQIREuNjxPnBbOk/edit?gid=412698763#gid=412698763 -->

# 04 — TC List (fetched từ Redmine #37507 Link TCs)

> ⚠️ **Lưu ý cấu trúc:** Sheet nguồn (tab `Improve 1.0`) dùng cấu trúc TC **phân cấp** (Main Function → Sub1 → Sub2 → Sub3 → Sub4 → Sub5 → Expect Result → Actual Result → Status), **KHÔNG** phải bảng 10 cột chuẩn (TC ID / Title / Type / Priority / ...). Bảng dưới giữ NGUYÊN giá trị cell theo đúng cột của Sheet.
>
> - Cột `A` (Assignee), `B` (Main Function), `C` (Sub1) **trống** trong toàn dải `A2914:J2977` (merged cell từ row phía trên — thuộc nhóm "Quản lý qrlanding").
> - Cột `J` = `Support #37507` (cột status riêng cho ticket này), giá trị hiện tại đều là `Not test`.
> - Newline trong cell đã được chuyển thành `<br>` để hiển thị markdown.

## Thông tin

| Trường | Giá trị |
|---|---|
| Tester viết TCs | `<member điền sau khi review>` |
| Ngày submit | `<member điền sau khi review>` |
| Version TCs | `<member điền sau khi review>` |
| Link TC gốc | `https://docs.google.com/spreadsheets/d/15QEYkgp3OhzQyA5CLADvpQu_CAGovQIREuNjxPnBbOk/edit?gid=412698763#gid=412698763` (tab `Improve 1.0`, LINE 2914~2977, cột `Support #37507`) |

---

## TC List

| Sheet Row | Sub2 | Sub3 | Sub4 | Sub5 | Expect Result | Actual Result | Status (#37507) |
|---|---|---|---|---|---|---|---|
| 2914 | Check landing new friend | check khi add new friend | quét qr |  | - có call back vào Request Bin |  | Not test |
| 2915 |  |  | friend nhấn vào link qr |  |  |  | Not test |
| 2916 |  |  | check khi landing off |  |  |  | Not test |
| 2917 |  | check khi unblock | quét qr |  | - không call back vào Request Bin |  | Not test |
| 2918 |  |  | friend nhấn vào link qr |  |  |  | Not test |
| 2919 |  |  | check khi landing off |  |  |  | Not test |
| 2920 |  | check khi old friend | quét qr |  |  |  | Not test |
| 2921 |  |  | friend nhấn vào link qr |  |  |  | Not test |
| 2922 |  |  | check khi landing off |  |  |  | Not test |
| 2923 |  | check khi đang là friend | quét qr |  |  |  | Not test |
| 2924 |  |  | friend nhấn vào link qr |  |  |  | Not test |
| 2925 |  |  | check khi landing off |  |  |  | Not test |
| 2926 | Check landing all friend friend | check khi add new friend | quét qr |  | - có call back vào Request Bin |  | Not test |
| 2927 |  |  | friend nhấn vào link qr |  |  |  | Not test |
| 2928 |  |  | check khi landing off |  |  |  | Not test |
| 2929 |  | check khi unblock | quét qr |  |  |  | Not test |
| 2930 |  |  | friend nhấn vào link qr |  |  |  | Not test |
| 2931 |  |  | check khi landing off |  |  |  | Not test |
| 2932 |  | check khi old friend | quét qr |  |  |  | Not test |
| 2933 |  |  | friend nhấn vào link qr |  |  |  | Not test |
| 2934 |  |  | check khi landing off |  |  |  | Not test |
| 2935 |  | check khi đang là friend | quét qr |  |  |  | Not test |
| 2936 |  |  | friend nhấn vào link qr |  |  |  | Not test |
| 2937 |  |  | check khi landing off |  |  |  | Not test |
| 2938 | _[Annotation — Đánh giá ảnh hưởng Dev. Xem [03-dev-impact.md](03-dev-impact.md)]_ |  |  |  |  |  | Not test |
| 2939 | _[Annotation — Tái hiện case KH. Xem [01-bug-task.md](01-bug-task.md)]_ |  |  |  |  |  | Not test |
| 2940 | Check landing all friend<br>CÓ SETTING PARAM NGOÀI | không setting ucid={line_id}, {friend_type}, {friend_name}, {mail} hoặc {forward_param} | URL landing tự nhập thêm param | &sid=&lt;giá | - Tự động add all param ucid mặc định vào<br>- add thêm param admin tự nhập vào, hiển thị bên request bin |  | Not test |
| 2941 |  |  |  | &sid=YmlaNXEzZk1q&test=true |  |  | Not test |
| 2942 |  |  |  | &0 |  |  | Not test |
| 2943 |  |  |  | & dấu space |  |  | Not test |
| 2944 |  |  |  | &\` ~ ! @ # $ % ^ & ( ) + = _ " < > { } [] \|. , / *  \:? |  |  | Not test |
| 2945 |  |  |  | &・ー【】～！＠＃＄％＾＆＊（）「」｜￥；。→■∞ |  |  | Not test |
| 2946 |  |  |  | &まことボット智恵助 |  |  | Not test |
| 2947 |  |  |  | &AIボット🤖_Ver1 |  |  | Not test |
| 2948 |  |  |  | &こーだい/プレゼント専用🎁 |  |  | Not test |
| 2949 |  | có setting 1trong các ucid={line_id}, {friend_type}, {friend_name}, {mail} hoặc {forward_param} | URL landing tự nhập thêm param=> chỉ setting 1 trong các param | &sid=&lt;giá | - chỉ add param ucid setting tương ứng<br>- add thêm param admin tự nhập vào, hiển thị bên request bin |  | Not test |
| 2950 |  |  |  | &sid=YmlaNXEzZk1q&test=true |  |  | Not test |
| 2951 |  |  |  | &0 |  |  | Not test |
| 2952 |  |  |  | & dấu space |  |  | Not test |
| 2953 |  |  |  | &\` ~ ! @ # $ % ^ & ( ) + = _ " < > { } [] \|. , / *  \:? |  |  | Not test |
| 2954 |  |  |  | &・ー【】～！＠＃＄％＾＆＊（）「」｜￥；。→■∞ |  |  | Not test |
| 2955 |  |  |  | &まことボット智恵助 |  |  | Not test |
| 2956 |  |  |  | &AIボット🤖_Ver1 |  |  | Not test |
| 2957 |  |  |  | &こーだい/プレゼント専用🎁 |  |  | Not test |
| 2958 | Check landing cũ<br>KHÔNG SETTING PARAM NGOÀI | có setting ucid={line_id}, {friend_type}, {friend_name}, {mail} hoặc {forward_param} | check khi chỉ setting line_id | check case add new friend | - Không tự động add param thêm vào<br>- Call back ở url request bin chỉ có param được setting |  | Not test |
| 2959 |  |  |  | check case old friend |  |  | Not test |
| 2960 |  |  |  | check case unblock |  |  | Not test |
| 2961 |  |  |  | check case đang friend |  |  | Not test |
| 2962 |  |  | check khi chỉ setting friend_type | check case add new friend |  |  | Not test |
| 2963 |  |  |  | check case old friend |  |  | Not test |
| 2964 |  |  |  | check case unblock |  |  | Not test |
| 2965 |  |  |  | check case đang friend |  |  | Not test |
| 2966 |  |  | check khi chỉ setting friend_name | check case add new friend |  |  | Not test |
| 2967 |  |  |  | check case old friend |  |  | Not test |
| 2968 |  |  |  | check case unblock |  |  | Not test |
| 2969 |  |  |  | check case đang friend |  |  | Not test |
| 2970 |  |  |  | Check name tiếng Nhật có dấu cách, có emoji => Vẫn truyền param đúng lên callback |  |  | Not test |
| 2971 |  |  | check khi chỉ setting mail | check case add new friend |  |  | Not test |
| 2972 |  |  |  | check case old friend |  |  | Not test |
| 2973 |  |  |  | check case unblock |  |  | Not test |
| 2974 |  |  |  | check case đang friend |  |  | Not test |
| 2975 |  |  | check khi setting param[...] |  | - Không replace được |  | Not test |
| 2976 |  | Không setting 1 trong các param trên |  |  | - Tự động add all param vào |  | Not test |
| 2977 |  |  | Setting param custome | VD: &datatest = {続編にレディー・ガガ　サポート　スイカ　ソフトウェア　❤️❤️} | Truyền lên param datatest = 続編にレディー・ガガ　サポート　スイカ　ソフトウェア　❤️❤️❤️ | - nhập param text liền nhau+ icon có lưu vào được<br>- nhập text có dấu cách k phải định dạng URL không lưu vào dk | Not test |

---

## Member tự check trước khi submit

`<member điền sau khi review>`

<!-- Source: fetched từ Redmine #37507 Link TCs, range A2914:J2977 tab "Improve 1.0" lúc 2026-06-13. KHÔNG sửa TCs này nếu chưa confirm với Leader. -->
