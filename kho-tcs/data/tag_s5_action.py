# -*- coding: utf-8 -*-
"""FA-012 — Nhóm 11: Action gắn tag (action khi gắn + action khi bị limit).

Liệt kê ĐẦY ĐỦ 24 điểm gắn tag cho friend của WEB và JOB + 2 luồng CSV.
Nguồn danh sách điểm gắn tag: r122-r135 (khối 'Check job gắn tag') và
r380-r613 (khối 'Check triển khai ngang cho add tag phía web').

Quyết định MT-09 (2026-08-19): GIỮ NGUYÊN hành vi hiện tại — 6 điểm KHÔNG gửi
action dù tag đặt「何度でも」, ghi ngoại lệ vào BR-07.
"""
from _common import tc

BOT = "- Đăng nhập admin, đang chọn bot A\n- Màn hình /basic/tag"

PRE_MATRIX = (
    "- Tag「MatrixMany」: is_2th_apply=1 (何度でも), có 1 action send text「行動確認」, KHÔNG set limit\n"
    "- Friend F ĐÃ có sẵn bản ghi tag_line_user với tag này (đã được gắn tag từ trước)\n"
    "- Chuẩn bị sẵn LINE app thật của Friend F để kiểm tra tin nhận"
)

# 24 điểm gắn tag: (nhóm, tên điểm, các bước riêng, có gửi action?, nguồn)
POINTS = [
    ("WEB", "Chat 1:1 — right bar「クイック操作」",
     "1. Mở màn chat 1:1, chọn Friend F\n2. Ở right bar bấm「クイック操作」\n3. Tick chọn tag「MatrixMany」\n4. Bấm「保存」",
     False, "r386 (TC gốc ghi rõ 'logic từ trước')"),
    ("WEB", "Chat 1:1 — right bar icon ... → modal edit tag",
     "1. Mở màn chat 1:1, chọn Friend F\n2. Ở right bar bấm icon ... → mở modal edit tag\n3. Tick chọn tag「MatrixMany」\n4. Bấm save",
     False, "r407"),
    ("WEB", "Chat 1:1 — tick avatar friend ở left bar → modal quick action",
     "1. Mở màn chat 1:1\n2. Ở left bar, tick chọn avatar của Friend F\n3. Modal quick action mở ra → chọn add tag\n4. Chọn tag「MatrixMany」→ xác nhận",
     True, "r428"),
    ("WEB", "Chat 1:1 — multi action từ ô chat (center bar)",
     "1. Mở màn chat 1:1 của Friend F\n2. Ở ô chat (center bar) mở modal multi action\n3. Thêm action gắn tag「MatrixMany」\n4. Thực hiện gửi",
     True, "r449"),
    ("WEB", "Friendlist — multi action",
     "1. Mở màn friendlist\n2. Tick chọn Friend F\n3. Mở modal multi action → thêm action gắn tag「MatrixMany」\n4. Thực hiện",
     True, "r471"),
    ("WEB", "My page (web)",
     "1. Mở màn my page của Friend F\n2. Tick chọn tag「MatrixMany」\n3. Bấm save\n4. Xác nhận tag đã hiển thị ở danh sách tag của F",
     False, "r493"),
    ("APP", "App mobile — chat 1:1, icon edit tag cạnh ô nhập message",
     "1. Mở app mobile, vào chat 1:1 của Friend F\n2. Bấm icon edit tag cạnh ô nhập message\n3. Bấm button edit tag → chọn tag「MatrixMany」\n4. Bấm save",
     False, "r515"),
    ("APP", "App mobile — my page, button add tag",
     "1. Mở app mobile, vào màn my page của Friend F\n2. Bấm button add tag\n3. Tick chọn tag「MatrixMany」\n4. Bấm add tag",
     False, "r536"),
    ("FORM", "Form answer — item RADIO có map tag",
     "1. Tạo form có item radio map tới tag「MatrixMany」\n2. Friend F mở form bằng LINE\n3. Chọn option đã map tag\n4. Submit form",
     True, "r558"),
    ("FORM", "Form answer — item DROPDOWN có map tag",
     "1. Tạo form có item dropdown map tới tag「MatrixMany」\n2. Friend F mở form bằng LINE\n3. Chọn option đã map tag\n4. Submit form",
     True, "r577"),
    ("FORM", "Form answer — item CHECKBOX có map tag",
     "1. Tạo form có item checkbox map tới tag「MatrixMany」\n2. Friend F mở form bằng LINE\n3. Tick option đã map tag\n4. Submit form",
     True, "r596"),
    ("JOB-callback", "Setting kết bạn thường (màn setting add friend)",
     "1. Vào màn setting kết bạn, thêm action gắn tag「MatrixMany」→ lưu\n2. Friend F block rồi kết bạn lại với bot (hoặc dùng friend mới đã có tag)\n3. Chờ callback xử lý xong\n4. Kiểm tra log callback",
     True, "r122, r326"),
    ("JOB-callback", "Template button",
     "1. Tạo template dạng button, gán action gắn tag「MatrixMany」cho 1 button\n2. Gửi template cho Friend F\n3. Friend F bấm button đó trên LINE\n4. Chờ callback xử lý",
     True, "r123, r326"),
    ("JOB-callback", "Template Image map",
     "1. Tạo template image map, gán action gắn tag「MatrixMany」cho 1 vùng\n2. Gửi template cho Friend F\n3. Friend F bấm vùng đó trên LINE\n4. Chờ callback xử lý",
     True, "r124, r326"),
    ("JOB-callback", "Rich menu",
     "1. Tạo rich menu có vùng gắn action tag「MatrixMany」→ áp dụng cho Friend F\n2. Friend F bấm vùng đó trên LINE\n3. Chờ callback xử lý",
     True, "r125, r326"),
    ("JOB-callback", "Auto reply",
     "1. Tạo auto reply có action gắn tag「MatrixMany」\n2. Friend F gửi keyword khớp điều kiện auto reply\n3. Chờ callback xử lý",
     True, "r126, r326"),
    ("JOB-action", "Action schedule",
     "1. Tạo action schedule có action gắn tag「MatrixMany」\n2. Đặt điều kiện lọc bao gồm Friend F\n3. Chờ/kích hoạt job action schedule chạy\n4. Kiểm tra log job đã xử lý F",
     True, "r127, r320"),
    ("JOB-action", "Action CỦA TAG khác (tag → tag)",
     "1. Tạo tag「Trigger」có action gắn tag「MatrixMany」\n2. Gắn tag「Trigger」cho Friend F\n3. Chờ job xử lý action chuỗi",
     True, "r128, r329"),
    ("JOB-action", "Action của Scenario (ステップ配信)",
     "1. Tạo scenario có step chứa action gắn tag「MatrixMany」\n2. Đưa Friend F vào scenario\n3. Chờ step chạy tới",
     True, "r129, r329"),
    ("JOB-action", "Action của Broadcast (gửi tin hàng loạt)",
     "1. Tạo broadcast có action gắn tag「MatrixMany」\n2. Đặt filter bao gồm Friend F\n3. Gửi broadcast, chờ job xử lý xong",
     True, "r130, r329"),
    ("JOB-action", "Action của Remind (remind booking / form mới)",
     "1. Tạo remind (của booking hoặc form) có action gắn tag「MatrixMany」\n2. Tạo điều kiện để remind kích hoạt cho Friend F\n3. Chờ job remind chạy",
     True, "r131, r329"),
    ("JOB-action", "Action của Form (sau khi submit form)",
     "1. Tạo form có action sau submit gắn tag「MatrixMany」\n2. Friend F submit form\n3. Chờ job xử lý",
     True, "r132, r329"),
    ("JOB-action", "Action của Booking (salon / lesson calendar)",
     "1. Tạo booking calendar có action gắn tag「MatrixMany」\n2. Friend F đặt lịch\n3. Chờ job xử lý",
     True, "r133, r329"),
    ("JOB-action", "Action của Item (bán sản phẩm)",
     "1. Tạo sản phẩm có action gắn tag「MatrixMany」sau khi mua\n2. Friend F mua sản phẩm\n3. Chờ job xử lý",
     True, "r134, r329"),
]


def _matrix(idx, group, name, steps, has_action, src):
    verdict = ("Friend F NHẬN được text「行動確認」trên LINE app THẬT"
               if has_action else
               "Friend F KHÔNG nhận được text「行動確認」trên LINE app")
    extra = ("" if has_action else
             "\n- Đây là NGOẠI LỆ của BR-07 đã được Leader chấp nhận (MT-09) — KHÔNG raise bug")
    env = "PRODUCTION" if group.startswith("JOB") else "STAGING"
    return tc("Action gắn tag", "MSG-001", "Normal" if has_action else "Abnormal",
              f"Điểm gắn tag {idx}/24 [{group}] {name} — tag 何度でも + user ĐÃ có tag → "
              + ("CÓ gửi action" if has_action else "KHÔNG gửi action (ngoại lệ BR-07)"),
              PRE_MATRIX,
              steps + "\n5. Mở LINE app của Friend F kiểm tra có nhận text「行動確認」không\n"
                      "6. Query tag_line_user WHERE tag_id AND line_user_id=F\n"
                      "7. Query tags.count_user_tag",
              "Tag「MatrixMany」(何度でも, action send text「行動確認」)\nFriend F đã có tag từ trước",
              f"- {verdict}\n- tag_line_user KHÔNG thêm bản ghi trùng (user đã có tag)\n"
              f"- count_user_tag KHÔNG tăng{extra}",
              env=env, spec="Đã hỏi leader",
              note=f"Leader chốt MT-09 (2026-08-19): GIỮ NGUYÊN hành vi, ghi ngoại lệ vào BR-07. "
                   f"RULE-06: verify tại LINE app thật. "
                   + ("RULE-08: job/callback phải kết luận từ production. " if group.startswith("JOB") else "")
                   + f"Evidence: ảnh màn hình LINE của F. Nguồn: {src}")


S5 = [
    # ═══════ Quy tắc action mode (nền tảng cho ma trận) ═══════
    tc("Action gắn tag", "MSG-001", "Normal",
       "BR-07 mode「1度のみ」(1/2): gắn tag LẦN ĐẦU cho user chưa từng có tag → CÓ gửi action",
       BOT + "\n- Tag「ActionOnce」: is_2th_apply=0, có 1 action send text「テスト送信」\n- Friend F CHƯA từng có bản ghi tag_line_user với tag này",
       "1. Gắn tag cho F từ màn chat 1:1\n2. Mở LINE app của F kiểm tra tin nhận\n3. Query tag_line_user",
       "Friend F chưa từng có tag; tag mode 1度のみ",
       "- F NHẬN được text「テスト送信」trên LINE app THẬT\n- DB: tag_line_user có bản ghi mới cho F\n- count_user_tag tăng 1",
       note="BR-07. RULE-06. Evidence: ảnh màn hình LINE. Nguồn: r319, r192"),

    tc("Action gắn tag", "MSG-001", "Abnormal",
       "BR-07 mode「1度のみ」(2/2): gỡ tag rồi GẮN LẠI cho user đã từng có tag → KHÔNG gửi action",
       BOT + "\n- Tag「ActionOnce」: is_2th_apply=0, có 1 action send text\n- Friend F đã từng được gắn rồi gỡ tag này",
       "1. Xác nhận F đang KHÔNG có tag nhưng đã từng có\n2. Gắn lại tag cho F\n3. Mở LINE app của F kiểm tra\n4. Query tag_line_user",
       "Friend F đã từng có tag; tag mode 1度のみ",
       "- F KHÔNG nhận thêm tin nào trên LINE app\n- DB: tag_line_user có bản ghi mới (tag VẪN được gắn)\n- Chỉ action bị chặn, không phải việc gắn tag",
       note="BR-07. RULE-06. Nguồn: r319, r192"),

    tc("Action gắn tag", "MSG-001", "Normal",
       "BR-07 mode「何度でも」: gắn tag lần đầu cho user chưa có tag → CÓ gửi action",
       BOT + "\n- Tag「ActionMany」: is_2th_apply=1, có 1 action send text\n- Friend F chưa từng có tag này",
       "1. Chạy action schedule gắn tag cho F\n2. Mở LINE app của F kiểm tra\n3. Query tag_line_user",
       "Friend F chưa có tag; tag mode 何度でも",
       "- F NHẬN được tin trên LINE app\n- DB: tag_line_user có bản ghi mới",
       note="BR-07. RULE-06. Nguồn: r320, r193"),
]

# ═══════ 24 TC ma trận điểm gắn tag ═══════
S5 += [_matrix(i, g, n, s, a, src) for i, (g, n, s, a, src) in enumerate(POINTS, start=1)]

S5 += [
    # ═══════ 2 luồng CSV (MT-13) ═══════
    tc("Action gắn tag", "MSG-001", "Normal",
       "Luồng CSV 1/3: CSV一括追加 ở /basic/tag chỉ TẠO TAG, không gắn cho friend nên không có action",
       BOT + "\n- File CSV chứa 3 tên tag mới\n- Các tag này sẽ có action sau khi tạo",
       "1. Vào /basic/tag → CSV一括追加 → import file\n2. Kiểm tra 3 tag được tạo\n3. Query tag_line_user WHERE tag_id IN (3 tag mới)\n4. Kiểm tra có friend nào nhận tin không",
       "3 tên tag mới trong CSV",
       "- 3 tag được TẠO ở màn list tag\n- tag_line_user: 0 bản ghi (luồng này KHÔNG gắn tag cho friend)\n- KHÔNG friend nào nhận tin\n- Đây là luồng tạo tag, khác hoàn toàn luồng gắn tag cho friend",
       spec="Đã hỏi leader",
       note="Leader chốt MT-13 (2026-08-19): import CSV ở màn quản lý tag KHÔNG send action, chỉ insert tag. ⚠️ SPEC CẦN SỬA: ghi rõ vào luồng EP-31. Nguồn: r292-r295"),

    tc("Action gắn tag", "MSG-001", "Normal",
       "Luồng CSV 2/3: import ở /basic/csv-management với option action BẬT → CÓ gửi action",
       BOT + "\n- Tag「CsvAction」có action send text「CSV確認」, is_2th_apply=0\n- File CSV gắn tag này cho 3 friend CHƯA có tag\n- 3 friend đều có LINE app thật để kiểm tra",
       "1. Vào /basic/csv-management → import file\n2. Ở option gửi action → chọn CÓ\n3. Thực hiện import, chờ xử lý xong\n4. Mở LINE app của cả 3 friend\n5. Query tag_line_user và tags.count_user_tag",
       "3 friend chưa có tag; option action = BẬT",
       "- Cả 3 friend được gắn tag (tag_line_user +3, count_user_tag +3)\n- Cả 3 friend NHẬN được text「CSV確認」trên LINE app THẬT\n- Option BẬT hoạt động đúng",
       env="PRODUCTION", spec="Đã hỏi leader",
       note="Leader chốt MT-13: màn quản lý CSV CÓ option chọn có action hay không. ⚠️ Option này CHƯA có trong spec FA-012 lẫn spec Quản lý CSV → cần bổ sung. RULE-06 + RULE-08. Nguồn: quyết định MT-13"),

    tc("Action gắn tag", "MSG-001", "Abnormal",
       "Luồng CSV 3/3: import ở /basic/csv-management với option action TẮT → gắn tag nhưng KHÔNG gửi action",
       BOT + "\n- Tag「CsvAction」có action send text「CSV確認」\n- File CSV gắn tag này cho 3 friend CHƯA có tag",
       "1. Vào /basic/csv-management → import file\n2. Ở option gửi action → chọn KHÔNG\n3. Thực hiện import, chờ xử lý xong\n4. Mở LINE app của cả 3 friend\n5. Query tag_line_user và tags.count_user_tag\n6. Lặp lại với tag ở mode 何度でも",
       "3 friend chưa có tag; option action = TẮT; test cả 2 mode 1度のみ và 何度でも",
       "- Cả 3 friend ĐƯỢC gắn tag (tag_line_user +3, count_user_tag +3)\n- KHÔNG friend nào nhận tin trên LINE app\n- Kết quả GIỐNG NHAU ở cả 2 mode action",
       env="PRODUCTION", spec="Đã hỏi leader",
       note="Leader chốt MT-13. Nguồn: r322-r323, r346-r347 + quyết định MT-13"),

    # ═══════ Action khi bị LIMIT ═══════
    tc("Action gắn tag", "PAY-LIMIT-001", "Abnormal",
       "Limit enforcement: tag ĐÃ đạt limit → KHÔNG điểm gắn tag nào trong 24 điểm gắn thêm được",
       BOT + "\n- Tag「LimitAll」: is_limit=1, limit=1, count_user_tag=1 (đã đầy)\n- Friend F chưa có tag này",
       "Với TỪNG điểm trong 24 điểm gắn tag (xem cột Dữ liệu test):\n1. Thử gắn tag「LimitAll」cho Friend F\n2. Query tag_line_user WHERE tag_id AND line_user_id=F\n3. Query tags.count_user_tag\n4. Ghi lại điểm nào (nếu có) lọt qua được limit",
       "24 điểm: WEB (chat 1:1 ×4, friendlist, my page) · APP (chat 1:1, my page) · "
       "FORM (radio, dropdown, checkbox) · JOB-callback (kết bạn, template button, image map, "
       "rich menu, auto reply) · JOB-action (schedule, tag, scenario, broadcast, remind, form, booking, item)",
       "- CẢ 24 điểm: F KHÔNG được gắn tag\n- tag_line_user không có bản ghi mới cho F\n- tags.count_user_tag giữ nguyên = 1 ở mọi lần thử\n- Điểm nào bypass được limit → BUG, raise ticket ngay",
       env="PRODUCTION",
       note="BR-05. 24 điểm CÙNG 1 kết quả nên giữ chung 1 TC (khác ma trận action MT-09 vốn có kết quả khác nhau). RULE-08. Nguồn: r331, r343, r353, r365, r388, r409, r430, r451, r473, r495, r517, r538, r560, r579, r598"),

    tc("Action gắn tag", "STATE-DEP-001", "Normal",
       "Limit action 1/4: mode「1度のみ」, user CHƯA có bản ghi action_limit_tags → CÓ gửi + INSERT record",
       BOT + "\n- Tag「LimitAct」: is_limit=1, limit=1, count_user_tag=1 (đã đầy)\n- Tab 人数制限 có limit action = send text「上限に達しました」, limit_action_mode = 0 (1度のみ)\n- Friend F chưa có bản ghi action_limit_tags với tag này",
       "1. Gắn tag cho Friend F\n2. Mở LINE app của F kiểm tra\n3. Query action_limit_tags WHERE tag_id AND line_user_id=F\n4. Query tag_line_user",
       "F chưa có record action_limit_tags; mode 1度のみ",
       "- F NHẬN text「上限に達しました」trên LINE app THẬT\n- DB: INSERT 1 bản ghi action_limit_tags\n- F KHÔNG được gắn tag (tag_line_user không tăng)",
       note="BR-05 + BR-06. RULE-06. Evidence: ảnh LINE + query action_limit_tags. Nguồn: r338"),

    tc("Action gắn tag", "STATE-DEP-001", "Abnormal",
       "Limit action 2/4: mode「1度のみ」, user ĐÃ có bản ghi action_limit_tags → KHÔNG gửi, KHÔNG thêm record",
       BOT + "\n- Như TC trên nhưng Friend F ĐÃ có 1 bản ghi action_limit_tags\n- limit_action_mode = 0",
       "1. Gắn tag cho Friend F lần 2\n2. Mở LINE app của F kiểm tra\n3. Query COUNT action_limit_tags WHERE tag_id AND line_user_id=F",
       "F đã có record action_limit_tags; mode 1度のみ",
       "- F KHÔNG nhận thêm tin nào\n- DB: COUNT action_limit_tags vẫn = 1 (không thêm)\n- F vẫn KHÔNG được gắn tag",
       note="BR-06: limit_action_mode=0 chỉ trigger 1 lần/user. Nguồn: r339"),

    tc("Action gắn tag", "STATE-DEP-001", "Normal",
       "Limit action 3/4: mode「何度でも」, user CHƯA có bản ghi action_limit_tags → CÓ gửi + INSERT record",
       BOT + "\n- Tag「LimitAct2」: is_limit=1 đã đầy, limit action send text, limit_action_mode = 1 (何度でも)\n- Friend G chưa có bản ghi action_limit_tags",
       "1. Gắn tag cho Friend G\n2. Mở LINE app của G kiểm tra\n3. Query action_limit_tags WHERE tag_id AND line_user_id=G",
       "G chưa có record; mode 何度でも",
       "- G NHẬN được text limit trên LINE app\n- DB: INSERT 1 bản ghi action_limit_tags\n- G KHÔNG được gắn tag",
       note="BR-06. Nguồn: r340"),

    tc("Action gắn tag", "STATE-DEP-001", "Normal",
       "Limit action 4/4: mode「何度でも」, user ĐÃ có bản ghi action_limit_tags → VẪN gửi nhưng KHÔNG thêm record",
       BOT + "\n- Như TC trên nhưng Friend G ĐÃ có 1 bản ghi action_limit_tags\n- limit_action_mode = 1",
       "1. Gắn tag cho Friend G lần 2\n2. Mở LINE app của G kiểm tra\n3. Query COUNT action_limit_tags WHERE tag_id AND line_user_id=G",
       "G đã có record; mode 何度でも",
       "- G VẪN NHẬN được text limit (khác mode 1度のみ)\n- DB: COUNT action_limit_tags vẫn = 1 (KHÔNG thêm record mới)\n- G vẫn KHÔNG được gắn tag",
       note="BR-06: mode 何度でも vẫn gửi nhưng không nhân bản record tracking. Nguồn: r341"),

    # ═══════ Race condition khi limit ═══════
    tc("Action gắn tag", "CONC-001", "Boundary",
       "Bug #31703: action schedule đa luồng gắn tag có limit → KHÔNG được vượt quá limit",
       BOT + "\n- Tag「LimitRace」: is_limit=1, limit=2, count_user_tag=0\n- Action schedule gắn tag này cho 5 friend, cả 5 đều CHƯA có tag\n- Job action schedule chạy đa luồng",
       "1. Kích hoạt action schedule cho 5 friend cùng lúc\n2. Chờ job xử lý xong\n3. Query COUNT(tag_line_user WHERE tag_id) và tags.count_user_tag\n4. Kiểm tra 3 friend còn lại\n5. Lặp lại test 3 lần để loại trừ may rủi",
       "limit = 2, action cho 5 user cùng lúc",
       "- ĐÚNG 2 friend được gắn tag (không phải 3, 4 hay 5)\n- tags.count_user_tag = 2, khớp COUNT(tag_line_user) = 2\n- 3 friend còn lại KHÔNG có tag\n- Cột 人数制限 hiển thị「2/2 人（上限到達）」màu đỏ\n- Lặp 3 lần đều cho kết quả giống nhau",
       env="PRODUCTION",
       note="Bug #31703 [06-09-2025] — root cause: đa luồng action cùng lúc vượt limit; fix = xử lý đồng bộ khi tag có limit. RULE-08. Evidence: query DB + log job. Nguồn: r330-r332"),

    tc("Action gắn tag", "CONC-001", "Boundary",
       "Limit race: remain limit = 1, action cho 3 user trong đó 1 user ĐÃ có tag từ trước",
       BOT + "\n- Tag「LimitMix」: is_limit=1, limit=3, count_user_tag=2 (remain = 1), is_2th_apply=1\n- User1 đã có tag; User2, User3 chưa có",
       "1. Chạy action schedule gắn tag cho cả User1, User2, User3\n2. Kiểm tra LINE app của 3 user\n3. Query tag_line_user, tags.count_user_tag, action_limit_tags",
       "remain=1; User1 có tag, User2/User3 chưa",
       "- User1: KHÔNG thêm bản ghi tag_line_user mới, NHƯNG vẫn gửi action add tag (do 何度でも)\n- User2: được gắn tag mới + gửi action add tag\n- User3: KHÔNG được gắn tag → gửi action LIMIT + thêm bản ghi action_limit_tags\n- tags.count_user_tag = 3 (đạt limit)",
       env="PRODUCTION",
       note="Nguồn: r333, r345, r355, r367"),

    tc("Action gắn tag", "CONC-001", "Boundary",
       "Limit race qua CALLBACK: 2 user cùng bấm action lúc remain limit = 1",
       BOT + "\n- Tag「LimitCb」: is_limit=1, limit=1, count_user_tag=0\n- Action gắn tag đặt ở rich menu (callback)\n- User1 và User2 đều chưa có tag",
       "1. Cho User1 và User2 bấm rich menu GẦN NHƯ ĐỒNG THỜI\n2. Chờ callback xử lý xong\n3. Query tag_line_user và tags.count_user_tag\n4. Kiểm tra LINE app của cả 2\n5. Lặp lại 3 lần",
       "limit = 1, 2 user bấm cùng lúc qua callback",
       "- ĐÚNG 1 user được gắn tag\n- User còn lại KHÔNG được gắn, nhận limit action (nếu có setting)\n- count_user_tag = 1, khớp COUNT(tag_line_user)\n- Lặp 3 lần đều đúng",
       env="PRODUCTION",
       note="Bug #31703 áp cho nhánh callback. RULE-08. Nguồn: r354-r355"),

    # ═══════ Action gắn nhiều tag ═══════
    tc("Action gắn tag", "FUNC-MULTI-001", "Normal",
       "Action gắn NHIỀU tag: trộn tag không limit / limit chưa đầy / limit đã đầy",
       BOT + "\n- 1 action detail type=tag chứa 3 tag: TagFree (không limit), TagOk (limit 10, count 0), TagFull (limit 1, count 1 — đã đầy)\n- Friend F chưa có tag nào",
       "1. Kích hoạt action cho Friend F\n2. Query tag_line_user của F\n3. Kiểm tra LINE app của F",
       "3 tag trong 1 action, Friend F",
       "- F được gắn TagFree và TagOk\n- F KHÔNG được gắn TagFull\n- TagFull gửi limit action (nếu có setting)\n- Các tag còn lại không bị ảnh hưởng bởi tag bị limit",
       note="Nguồn: r376-r378"),

    tc("Action gắn tag", "STATE-DEP-001", "Abnormal",
       "Action gắn nhiều tag: 1 trong các tag bị XOÁ sau khi action đã tạo → bỏ qua tag đó",
       BOT + "\n- 1 action detail chứa 3 tag: TagA, TagB (sẽ bị xoá), TagC\n- Friend G chưa có tag nào",
       "1. Xoá TagB ở màn list tag\n2. Kích hoạt action cho Friend G\n3. Query tag_line_user của G\n4. Query t_actions_detail xem id TagB còn không",
       "3 tag, TagB bị xoá",
       "- G được gắn TagA và TagC\n- G KHÔNG được gắn TagB\n- DB: id của TagB đã bị gỡ khỏi t_actions_detail\n- Tag có setting limit trong nhóm vẫn apply logic limit bình thường",
       note="Nguồn: r379"),

    tc("Action gắn tag", "MSG-001", "Normal",
       "Gỡ tag (remove tag): action gỡ tag hoạt động ở web và job, count giảm đúng",
       BOT + "\n- Tag「RemoveMe」đã gắn cho Friend F (count_user_tag = 5)\n- Action có type gỡ tag「RemoveMe」",
       "1. Gỡ tag cho F từ màn chat 1:1 → query tag_line_user + count\n2. Gắn lại, rồi gỡ bằng action job (action schedule) → query\n3. Kiểm tra F ở màn danh sách friend đã gắn tag\n4. Kiểm tra tab タグ của F ở chat 1:1",
       "Friend F, gỡ tag qua 2 đường",
       "- Cả 2 đường: bản ghi tag_line_user của F bị xoá\n- count_user_tag giảm đúng 1 mỗi lần\n- F KHÔNG còn hiển thị ở màn friend đã gắn tag\n- Tab タグ của F không còn tag「RemoveMe」",
       note="TC gốc r4 (Improve chung/Improve tag): 'gỡ tag ⇒ ko hiển thị trong mh list friend đã gắn tag nữa'. Nguồn: Improve chung r3-r5"),

    tc("Action gắn tag", "MSG-001", "Normal",
       "Filter theo tag: gửi tin (send all / scenario) lọc theo tag AND / OR → chỉ user thỏa mãn nhận tin",
       BOT + "\n- 3 tag: TagA, TagB, TagC\n- 4 friend với tổ hợp tag khác nhau (đủ 4 điều kiện lọc)",
       "1. Tạo broadcast filter tag theo điều kiện AND (đủ 4 tổ hợp) → gửi\n2. Kiểm tra danh sách user thực nhận\n3. Lặp lại với điều kiện OR\n4. Lặp lại với scenario dùng cùng filter\n5. Mở LINE app của 1-2 friend đối chứng",
       "4 tổ hợp điều kiện AND và 4 tổ hợp OR",
       "- CHỈ user thỏa mãn điều kiện lọc nhận tin\n- User không thỏa mãn KHÔNG nhận\n- Kết quả AND và OR khác nhau đúng như định nghĩa\n- Xác nhận trên LINE app thật của ít nhất 2 friend",
       env="PRODUCTION",
       note="MSG-001 (gửi ĐÚNG đối tượng). RULE-06 + RULE-08. Nguồn: Improve chung/Improve tag r6-r17 (filter tag AND/OR ở friendlist, send all, scenario)"),
]

# ═══════════ Nhóm 12-13: Phân quyền · Môi trường & Legacy ═══════════
S5 += [
    tc("Phân quyền", "PERM-001", "Normal",
       "Staff CÓ quyền màn tag: thực hiện được các thao tác được cấp",
       "- Bot A có 1 tài khoản staff ĐƯỢC phân quyền màn Quản lý tag",
       "Đăng nhập bằng staff có quyền, thực hiện:\n1. Xem danh sách tag / folder\n2. Tạo tag mới, tạo nhiều tag\n3. Edit tag, copy tag\n4. Xoá tag đơn lẻ + 一括削除\n5. Import CSV\n6. Sort tag, sort folder\n7. Vào màn 削除済みタグ + khôi phục tag",
       "Staff có quyền, 7 nhóm thao tác",
       "- Menu Quản lý tag HIỂN THỊ\n- Thực hiện được đúng các thao tác được cấp\n- Thao tác bị giới hạn (nếu có) hiển thị rõ ràng: ẩn nút hoặc báo lỗi\n- Thao tác xoá bởi staff → cột 操作者 ghi đúng staff đó",
       spec="Spec không ghi",
       note="Spec Gap G-12: phân quyền staff ở middleware basic_access, không có logic chi tiết trong TagController. Nguồn: r118-r120, r244, r259, r291, r313, r962"),

    tc("Phân quyền", "PERM-001", "Abnormal",
       "Staff KHÔNG có quyền màn tag: menu Quản lý tag bị ẩn",
       "- Bot A có 1 tài khoản staff KHÔNG được cấp quyền màn Quản lý tag",
       "1. Đăng nhập bằng staff không quyền\n2. Kiểm tra menu trái\n3. Thử truy cập trực tiếp URL /basic/tag",
       "Staff không quyền",
       "- KHÔNG thấy menu Quản lý tag ở menu trái\n- Truy cập trực tiếp /basic/tag → bị chặn hoặc redirect\n- Không thấy dữ liệu tag của bot",
       spec="Spec không ghi",
       note="Nguồn: suy ra từ Gap G-12"),

    tc("Phân quyền", "PERM-002", "Abnormal",
       "Không bypass được quyền bằng API trực tiếp: staff không quyền gọi thẳng 7 endpoint tag",
       "- Staff S KHÔNG được cấp quyền màn Quản lý tag, đã đăng nhập lấy session/token hợp lệ",
       "Dùng session của staff S gọi trực tiếp (Postman/DevTools):\n1. GET /ajax/v2/tag\n2. POST /ajax/v2/tag/create-multiple\n3. DELETE /ajax/v2/tag\n4. POST /ajax/save-tag (edit_tag)\n5. POST /ajax/v2/tag/restore-tag/{id}\n6. POST /ajax/save-tag-csv\n7. GET /basic/tag/edit-tag/{id}",
       "Session staff không quyền, 7 endpoint",
       "- CẢ 7 request bị từ chối ở TẦNG API (403/redirect), KHÔNG chỉ ẩn menu ở UI\n- Query DB: không record tags/category nào bị tạo/sửa/xoá\n- Response không lộ dữ liệu tag của bot",
       note="PERM-002: 'UI ẩn menu nhưng API vẫn cho' là mẫu bug lặp lại. 7 endpoint cùng 1 kết quả nên giữ chung. Evidence: response từng request + query DB. Nguồn: TC bổ sung"),

    tc("Phân quyền", "PERM-002", "Boundary",
       "Backend không enforce giới hạn 20 tag/lần: gọi thẳng EP-13 với 21 tag",
       BOT + "\n- Có session admin hợp lệ",
       "1. Gọi trực tiếp POST /ajax/v2/tag/create-multiple với mảng 21 tên tag\n2. Đọc response\n3. Query COUNT(*) tags mới tạo",
       "21 tên tag gửi thẳng qua API",
       "- Ghi nhận CHÍNH XÁC: backend tạo đủ 21 tag (không validate) HAY chặn ở 20\n- Nếu tạo đủ 21 → xác nhận Gap G-03 (giới hạn 20 là frontend-only) → cân nhắc bổ sung validate backend",
       note="Spec Gap G-03. TC bổ sung để xác nhận. Nguồn: G-03 spec"),

    tc("Phân quyền", "PERM-003", "Abnormal",
       "Cách ly đa bot: không thao tác được tag của bot khác qua API dù đã đăng nhập",
       "- Tài khoản admin quản lý bot A và bot B\n- Tag「BotBTag」id=555 thuộc bot B\n- Tài khoản admin thứ 2 chỉ quản lý bot C",
       "Đang chọn bot A, gọi trực tiếp:\n1. GET /basic/tag/edit-tag/555\n2. POST /ajax/save-tag với tag_id=555\n3. DELETE /ajax/v2/tag với ids=[555]\n4. POST /ajax/v2/tag/restore-tag/555\n5. Đăng nhập admin 2 (bot C), lặp lại các bước trên",
       "tag_id=555 thuộc bot B; bot đang chọn = A hoặc C",
       "- Tất cả request bị từ chối hoặc redirect về /basic/tag\n- Query tags id=555: name, deleted_at, category_id KHÔNG đổi\n- Admin 2 (khác tài khoản) cũng không truy cập được",
       note="PERM-003 + DATA-DB-001. Evidence: response + query tags id=555 trước/sau. Nguồn: TC bổ sung"),

    tc("Phân quyền", "DATA-DB-001", "Normal",
       "WHERE scope: 2 bot cùng có tag TRÙNG TÊN — thao tác trên bot A không đụng tới bot B",
       "- Bot A và bot B đều có tag tên「共通タグ」(khác id)\n- Mỗi tag đều có friend gắn",
       "1. Ở bot A: đổi tên「共通タグ」thành「共通タグ_A」→ query cả 2 record\n2. Ở bot A: xoá tag đó → query cả 2 record\n3. Ở bot A: import CSV có tên「共通タグ」→ query\n4. Ở bot A: khôi phục tag đã xoá → query\n5. Kiểm tra danh sách tag + màn 削除済みタグ của bot B",
       "2 bot, tag cùng tên「共通タグ」",
       "- Sau MỖI bước: record của bot B GIỮ NGUYÊN hoàn toàn (name, deleted_at, count_user_tag, category_id)\n- tag_line_user của bot B không bị xoá\n- Màn 削除済みタグ của bot B RỖNG\n- Không bản ghi nào bị update chéo bot",
       note="RULE-07: kiểm WHERE scope trên 2 tài khoản. Liên quan Bug #33286. Evidence: query trước/sau cả 2 record. Nguồn: r245 + BR-01"),

    tc("Môi trường & Legacy", "DATA-BACKUP-001", "Abnormal",
       "BR-02 backup lock: bot đang backup → mọi thao tác CUD tag/folder bị chặn cùng 1 message",
       "- Bot A đang có bản ghi backup_history với status IN (0,1)",
       "1. Thử tạo tag mới\n2. Thử sửa tên 1 tag\n3. Thử xoá 1 tag (đơn lẻ + 一括削除)\n4. Thử import CSV\n5. Thử tạo/xoá folder\n6. Thử 一括フォルダ変更\n7. Query tags + category sau tất cả",
       "backup_history.status = 0 hoặc 1; 6 nhóm thao tác",
       "- CẢ 6 nhóm bị chặn với「データコピー中は、データ不備を回避するために、編集不可能です。少し待ってから操作し直してください。」\n- DB: không record tags/category nào bị thêm/sửa/xoá",
       note="BR-02 — TC gốc CHƯA cover, TC bổ sung. 6 thao tác cùng 1 kết quả nên giữ chung. Evidence: query backup_history + ảnh message. Nguồn: BR-02 spec"),

    tc("Môi trường & Legacy", "DATA-BACKUP-001", "Normal",
       "BR-02: sau khi backup xong → các thao tác CUD tag hoạt động lại bình thường",
       "- Bot A vừa hoàn tất backup (backup_history.status khác 0 và 1)",
       "1. Tạo tag mới → kiểm tra\n2. Sửa tên tag → kiểm tra\n3. Xoá tag → kiểm tra\n4. Query tags",
       "backup_history.status đã khác 0,1",
       "- Cả 3 thao tác thành công, không còn message chặn\n- DB ghi nhận đúng thay đổi",
       note="BR-02. Nguồn: BR-02 spec"),

    tc("Môi trường & Legacy", "DATA-BACKUP-001", "Normal",
       "Backup dữ liệu bot: tag đã soft delete KHÔNG được đưa vào bản backup",
       "- Bot A có 5 tag active + 3 tag đã xoá (deleted_at NOT NULL)",
       "1. Chạy chức năng backup/copy dữ liệu bot A sang bot đích\n2. Kiểm tra danh sách tag ở bot đích\n3. Kiểm tra màn 削除済みタグ của bot đích\n4. Query tags WHERE bot_id = bot đích",
       "5 tag active + 3 tag deleted",
       "- Bot đích chỉ có ĐÚNG 5 tag active\n- Màn 削除済みタグ của bot đích RỖNG\n- Không record nào có deleted_at NOT NULL được copy sang",
       note="Nguồn: r963"),

    tc("Môi trường & Legacy", "JOB-001", "Normal",
       "Job auto-purge 1/4: tag có deleted_at = NULL → job KHÔNG động tới",
       "- Bot A có tag TagN với deleted_at = NULL",
       "1. Chạy job auto-purge (hoặc chờ lịch chạy)\n2. Query tags WHERE id = TagN\n3. Kiểm tra màn /basic/tag",
       "TagN: deleted_at = NULL",
       "- TagN KHÔNG bị xoá\n- Vẫn hiển thị ở /basic/tag\n- tag_line_user và action của TagN nguyên vẹn",
       env="PRODUCTION",
       note="Leader chốt MT-11 (2026-08-19): CÓ job xoá tag soft-delete sau 90 ngày → bổ sung vào spec. RULE-08. Nguồn: r951"),

    tc("Môi trường & Legacy", "JOB-001", "Boundary",
       "Job auto-purge 2/4: tag xoá 89 ngày trước (< 90) → job KHÔNG xoá, vẫn ở màn 削除済みタグ",
       "- Bot A có tag Tag89: deleted_at = hôm nay − 89 ngày",
       "1. Set deleted_at của Tag89 = hôm nay − 89 ngày\n2. Chạy job auto-purge\n3. Query tags WHERE id = Tag89\n4. Kiểm tra màn /basic/tag/removed",
       "Tag89: deleted_at = −89 ngày",
       "- Tag89 KHÔNG bị xoá khỏi DB\n- VẪN hiển thị ở màn 削除済みタグ\n- Vẫn khôi phục được",
       env="PRODUCTION",
       note="Leader chốt MT-11. Biên dưới. RULE-08. Nguồn: r952"),

    tc("Môi trường & Legacy", "JOB-001", "Boundary",
       "Job auto-purge 3/4: tag xoá ĐÚNG 90 ngày trước → job XOÁ VĨNH VIỄN khỏi DB",
       "- Bot A có tag Tag90: deleted_at = hôm nay − 90 ngày\n- Tag90 có tag_line_user + t_actions + t_actions_detail",
       "1. Set deleted_at của Tag90 = hôm nay − 90 ngày\n2. Ghi lại id tag + id action\n3. Chạy job auto-purge\n4. Query tags / tag_line_user / t_actions / t_actions_detail\n5. Kiểm tra màn /basic/tag/removed",
       "Tag90: deleted_at = −90 ngày (biên)",
       "- Tag90 bị XOÁ VĨNH VIỄN khỏi bảng tags\n- tag_line_user tương ứng bị xoá\n- t_actions và t_actions_detail của tag bị xoá\n- KHÔNG còn hiển thị ở màn 削除済みタグ",
       env="PRODUCTION",
       note="Leader chốt MT-11 → đóng Gap G-01, nâng confidence BR-08 lên Cao. TC gốc có id thật: tag 23513 / action 60795. RULE-08. Evidence: log job + query DB. Nguồn: r953"),

    tc("Môi trường & Legacy", "JOB-001", "Normal",
       "Job auto-purge 4/4: tag xoá 91 ngày trước (> 90) → job XOÁ VĨNH VIỄN",
       "- Bot A có tag Tag91: deleted_at = hôm nay − 91 ngày, có tag_line_user + action",
       "1. Set deleted_at của Tag91 = hôm nay − 91 ngày\n2. Chạy job auto-purge\n3. Query tags / tag_line_user / t_actions / t_actions_detail\n4. Kiểm tra màn 削除済みタグ",
       "Tag91: deleted_at = −91 ngày",
       "- Tag91 bị XOÁ VĨNH VIỄN khỏi bảng tags\n- tag_line_user, t_actions, t_actions_detail bị xoá theo\n- KHÔNG còn ở màn 削除済みタグ",
       env="PRODUCTION",
       note="Leader chốt MT-11. RULE-08. Nguồn: r954"),

    tc("Môi trường & Legacy", "COMPAT-LEGACY-001", "Normal",
       "Endpoint legacy /ajax/save-tag và /ajax/save-tag-csv vẫn hoạt động song song với v2",
       BOT + "\n- Bot A có tag tạo từ trước đợt improve 02/2025",
       "1. Edit tag qua UI (nội bộ dùng EP-30 /ajax/save-tag) → verify lưu đúng\n2. Copy tag qua UI (cũng EP-30) → verify\n3. Import CSV (EP-31 /ajax/save-tag-csv) → verify\n4. Kiểm tra response không lỗi 500",
       "Endpoint legacy EP-30, EP-31",
       "- Cả 3 thao tác thành công, không lỗi 500\n- Dữ liệu lưu đúng vào tags / t_actions / t_actions_detail",
       note="COMPAT-LEGACY-001. Spec §6 liệt kê legacy endpoints vẫn dùng. Nguồn: spec §6"),

    tc("Môi trường & Legacy", "COMPAT-LEGACY-001", "Normal",
       "Mobile API EP-60/EP-64/EP-67: gắn/gỡ tag đồng bộ 2 chiều với web, không trả tag đã xoá",
       BOT + "\n- Bot A có 5 tag active + 2 tag đã xoá\n- App mobile đã đăng nhập",
       "1. Gọi EP-67 /api/add-tag-for-user gắn 2 tag cho Friend F\n2. Kiểm tra trên web màn chat 1:1 của F\n3. Gỡ 1 tag trên web → gọi lại EP-60 /api/get-list-tag-of-user\n4. Gọi EP-64 /api/get-list-folder-tag-by-bot-v2\n5. Tìm 2 tag đã xoá trong response",
       "5 tag active + 2 tag đã xoá",
       "- EP-67 gắn tag thành công, web hiển thị ngay\n- Gỡ trên web → EP-60 phản ánh đúng\n- EP-60 và EP-64 KHÔNG trả về tag có deleted_at NOT NULL",
       note="COMPAT-LEGACY-001 + SYNC-APP-001. Nguồn: spec §6 mobile API"),

    tc("Môi trường & Legacy", "COMPAT-LEGACY-001", "Normal",
       "RULE-09: tag CŨ tạo trước đợt improve 02/2025 vẫn mở, sửa và lưu được bình thường",
       BOT + "\n- Bot A có ≥3 tag tạo từ trước 02/2025, một số có action theo format cũ",
       "1. Mở edit từng tag cũ\n2. Kiểm tra hiển thị: tên, folder, action, limit, action mode\n3. Sửa tên → lưu → query\n4. Thêm 1 action mới → lưu → query\n5. Gắn tag cũ cho Friend F, kiểm tra LINE app",
       "≥3 tag tạo trước đợt improve",
       "- Tag cũ mở lên hiển thị ĐỦ action/limit/folder, không lỗi\n- Sửa và lưu được bình thường\n- Action cũ vẫn gửi được tới LINE app của F\n- Không bị mất setting khi lưu lại",
       note="RULE-09 + RULE-06. Nguồn: r661-r663"),

    tc("Môi trường & Legacy", "ENV-003", "Normal",
       "Khác biệt môi trường: job / callback / auto-purge / performance phải kết luận từ PRODUCTION",
       "- Chuẩn bị cùng bộ data tag trên dev / staging / production",
       "1. Trên mỗi môi trường: gắn tag qua callback (rich menu / auto reply / template button)\n2. Gắn tag qua job không-callback (send all / scenario)\n3. Kiểm tra job auto-purge 90 ngày\n4. Import CSV 200 tag, đo thời gian\n5. Lập bảng so sánh kết quả 3 môi trường",
       "3 môi trường × 4 nhóm thao tác",
       "- Ghi rõ kết quả từng môi trường vào bảng so sánh\n- Mọi khác biệt giữa production và staging phải được ghi nhận và raise ticket\n- Kết luận CUỐI CÙNG về job / performance / callback CHỈ lấy từ PRODUCTION",
       env="PRODUCTION",
       note="RULE-08 + ENV-003. TC gốc ghi rõ mỗi server test tính năng khác nhau (dev: button · staging: autoreply · product: richmenu). Nguồn: r324, r327, r830"),
]
