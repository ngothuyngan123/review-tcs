# -*- coding: utf-8 -*-
"""FA-015 — Nhóm 5: Action gán friend info · Job action ngày tháng · Filter · Chèn giá trị vào tin nhắn.

Nguồn chính:
- 10.2 /「check setting-action-friend-info-date」(10/2025 → 04/2026): r17-r124 (action theo lối vào),
  r86-r120 (Bug #32287 duplicate), r196-r278 (Bug KH #34675 + Bug Tester #35967 mốc năm),
  r359-r390 (sửa setting khi bạn đã có giá trị).
- TCsLine_Modal Filter /「Filter point & date」(10/2023).
- TCsLine_Improve chung /「Improve filter friend info + sửa domain liff app」(07/2023).
- Feature #29832 (06/2025) — mã chèn giá trị friend info địa chỉ vào message.
"""
from _common import tc

CB = ("Action của callback: kết bạn mới · auto-reply · nút template button · image map · rich menu · "
      "postback từ LINE")
NOCB = ("Action KHÔNG phải callback: action schedule · booking (salon/lesson/event) · form · item · "
        "friend info · remind · tag · kịch bản · broadcast")

S5 = [
    # ══════════════════ Action gán friend info ══════════════════
    tc("Action gán friend info", "FUNC-MULTI-001", "Normal",
       "Dialog action: chọn action 友だち情報 → chọn được trường và kiểu thao tác theo từng loại trường",
       "- Bot A có đủ trường: 選択肢, 記述, 年月日, ポイント và trường mặc định 生年月日",
       "1. Mở dialog action ở màn bất kỳ (vd auto-reply)\n2. Chọn loại action「友だち情報」\n"
       "3. Chọn lần lượt từng trường và quan sát các tùy chọn thao tác hiện ra\n4. Chụp màn hình",
       "5 trường khác kiểu",
       "- Chọn được trường từ danh sách (nhóm theo folder)\n"
       "- Trường 選択肢: chọn được 1 option để ghi\n- Trường ポイント: có ghi đè / cộng / trừ / xóa, "
       "mỗi loại có kiểu chỉ định và ngẫu nhiên\n"
       "- Trường 年月日 và 生年月日: có「指定の日付を登録」/「当日日付を登録」/「登録情報を削除」",
       note="Evidence: ảnh chụp. Nguồn: tab date r17-r19 + spec SCR-FRI-06 (SC-004)."),

    tc("Action gán friend info", "FUNC-001", "Normal",
       "Action ghi giá trị 年月日 kiểu「指定の日付を登録」→ bạn nhận đúng giá trị ngày đã chỉ định",
       "- Trường 年月日「予約日」\n- Bạn U1 chưa có giá trị\n- Auto-reply keyword「予約」có action ghi 予約日 = 2026-12-24",
       "1. U1 gửi keyword「予約」từ LINE app\n2. Mở 友だち詳細 của U1 đọc giá trị 予約日\n"
       "3. Mở right bar chat 1:1\n4. Đọc 回答人数",
       "Ngày chỉ định: 2026-12-24",
       "- 友だち詳細 và right bar hiển thị 予約日 = 2026-12-24\n- 回答人数 tăng 1\n"
       "- Lịch sử ghi nhận việc gán giá trị",
       note="Nguồn: tab date r17, r28, r32, r36, r41, r45."),

    tc("Action gán friend info", "FUNC-001", "Normal",
       "Action ghi giá trị 年月日 kiểu「当日日付を登録」→ ghi đúng ngày hôm nay",
       "- Trường 年月日「初回来店日」\n- Bạn U1 chưa có giá trị\n- Auto-reply có action ghi 当日日付",
       "1. Ghi lại ngày hiện tại\n2. U1 gửi keyword từ LINE app\n3. Đọc giá trị ở 友だち詳細",
       "Ngày thực hiện test",
       "- Giá trị = đúng ngày hôm nay (theo múi giờ hệ thống)\n- 回答人数 tăng 1",
       note="Nguồn: tab date r18, r29, r33, r37."),

    tc("Action gán friend info", "FUNC-001", "Normal",
       "Action「登録情報を削除」cho trường 年月日 → xóa giá trị VÀ dọn lịch gửi của bạn",
       "- Trường 年月日 có action lịch\n- Bạn U1 đang có giá trị và đã sinh lịch gửi tương lai\n"
       "- Auto-reply keyword「解除」có action 登録情報を削除 cho trường đó",
       "1. Ghi lại mốc gửi dự kiến của U1\n2. U1 gửi keyword「解除」\n"
       "3. Đọc giá trị ở 友だち詳細 và 回答人数\n4. Chờ qua mốc gửi cũ, kiểm tra LINE app U1",
       "U1 có giá trị + có lịch gửi",
       "- U1 không còn giá trị ở trường đó, 回答人数 giảm 1\n"
       "- U1 KHÔNG nhận action nào tại mốc gửi cũ (lịch đã bị dọn)",
       env="PRODUCTION",
       note="RULE-08 (job). Nguồn: tab date r19, r69, r104, r120."),

    tc("Action gán friend info", "FUNC-001", "Normal",
       "Action ghi giá trị cho trường mặc định 生年月日 → lưu vào thông tin bạn và sinh lịch nếu có setting",
       "- Trường mặc định 生年月日 đã setting action lịch\n- Bạn U1 chưa có ngày sinh",
       "1. Auto-reply có action ghi 生年月日 =「指定の日付」\n2. U1 gửi keyword\n"
       "3. Đọc ngày sinh của U1 ở 友だち詳細\n4. Kiểm tra lịch gửi đã sinh cho U1",
       "生年月日 = 1996-01-01",
       "- Ngày sinh của U1 hiển thị đúng ở 友だち詳細 và right bar\n"
       "- Sinh lịch gửi đúng theo cấu hình của trường 生年月日",
       env="PRODUCTION",
       note="Nguồn: tab date r20-r21, r30-r31, r38-r39, r43-r44."),

    tc("Action gán friend info", "REG-SHARED-001", "Normal",
       "Action gán friend info chạy đúng từ MỌI lối vào có callback",
       "- Trường 年月日 và trường ポイント có action\n"
       "- Đã cấu hình action 友だち情報 ở tất cả các lối vào callback",
       "1. Với từng lối vào, kích hoạt action từ LINE app của 1 bạn riêng\n"
       "2. Sau mỗi lần: đọc giá trị ở 友だち詳細 + right bar và 回答人数\n"
       "3. Kiểm tra lịch gửi được sinh (với trường 年月日)",
       CB,
       "- Mọi lối vào: giá trị friend info được ghi đúng cho bạn tương ứng\n"
       "- 回答人数 tăng đúng\n- Với trường 年月日: lịch gửi được sinh đúng mốc",
       env="PRODUCTION",
       note="Các lối vào cùng 1 kết quả nên gộp 1 TC (liệt kê đủ ở Dữ liệu test). Nguồn: tab date r17-r44, r89."),

    tc("Action gán friend info", "REG-SHARED-001", "Normal",
       "Action gán friend info chạy đúng từ MỌI lối vào KHÔNG phải callback",
       "- Trường 年月日 và ポイント có action\n- Đã cấu hình action 友だち情報 ở các tính năng phía job",
       "1. Kích hoạt từng tính năng cho 1 bạn riêng\n2. Sau mỗi lần đọc giá trị và 回答人数\n"
       "3. Với trường 年月日 kiểm tra lịch gửi sinh ra\n4. Kiểm tra phía LINE app của bạn",
       NOCB,
       "- Mọi tính năng: giá trị được ghi đúng, hiển thị đủ ở 友だち詳細 và right bar\n"
       "- 回答人数 tăng đúng\n- Lịch gửi (nếu có) sinh đúng mốc",
       env="PRODUCTION",
       note="Nguồn: tab date r45-r85 (action schedule, tag, kịch bản, broadcast, remind, form, booking, item)."),

    tc("Action gán friend info", "FUNC-MULTI-001", "Normal",
       "Multi action chứa nhiều action friend info khác nhau → tất cả đều chạy đúng",
       "- Multi action gồm: ghi 年月日, cộng điểm, ghi option 選択肢, gắn tag\n- Bạn U1 chưa có giá trị",
       "1. Kích hoạt multi action cho U1\n2. Đọc giá trị 3 trường ở 友だち詳細\n"
       "3. Kiểm tra tag đã gắn\n4. Đọc 回答人数 của 3 trường",
       "4 action trong 1 multi action",
       "- Cả 3 trường friend info đều có giá trị đúng\n- Tag được gắn\n"
       "- 回答人数 của cả 3 trường đều tăng 1\n- Không action nào bị bỏ sót",
       note="Nguồn: tab date r45-r49 + tab「Change spec info type select」r10."),

    tc("Action gán friend info", "FUNC-001", "Normal",
       "Action ghi option cho trường 選択肢 → giá trị ghi đúng option và kích hoạt action của option đó",
       "- Trường 選択肢 với option A gắn action gửi text T1\n- Auto-reply có action ghi option A cho bạn",
       "1. Bạn U1 gửi keyword kích hoạt\n2. Đọc giá trị của U1\n3. Kiểm tra LINE app U1",
       "Ghi option A cho U1",
       "- U1 có giá trị = option A\n"
       "- U1 nhận text T1 (action gắn trên option được kích hoạt)\n- 回答人数 tăng 1",
       note="Nguồn: tab「Change spec info type select」r10 + corpus r267. Vế 'kích hoạt action của option' "
            "do AI khẳng định từ r267 — cần Leader xác nhận thứ tự chạy."),

    tc("Action gán friend info", "STATE-001", "Normal",
       "Action gán giá trị nhưng GIÁ TRỊ KHÔNG ĐỔI so với giá trị hiện có → không cập nhật lại lịch gửi",
       "- Trường 年月日 có action lịch\n- Bạn U1 đang có giá trị = 2026-12-24 và đã sinh lịch\n"
       "- Auto-reply có action ghi đúng 2026-12-24",
       "1. Ghi lại mốc gửi hiện tại của U1\n2. U1 gửi keyword kích hoạt action\n"
       "3. Đọc lại mốc gửi của U1\n4. Chờ tới mốc, kiểm tra LINE app U1",
       "Ghi lại đúng giá trị cũ 2026-12-24",
       "- Mốc gửi KHÔNG bị đổi\n- U1 nhận đúng 1 action tại mốc (không nhận trùng lặp)\n"
       "- 回答人数 không đổi",
       env="PRODUCTION",
       note="Đây là lõi Bug #32287. Nguồn: tab date r22-r24, r92-r94."),

    tc("Action gán friend info", "STATE-001", "Normal",
       "Bạn ĐÃ nhận action (lịch đã gửi xong) → thao tác chạm vào giá trị nhưng không đổi giá trị → KHÔNG gửi trùng",
       "- Trường 年月日 kiểu「月日」có action\n"
       "- Bạn U1 đã được gửi action năm nay và đã có lịch cho năm sau",
       "1. Ghi lại lịch hiện có của U1 (1 lịch đã gửi + 1 lịch năm sau)\n"
       "2. Ở right bar chat 1:1, mở datepicker của trường nhưng KHÔNG đổi ngày, click ra ngoài\n"
       "3. Đọc lại danh sách lịch của U1\n4. Chờ tới mốc gửi và đếm số tin U1 nhận",
       "Thao tác mở datepicker không đổi giá trị (đúng thao tác của khách trong #32287)",
       "- Số lịch không tăng, lịch đã gửi vẫn ở trạng thái đã gửi\n"
       "- U1 nhận ĐÚNG 1 tin tại mốc, KHÔNG nhận 2 tin trùng thời điểm",
       env="PRODUCTION",
       note="Tái hiện chính xác Bug #32287 (10/2025). Nguồn: tab date r87 (mô tả tái hiện) + r94, r103."),

    tc("Action gán friend info", "STATE-001", "Normal",
       "Cập nhật giá trị từ THỎA MÃN sang KHÔNG thỏa mãn điều kiện gửi → lịch được xử lý đúng theo kiểu 月日 / 年月日",
       "- Trường 年月日 có action\n- Bạn U1 (kiểu 月日) và U2 (kiểu 年月日) đều đang có lịch chờ gửi",
       "1. Đổi giá trị của U1 sang ngày không còn thỏa mãn → đọc lịch của U1\n"
       "2. Đổi giá trị của U2 sang ngày không còn thỏa mãn → đọc lịch của U2\n"
       "3. Chờ qua mốc cũ, kiểm tra LINE app của U1 và U2",
       "U1: kiểu 月日 · U2: kiểu 年月日",
       "- U1 (月日): lịch dời sang năm kế tiếp, không gửi ở mốc cũ\n"
       "- U2 (年月日): lịch bị xóa, U2 không nhận action nào\n- Cả 2 không nhận tin ở mốc cũ",
       env="PRODUCTION",
       note="Nguồn: tab date r95-r96, r111-r112."),

    tc("Action gán friend info", "STATE-001", "Normal",
       "Cập nhật giá trị từ KHÔNG thỏa mãn sang THỎA MÃN → sinh hoặc cập nhật lịch đúng",
       "- Trường 年月日 có action\n- U1 chưa có lịch nào, U2 đang có 1 lịch cho năm sau",
       "1. Đổi giá trị U1 sang ngày thỏa mãn → đọc lịch U1\n"
       "2. Đổi giá trị U2 sang ngày thỏa mãn → đọc lịch U2\n"
       "3. Chờ tới mốc, kiểm tra LINE app U1 và U2",
       "U1 chưa có lịch · U2 đã có lịch năm sau",
       "- U1: sinh lịch mới đúng mốc, nhận action đúng giờ\n"
       "- U2: lịch cũ được cập nhật sang mốc mới (không sinh thêm lịch thứ 2), nhận đúng 1 tin",
       env="PRODUCTION",
       note="Nguồn: tab date r99-r101, r115-r117."),

    tc("Action gán friend info", "STATE-001", "Boundary",
       "Bạn đã có lịch ĐÃ GỬI + cập nhật sang giá trị thỏa mãn khác → lịch đã gửi giữ nguyên, sinh thêm 1 lịch mới",
       "- Trường 年月日 có action\n- Bạn U1 có 1 lịch trạng thái đã gửi",
       "1. Ghi lại lịch đã gửi của U1\n2. Đổi giá trị U1 sang ngày khác vẫn thỏa mãn\n"
       "3. Đọc danh sách lịch của U1\n4. Chờ tới mốc mới, kiểm tra LINE app U1",
       "U1 có 1 lịch đã gửi, đổi sang giá trị thỏa mãn khác",
       "- Lịch đã gửi giữ nguyên trạng thái đã gửi (không bị đưa về chờ gửi)\n"
       "- Sinh thêm đúng 1 lịch mới ở trạng thái chờ gửi\n- U1 nhận đúng 1 tin ở mốc mới",
       env="PRODUCTION",
       note="Đối chứng trực tiếp Bug #32287. Nguồn: tab date r102, r118."),

    tc("Action gán friend info", "STATE-001", "Boundary",
       "Bạn có 2 lịch (1 đã gửi năm nay + 1 chờ gửi năm sau) + cập nhật giá trị → chỉ lịch chờ gửi được cập nhật",
       "- Bạn U1 có 2 lịch: năm nay đã gửi, năm sau chờ gửi",
       "1. Ghi lại 2 lịch của U1\n2. Đổi giá trị U1 sang ngày khác (vẫn thỏa mãn)\n"
       "3. Đọc lại 2 lịch\n4. Chờ tới mốc mới, đếm số tin U1 nhận",
       "2 lịch: đã gửi + chờ gửi",
       "- Lịch đã gửi giữ nguyên\n- Lịch chờ gửi được cập nhật sang mốc mới\n"
       "- Không sinh lịch thứ 3\n- U1 nhận đúng 1 tin",
       env="PRODUCTION",
       note="Nguồn: tab date r98, r103, r114, r119."),

    tc("Action gán friend info", "REG-SHARED-001", "Normal",
       "Action friend info từ QR landing có set param (bạn mới / bạn cũ) → hành vi giống action callback",
       "- QR landing có set param ghi trường 生年月日 và trường 年月日 tự tạo",
       "1. Bạn mới quét QR (có callback kết bạn) → kiểm tra giá trị + lịch gửi\n"
       "2. Bạn cũ quét QR (không có callback kết bạn) → kiểm tra giá trị + lịch gửi\n"
       "3. Bạn đã là bạn của bot và có sẵn trong hệ thống → kiểm tra",
       "3 kịch bản quét QR",
       "- Cả 3 kịch bản: giá trị được ghi đúng, lịch gửi sinh đúng như lối vào callback\n"
       "- Bạn nhận action đúng mốc",
       env="PRODUCTION",
       note="Nguồn: tab date r121-r123, r181-r189, r252-r278."),

    tc("Action gán friend info", "INTG-HOOK-001", "Abnormal",
       "Import CSV cập nhật giá trị 年月日 → KHÔNG kích hoạt action, nhưng lịch gửi được cập nhật",
       "- Trường 年月日 có action gửi text\n- Bạn U1 đang có giá trị không thỏa mãn điều kiện gửi",
       "1. Import CSV đặt giá trị mới cho U1 (thỏa mãn điều kiện gửi)\n"
       "2. Ngay sau import: kiểm tra LINE app U1 có nhận tin ngay không\n"
       "3. Kiểm tra lịch gửi của U1\n4. Chờ tới mốc, kiểm tra LINE app U1",
       "CSV cập nhật giá trị thỏa mãn",
       "- Import KHÔNG kích hoạt action ngay (U1 không nhận tin lúc import)\n"
       "- Lịch gửi của U1 được cập nhật/sinh đúng mốc mới\n"
       "- U1 nhận action đúng mốc đã lên lịch",
       env="PRODUCTION",
       note="⚠️ Corpus có 2 vế khác nhau: tab date r124 ghi 'import CSV sẽ không action ⇒ info type date cũng "
            "không action ⇒ không update event_step_time', còn r279-r281 ghi 'update lại time send action' + "
            "'insert vào event_step_time' — xem MT-16. Cần Leader chốt."),

    tc("Action gán friend info", "PERM-001", "Abnormal",
       "Account staff thực hiện action gán friend info → theo quyền được cấp",
       "- Account staff, trường friend info có action",
       "1. Đăng nhập staff\n2. Thực hiện action gán friend info ở màn chat 1:1 (nếu có quyền)\n"
       "3. Đọc giá trị và 回答人数\n4. Ghi lại hành vi khi staff KHÔNG có quyền",
       "Staff có quyền / không có quyền",
       "- Staff có quyền: action chạy đúng, giá trị và count cập nhật như admin\n"
       "- Staff không có quyền: bị chặn với message quyền, không ghi giá trị",
       spec="Đã hỏi leader",
       note="⚠️ Corpus có dòng「Check account staff」(tab date r189, r356) nhưng KHÔNG có kết quả mong đợi → "
            "expected do AI viết. Xem MT-12."),

    # ══════════════════ Job action ngày tháng ══════════════════
    tc("Job action ngày tháng", "JOB-001", "Normal",
       "Job gửi action đúng thời điểm đã lên lịch → bạn nhận trên LINE app, lịch chuyển trạng thái đã gửi",
       "- Trường 年月日 có action gửi text\n- Bạn U1 đã sinh lịch gửi trong ~10 phút tới\n"
       "- Job gửi action đang bật",
       "1. Ghi lại mốc gửi của U1\n2. Chờ tới mốc, theo dõi LINE app U1\n"
       "3. Kiểm tra trạng thái lịch sau khi gửi\n4. Kiểm tra lịch sử gửi ở 友だち詳細",
       "Mốc gửi: T+10 phút",
       "- U1 nhận đúng tin nhắn tại mốc (sai lệch trong ngưỡng chấp nhận của job)\n"
       "- Lịch chuyển sang trạng thái đã gửi\n- Lịch sử gửi được ghi lại",
       env="PRODUCTION",
       note="RULE-08 (job) + RULE-06 (LINE app). ⚠️ Job có cấu hình bật/tắt (spec §7: ENABLE_EVENT_REMIND mặc định 0) "
            "→ phải xác nhận job đang bật trước khi test, xem MT-17."),

    tc("Job action ngày tháng", "JOB-001", "Normal",
       "Kiểu「月日」sau khi gửi xong → job tự sinh lịch cho năm kế tiếp, KHÔNG gửi trùng",
       "- Trường 年月日 kiểu「月日」có action\n- Bạn U1 có lịch gửi sắp tới",
       "1. Chờ job gửi cho U1\n2. Đếm số tin U1 nhận trong 24h\n"
       "3. Kiểm tra lịch mới sinh và năm của nó",
       "U1 kiểu 月日",
       "- U1 nhận ĐÚNG 1 tin\n- Sinh đúng 1 lịch mới cho cùng ngày/tháng năm kế tiếp\n"
       "- Không tồn tại 2 lịch cùng mốc ở trạng thái chờ gửi",
       env="PRODUCTION",
       note="Bug #32287. Nguồn: tab date r3, r40."),

    tc("Job action ngày tháng", "JOB-001", "Boundary",
       "Mốc gửi tính theo GIÁ TRỊ bạn nhập, không theo năm hiện tại — giá trị quá khứ > 1 năm (năm thường)",
       "- Trường 年月日 kiểu「年月日」có action\n- Hôm nay 2026-04-18 (điều chỉnh theo ngày chạy thực tế)",
       "1. Gán U1 = 2023-04-18, cấu hình gửi SAU 1100 ngày\n"
       "2. Đọc mốc gửi dự kiến của U1\n3. Chờ tới mốc, kiểm tra LINE app U1",
       "Giá trị 2023-04-18 + 1100 ngày → mốc dự kiến 2026-04-22",
       "- Mốc gửi = 2026-04-22 (tính từ giá trị bạn nhập)\n"
       "- KHÔNG bị tính theo năm hiện tại làm mốc\n- U1 nhận action đúng ngày đó",
       env="PRODUCTION",
       note="Lõi Bug KH #34675 (03/2026). Nguồn: tab date r208."),

    tc("Job action ngày tháng", "JOB-001", "Boundary",
       "Mốc gửi với giá trị quá khứ năm NHUẬN (29/02) → tính đúng ngày, không lệch",
       "- Trường 年月日 kiểu「年月日」\n- Hôm nay 2026-04-18",
       "1. Gán U1 = 2024-02-29, gửi SAU 800 ngày → đọc mốc\n"
       "2. Gán U2 = 2000-02-29, gửi SAU 100 ngày và TRƯỚC 100 ngày → đọc mốc\n"
       "3. Chờ mốc của U1 và kiểm tra LINE app",
       "U1: 2024-02-29 + 800 ngày → 2026-05-09\nU2: 2000-02-29 (quá khứ xa)",
       "- U1: mốc = 2026-05-09, nhận action đúng ngày\n"
       "- U2: KHÔNG sinh lịch nào (mốc đã ở quá khứ), không nhận action",
       env="PRODUCTION",
       note="Nguồn: tab date r209-r210, r217."),

    tc("Job action ngày tháng", "JOB-001", "Boundary",
       "Kiểu「年月日」với giá trị NĂM HIỆN TẠI → mốc trước/sau tính đúng ngày",
       "- Trường 年月日 kiểu「年月日」\n- Hôm nay 2026-04-18",
       "1. Gán U1 = 2026-04-30, cấu hình gửi TRƯỚC 3 ngày → đọc mốc\n"
       "2. Đổi sang gửi SAU 3 ngày → đọc mốc\n3. Chờ tới mốc và kiểm tra LINE app",
       "Trước 3 ngày → 2026-04-27 · Sau 3 ngày → 2026-05-03",
       "- Mốc lần lượt = 2026-04-27 và 2026-05-03\n- U1 nhận action đúng mốc đang cấu hình",
       env="PRODUCTION",
       note="Nguồn: tab date r211."),

    tc("Job action ngày tháng", "JOB-001", "Boundary",
       "Kiểu「年月日」với giá trị NĂM TƯƠNG LAI liền sau → mốc tính đúng qua ranh giới năm",
       "- Trường 年月日 kiểu「年月日」\n- Hôm nay 2026-04-18",
       "1. Gán U1 = 2027-02-28, gửi TRƯỚC 30 ngày → đọc mốc\n"
       "2. Đổi gửi TRƯỚC 60 ngày → đọc mốc\n3. Đổi gửi SAU 60 ngày → đọc mốc",
       "Trước 30 → 2027-01-29 · Trước 60 → 2026-12-30 · Sau 60 → 2027-04-29",
       "- 3 mốc lần lượt đúng: 2027-01-29, 2026-12-30, 2027-04-29\n"
       "- Không bị nhảy về năm hiện tại",
       env="PRODUCTION",
       note="Nguồn: tab date r213."),

    tc("Job action ngày tháng", "JOB-001", "Boundary",
       "Kiểu「年月日」với giá trị năm tương lai cách > 1 năm (năm thường) → mốc tính đúng cả offset lớn",
       "- Trường 年月日 kiểu「年月日」\n- Hôm nay 2026-04-18",
       "1. Gán U1 = 2030-12-31\n2. Lần lượt cấu hình: trước 1 / trước 60 / trước 1000 / sau 1 / sau 365 ngày\n"
       "3. Sau mỗi cấu hình đọc mốc gửi dự kiến",
       "Trước 1 → 2030-12-30 · Trước 60 → 2030-11-01 · Trước 1000 → 2028-04-05 · "
       "Sau 1 → 2031-01-01 · Sau 365 → 2031-12-31",
       "- Cả 5 mốc đúng như bảng tính tay ở cột Dữ liệu test\n- Không mốc nào bị quy về năm hiện tại",
       env="PRODUCTION",
       note="Nguồn: tab date r214."),

    tc("Job action ngày tháng", "JOB-001", "Boundary",
       "Kiểu「年月日」với giá trị năm tương lai NHUẬN → mốc quanh 29/02 tính đúng",
       "- Trường 年月日 kiểu「年月日」\n- Hôm nay 2026-04-18",
       "1. Gán U1 = 2028-02-28\n2. Cấu hình lần lượt: trước 1 / trước 60 / trước 460 / sau 2 / sau 365 ngày\n"
       "3. Đọc mốc gửi dự kiến sau mỗi cấu hình",
       "Trước 1 → 2028-02-27 · Trước 60 → 2027-12-30 · Trước 460 → 2026-11-25 · "
       "Sau 2 → 2028-03-01 · Sau 365 → 2029-02-27",
       "- Cả 5 mốc đúng như bảng tính tay\n- Không lệch 1 ngày do năm nhuận",
       env="PRODUCTION",
       note="Nguồn: tab date r215."),

    tc("Job action ngày tháng", "JOB-001", "Boundary",
       "Kiểu「年月日」với giá trị quá khứ → KHÔNG sinh lịch, không gửi (mọi offset)",
       "- Trường 年月日 kiểu「年月日」\n- Hôm nay 2026-04-18",
       "1. Gán U1 = 2023-04-18, cấu hình gửi sau 1 ngày → kiểm tra lịch\n"
       "2. Đổi gửi trước 1 ngày → kiểm tra lịch\n"
       "3. Gán U2 = 2025-04-30 (quá khứ cách 1 năm), thử các offset → kiểm tra lịch\n"
       "4. Chờ 24h kiểm tra LINE app U1, U2",
       "U1 = 2023-04-18 · U2 = 2025-04-30 · offset trước/sau 1..365 ngày",
       "- Không sinh lịch với các mốc đã ở quá khứ\n"
       "- Chỉ sinh lịch cho mốc còn ở tương lai (vd U2 + sau 365 ngày = 2026-04-30)\n"
       "- Bạn không nhận action nào cho các mốc quá khứ",
       env="PRODUCTION",
       note="Nguồn: tab date r216, r259-r260."),

    tc("Job action ngày tháng", "JOB-001", "Boundary",
       "Kiểu「月日」với giá trị quá khứ xa → chỉ sinh ĐÚNG 1 lịch thỏa mãn của năm gần nhất",
       "- Trường 年月日 kiểu「月日」\n- Hôm nay 2026-04-18",
       "1. Gán U1 = 2022-12-31, cấu hình gửi trước 1 ngày → đọc số lịch và mốc\n"
       "2. Đổi trước 60 / trước 365 / sau 1 / sau 60 ngày → đọc lại sau mỗi lần\n"
       "3. Gán U2 = 1996-01-01 và lặp các offset",
       "U1 = 2022-12-31: trước 1 → 2026-12-30 · trước 60 → 2026-11-01 · trước 365 → 2026-12-31 · "
       "sau 1 → 2027-01-01\nU2 = 1996-01-01: trước 1 → 2026-12-31 · trước 30 → 2026-12-02 · "
       "trước 90 → 2026-10-03 · trước 270 → 2027-04-06",
       "- Mỗi cấu hình chỉ sinh ĐÚNG 1 lịch, đúng mốc trong bảng tính tay\n"
       "- Không sinh nhiều lịch cho các năm quá khứ",
       env="PRODUCTION",
       note="Nguồn: tab date r252-r253 (khối #34675)."),

    tc("Job action ngày tháng", "JOB-001", "Boundary",
       "Kiểu「月日」với giá trị năm hiện tại / tương lai → mốc lặp hàng năm tính đúng",
       "- Trường 年月日 kiểu「月日」\n- Hôm nay 2026-04-18",
       "1. Gán U1 = 2026-04-30, cấu hình trước 1 / trước 30 / trước 270 / trước 365 ngày → đọc mốc\n"
       "2. Gán U2 = 2027-01-01 và lặp các offset → đọc mốc\n"
       "3. Gán U3 = 2030-05-01 và lặp → đọc mốc",
       "U1 = 2026-04-30: trước 1 → 2026-04-29 · trước 30 → 2027-03-31 · trước 270 → 2026-08-03 · "
       "trước 365 → 2026-04-30\nU2 = 2027-01-01: trước 1 → 2026-12-31 · trước 30 → 2026-12-02\n"
       "U3 = 2030-05-01: trước 1 → 2030-04-30 · trước 270 → 2029-08-04",
       "- Toàn bộ mốc khớp bảng tính tay ở cột Dữ liệu test\n- Mỗi cấu hình chỉ 1 lịch chờ gửi",
       env="PRODUCTION",
       note="Nguồn: tab date r255-r258 (khối #34675)."),

    tc("Job action ngày tháng", "JOB-001", "Boundary",
       "Điều kiện gửi THỎA MÃN nhưng job vẫn đẩy sang năm sau → phải KHÔNG tái hiện (bug gốc #34675)",
       "- Trường 年月日 kiểu「月日」\n- Hôm nay ~2026-03-12 (điều chỉnh theo ngày chạy)",
       "1. Gán U1 = 2025-12-31, cấu hình gửi SAU 75 ngày → đọc mốc\n"
       "2. Gán U2 = 2024-12-31, gửi SAU 436 ngày → đọc mốc\n"
       "3. Gán U3 = 2026-03-11, gửi SAU 1 ngày → đọc mốc\n"
       "4. Gán U4 = 2027-01-01, gửi TRƯỚC 295 ngày → đọc mốc\n"
       "5. Gán U5 = 2026-03-12, gửi SAU 0 ngày → đọc mốc\n"
       "6. Chờ tới mốc từng bạn và kiểm tra LINE app",
       "5 bộ giá trị thỏa mãn điều kiện gửi trong năm hiện tại",
       "- Cả 5 bạn: lịch sinh cho mốc thỏa mãn NĂM HIỆN TẠI (không bị đẩy sang năm sau)\n"
       "- Cả 5 bạn nhận action đúng mốc\n- Mốc tính theo giá trị bạn nhập, không theo năm hiện tại",
       env="PRODUCTION",
       note="Đây là bộ dữ liệu tái hiện gốc của #34675 (corpus ghi rõ 'bug: setting thỏa mãn nhưng job insert "
            "vào next cho năm sau'). Nguồn: tab date r199-r203, r232-r236."),

    tc("Job action ngày tháng", "JOB-001", "Boundary",
       "Điều kiện gửi KHÔNG thỏa mãn (kiểu 月日) → sinh lịch cho năm kế tiếp",
       "- Trường 年月日 kiểu「月日」\n- Hôm nay ~2026-03-12",
       "1. Gán U1 = 2025-12-31, gửi TRƯỚC 1 ngày → đọc mốc\n"
       "2. Gán U2 = 2024-12-31, gửi TRƯỚC 1 ngày → đọc mốc\n"
       "3. Gán U3 = 2025-12-31, gửi SAU 69 ngày → đọc mốc\n"
       "4. Gán U4 = 2026-03-10, gửi TRƯỚC 1 ngày → đọc mốc",
       "4 bộ giá trị KHÔNG thỏa mãn trong năm hiện tại",
       "- Cả 4 bạn: sinh đúng 1 lịch cho NĂM KẾ TIẾP\n- Không bạn nào nhận action trong năm hiện tại",
       env="PRODUCTION",
       note="Nguồn: tab date r204-r207, r237-r240."),

    tc("Job action ngày tháng", "JOB-001", "Normal",
       "Job xử lý được cả action ghi trường 生年月日 và trường 年月日 tự tạo",
       "- Trường mặc định 生年月日 và 1 trường 年月日 tự tạo, cả 2 đều có action lịch",
       "1. Gán giá trị cho U1 ở 生年月日 và U2 ở trường tự tạo (cùng mốc gửi)\n"
       "2. Chờ tới mốc, kiểm tra LINE app U1 và U2\n3. Kiểm tra lịch sử gửi của cả 2",
       "U1 ở 生年月日 · U2 ở trường tự tạo",
       "- Cả U1 và U2 nhận action đúng mốc\n- Không bạn nào bị bỏ sót\n- Lịch của cả 2 chuyển trạng thái đã gửi",
       env="PRODUCTION",
       note="Nguồn: tab date r89-r120 (2 nhánh 'Action friend info ngày sinh' và 'Action friend info type date')."),

    tc("Job action ngày tháng", "JOB-001", "Normal",
       "Sửa SETTING của trường khi bạn ĐÃ có giá trị → lịch gửi được tính lại theo setting mới",
       "- Trường 年月日 kiểu「月日」\n- Bạn U1 có giá trị 2025-12-25, hôm nay 2026-03-24",
       "1. Thêm dòng cấu hình gửi SAU 90 ngày → đọc mốc của U1\n"
       "2. Đổi thành SAU 89 ngày với giờ còn thỏa mãn (> giờ hiện tại) → đọc mốc\n"
       "3. Đổi thành SAU 89 ngày với giờ đã qua (< giờ hiện tại) → đọc mốc\n"
       "4. Đổi thành TRƯỚC 1 ngày → đọc mốc",
       "U1 = 2025-12-25, hôm nay 2026-03-24\nSau 90 → 2026-03-25 · Sau 89 (giờ còn) → 2026-03-24 · "
       "Sau 89 (giờ đã qua) → 2027-03-24 · Trước 1 → 2026-12-24",
       "- 4 mốc lần lượt đúng như bảng tính tay\n"
       "- Mỗi lần sửa setting chỉ còn 1 lịch chờ gửi cho U1",
       env="PRODUCTION",
       note="Nguồn: tab date r360-r363, r368-r371."),

    tc("Job action ngày tháng", "JOB-001", "Boundary",
       "Sửa setting kiểu「年月日」khi mốc rơi vào quá khứ → KHÔNG thêm lịch, xóa lịch cũ nếu có",
       "- Trường 年月日 kiểu「年月日」\n- Bạn U1 có giá trị 2025-12-25 hoặc 2026-03-25, hôm nay 2026-03-24",
       "1. Thêm cấu hình SAU 89 ngày với giờ đã qua → kiểm tra lịch U1\n"
       "2. Đổi thành TRƯỚC 1 ngày với giờ đã qua → kiểm tra lịch\n"
       "3. Với trường hợp U1 ĐÃ có lịch trước đó: sửa setting sao cho mốc thành quá khứ → kiểm tra lịch\n"
       "4. Chờ 24h kiểm tra LINE app U1",
       "Các mốc rơi vào quá khứ",
       "- Không thêm lịch mới\n- Lịch cũ (nếu có) bị xóa khỏi hàng đợi gửi\n"
       "- U1 không nhận action nào",
       env="PRODUCTION",
       note="Nguồn: tab date r376-r380, r384-r388."),

    tc("Job action ngày tháng", "JOB-001", "Normal",
       "Xóa cấu hình action của trường 年月日 → lịch gửi của mọi bạn bị dọn",
       "- Trường 年月日 có action, 5 bạn đang có lịch chờ gửi",
       "1. Ghi lại mốc gửi của 5 bạn\n2. Vào màn edit xóa dòng cấu hình action → lưu\n"
       "3. Kiểm tra lịch của 5 bạn\n4. Chờ qua mốc cũ, kiểm tra LINE app của 5 bạn",
       "5 bạn có lịch",
       "- Không còn lịch chờ gửi nào cho 5 bạn ở trường này\n"
       "- Cả 5 bạn KHÔNG nhận action tại mốc cũ\n- Giá trị friend info của họ vẫn còn (không bị xóa theo)",
       env="PRODUCTION",
       note="Nguồn: tab date r390 ('Check xóa action info ⇒ xóa record trong bảng event_step_time')."),

    tc("Job action ngày tháng", "JOB-001", "Abnormal",
       "Bạn có 2 lịch trùng CÙNG mốc gửi → chỉ gửi 1 lần (không gửi trùng)",
       "- Dữ liệu lệch: bạn U1 có 2 lịch chờ gửi cùng thời điểm cho cùng trường",
       "1. Ghi lại 2 lịch của U1\n2. Chờ tới mốc gửi\n3. Đếm số tin U1 nhận trên LINE app\n"
       "4. Kiểm tra trạng thái 2 lịch sau khi gửi",
       "2 lịch cùng mốc, cùng trường",
       "- U1 nhận ĐÚNG 1 tin (không nhận 2 tin trùng)\n- Cả 2 lịch được xử lý, không còn lịch treo",
       env="PRODUCTION",
       note="Bug #32287. Corpus recover r192 ghi 'user có 2 bản ghi cùng send_time ⇒ xóa bớt 1 bản ghi'. "
            "Nguồn: tab date r192."),

    tc("Job action ngày tháng", "DATA-MIG-001", "Abnormal",
       "Recover dữ liệu lịch gửi bị lệch → xử lý đúng theo từng trường hợp, không đụng lịch tính năng khác",
       "- Có dữ liệu lệch: (a) bạn chỉ có 1 lịch chờ gửi, (b) bạn có 1 lịch đã gửi + 1 chờ gửi, "
       "(c) bạn có 2 lịch chờ gửi cùng mốc, (d) bạn có 2 lịch chờ gửi khác mốc\n"
       "- Có lịch remind của tính năng khác (booking, form) làm đối chứng",
       "1. Chạy tiến trình recover\n2. Kiểm tra lịch của bạn ở từng trường hợp (a)(b)(c)(d)\n"
       "3. Kiểm tra lịch remind của tính năng khác\n4. Chờ tới các mốc và kiểm tra LINE app",
       "4 trường hợp dữ liệu lệch + lịch của tính năng khác",
       "- (a) và (b): KHÔNG thay đổi gì\n- (c): xóa bớt còn 1 lịch\n"
       "- (d): giữ nguyên, có log để rà lại (không tự xóa)\n"
       "- Lịch remind của tính năng khác KHÔNG bị xóa nhầm\n- Bạn nhận đúng 1 action tại mỗi mốc",
       env="PRODUCTION",
       note="Nguồn: tab date r190-r194."),

    tc("Job action ngày tháng", "JOB-001", "Normal",
       "Recover lịch gửi cho trường 年月日 và 生年月日 → lịch được khôi phục đủ để gửi cho bạn",
       "- Đã chạy recover cho dữ liệu lịch của 2 loại trường",
       "1. Chạy recover\n2. Kiểm tra lịch của các bạn ở trường 年月日 tự tạo\n"
       "3. Kiểm tra lịch ở trường 生年月日\n4. Chờ tới mốc, kiểm tra LINE app",
       "2 loại trường",
       "- Lịch được khôi phục đúng mốc cho cả 2 loại trường\n- Bạn nhận action đúng thời điểm",
       env="PRODUCTION",
       note="Nguồn: tab date r357-r358."),

    tc("Job action ngày tháng", "ENV-001", "Abnormal",
       "Bot hết hạn / plan không hợp lệ → job bỏ qua lịch, không gửi và không lỗi",
       "- Bot B đã hết hạn plan > 7 ngày, có bạn với lịch gửi tới hạn\n- Bot A bình thường (đối chứng)",
       "1. Chờ tới mốc gửi của bạn thuộc bot B\n2. Kiểm tra LINE app bạn đó\n"
       "3. Kiểm tra trạng thái lịch\n4. Kiểm tra bạn thuộc bot A vẫn nhận action đúng",
       "Bot hết hạn > 7 ngày · bot bình thường",
       "- Bạn thuộc bot hết hạn KHÔNG nhận action\n- Lịch chuyển sang trạng thái bỏ qua, không báo lỗi\n"
       "- Bạn thuộc bot A vẫn nhận action bình thường",
       env="PRODUCTION",
       note="Spec §7 (bot hết hạn > 7 ngày → status SKIP). Corpus không có TC → AI bổ sung, cần Leader xác nhận."),

    tc("Job action ngày tháng", "JOB-001", "Abnormal",
       "Job khởi động lại giữa chừng → lịch đang gửi dở được xử lý lại, không mất và không gửi trùng",
       "- Có ≥ 20 lịch tới hạn cùng lúc\n- Có quyền restart tiến trình job (phối hợp dev)",
       "1. Kích hoạt lô lịch tới hạn\n2. Restart job khi đang gửi dở\n"
       "3. Sau khi job chạy lại, đếm số bạn đã nhận action\n4. Kiểm tra có bạn nào nhận 2 lần không",
       "≥ 20 lịch cùng mốc",
       "- Tất cả bạn đều nhận đúng 1 action (không mất, không trùng)\n"
       "- Không còn lịch treo ở trạng thái đang gửi",
       env="PRODUCTION",
       note="Spec §7 (resume sau restart: load lại status=1). TC do AI bổ sung, cần Leader xác nhận khả năng thực hiện."),

    # ══════════════════ Filter theo friend info ══════════════════
    tc("Filter theo friend info", "UI-001", "Normal",
       "Modal filter: chọn điều kiện theo trường friend info kiểu 年月日 → hiển thị đủ lựa chọn",
       "- Bot có trường 年月日 và trường mặc định 生年月日\n- Mở modal filter ở màn danh sách bạn bè",
       "1. Mở modal filter → chọn điều kiện 友だち情報\n2. Chọn trường kiểu 年月日\n"
       "3. Liệt kê các lựa chọn điều kiện hiện ra\n4. Chụp màn hình",
       "Trường 年月日 và 生年月日",
       "- Có lựa chọn「登録情報あり」(có giá trị) và「登録なし」(không có giá trị)\n"
       "- Có lựa chọn filter theo mốc thời gian (chỉ ngày/tháng hoặc ngày/tháng/năm)\n"
       "- Có lựa chọn filter theo khoảng thời gian (tick 範囲)",
       note="Evidence: ảnh chụp. Nguồn: Modal Filter /「Filter point & date」r3-r9 (10/2023). "
            "⚠️ TC gốc gần 3 năm — CẦN VERIFY LẠI."),

    tc("Filter theo friend info", "OUT-PREVIEW-001", "Normal",
       "Preview điều kiện filter hiển thị tên trường friend info",
       "- Đã tạo filter với 3 điều kiện theo 3 trường friend info khác nhau",
       "1. Tạo filter với điều kiện 1, 2, 3\n2. Đọc text preview của từng điều kiện",
       "3 điều kiện friend info",
       "- Mỗi điều kiện hiển thị dạng「友だち情報」+ tên trường tương ứng\n"
       "- Không hiển thị id nội bộ ra UI",
       note="Nguồn: Modal Filter r10-r12, r101."),

    tc("Filter theo friend info", "FUNC-001", "Normal",
       "Filter「có giá trị」/「không có giá trị」cho trường 年月日 → lọc đúng tập bạn",
       "- Trường 年月日 có 3 bạn có giá trị, 5 bạn không có giá trị",
       "1. Tạo filter điều kiện「登録情報あり」→ xem số bạn thỏa mãn và danh sách\n"
       "2. Đổi sang「登録なし」→ xem số bạn và danh sách",
       "3 bạn có giá trị · 5 bạn không",
       "- Điều kiện「có giá trị」: đúng 3 bạn, đúng danh sách\n"
       "- Điều kiện「không có giá trị」: đúng 5 bạn\n- Tổng 2 tập = toàn bộ bạn của bot",
       note="Nguồn: Modal Filter r4-r5, r58-r61, r66-r69."),

    tc("Filter theo friend info", "FUNC-DATE-001", "Normal",
       "Filter trường 年月日 theo MỐC thời gian (chỉ ngày/tháng và có năm) → lọc đúng",
       "- Trường 生年月日: U1 = 1990-05-10, U2 = 2000-05-10, U3 = 1990-06-01",
       "1. Filter theo mốc chỉ ngày/tháng = 05/10 → đọc danh sách bạn\n"
       "2. Filter theo mốc ngày/tháng/năm = 1990-05-10 → đọc danh sách",
       "U1, U2 cùng ngày/tháng 05/10 · U3 khác",
       "- Filter chỉ ngày/tháng: trả về U1 và U2 (bỏ qua năm)\n"
       "- Filter có năm: chỉ trả về U1\n- U3 không xuất hiện ở cả 2",
       note="Nguồn: Modal Filter r62-r63 + Improve filter friend info r21-r22."),

    tc("Filter theo friend info", "FUNC-DATE-001", "Normal",
       "Filter trường 年月日 theo KHOẢNG thời gian → chỉ bạn nằm trong khoảng được lấy",
       "- Trường 年月日: U1 = 2026-01-15, U2 = 2026-03-20, U3 = 2026-06-01",
       "1. Tạo filter khoảng từ 2026-01-01 đến 2026-04-30 → đọc danh sách bạn\n"
       "2. Đổi khoảng thành 2026-05-01 đến 2026-12-31 → đọc danh sách",
       "3 bạn, 2 khoảng thời gian",
       "- Khoảng 1: trả về U1 và U2\n- Khoảng 2: chỉ trả về U3\n"
       "- Bạn không có giá trị không xuất hiện ở cả 2 khoảng",
       note="Nguồn: Modal Filter r64-r65, r72-r73."),

    tc("Filter theo friend info", "FUNC-001", "Normal",
       "Filter trường ポイント theo 5 phép so sánh → lọc đúng tập bạn",
       "- Trường ポイント: U1 = 50, U2 = 100, U3 = 150, U4 chưa có giá trị",
       "1. Lần lượt tạo filter với từng phép so sánh, mốc = 100\n2. Sau mỗi lần đọc danh sách bạn thỏa mãn",
       "= 100 · ≥ 100 · > 100 · ≤ 100 · < 100 (mốc 100)",
       "- = 100 → U2\n- ≥ 100 → U2, U3\n- > 100 → U3\n- ≤ 100 → U1, U2\n- < 100 → U1\n"
       "- U4 (chưa có giá trị) không xuất hiện ở phép so sánh nào",
       note="5 phép so sánh cho 5 kết quả khác nhau nên phải tách rõ ở cột Dữ liệu test. "
            "Nguồn: Modal Filter r96-r100 + Improve filter friend info r41-r45."),

    tc("Filter theo friend info", "FUNC-001", "Normal",
       "Filter trường ポイント theo「có giá trị」/「không có giá trị」→ lọc đúng",
       "- Trường ポイント có 3 bạn có giá trị (kể cả 1 bạn giá trị 0), 4 bạn chưa có",
       "1. Filter「登録情報あり」→ đọc danh sách\n2. Filter「登録なし」→ đọc danh sách",
       "3 bạn có giá trị (1 bạn = 0 điểm) · 4 bạn chưa có",
       "- 「có giá trị」: đúng 3 bạn, BAO GỒM bạn có 0 điểm\n"
       "- 「không có giá trị」: đúng 4 bạn",
       note="Phân biệt 'giá trị 0' vs 'chưa có giá trị' — liên quan Bug #26541. Nguồn: Modal Filter r94-r95."),

    tc("Filter theo friend info", "FUNC-001", "Normal",
       "Filter trường 選択肢 theo option: chọn 1 trong các option / loại trừ option",
       "- Trường 選択肢 với option A, B, C: U1 = A, U2 = B, U3 chưa có giá trị",
       "1. Filter「bạn có 1 trong các option đã chọn」= {A} → đọc danh sách\n"
       "2. Filter loại trừ「bạn có 1 trong các option đã chọn」= {A} → đọc danh sách",
       "U1 = A · U2 = B · U3 chưa có giá trị",
       "- Điều kiện chọn A: chỉ U1\n"
       "- Điều kiện loại trừ A: U2 VÀ U3 (bao gồm cả bạn CHƯA có giá trị)",
       note="⚠️ Vế 'loại trừ bao gồm cả bạn chưa có giá trị' lấy từ corpus r36 "
            "(「user thỏa mãn bao gồm cả các friend không có friend_infor_value」) — điểm dễ hiểu nhầm. "
            "Nguồn: Improve filter friend info r35-r36. TC gốc 07/2023 → CẦN VERIFY LẠI."),

    tc("Filter theo friend info", "FUNC-001", "Normal",
       "Filter trường kiểu text theo khớp một phần / khớp toàn phần / loại trừ",
       "- Trường 記述: U1 =「東京都渋谷区」, U2 =「東京」, U3 =「大阪」, U4 chưa có giá trị",
       "1. Filter khớp MỘT PHẦN「東京」→ đọc danh sách\n2. Filter khớp TOÀN PHẦN「東京」→ đọc danh sách\n"
       "3. Filter loại trừ khớp toàn phần「東京」→ đọc danh sách\n"
       "4. Filter loại trừ khớp một phần「東京」→ đọc danh sách",
       "4 bạn, chuỗi tìm「東京」",
       "- Khớp một phần: U1, U2\n- Khớp toàn phần: chỉ U2\n"
       "- Loại trừ toàn phần: U1, U3 và U4 (gồm cả bạn chưa có giá trị)\n"
       "- Loại trừ một phần: U3 và U4",
       note="4 điều kiện cho 4 kết quả khác nhau. Nguồn: Improve filter friend info r3-r6, r28-r32."),

    tc("Filter theo friend info", "FUNC-001", "Normal",
       "Filter theo các trường mặc định (tên hệ thống, số điện thoại, email, địa chỉ) → lọc đúng",
       "- Có bạn có/không có giá trị ở từng trường mặc định",
       "1. Với mỗi trường (tên hệ thống, số điện thoại, email, 都道府県名): tạo filter khớp một phần, "
       "khớp toàn phần, có giá trị, không có giá trị\n2. Đọc danh sách bạn sau mỗi điều kiện",
       "4 trường mặc định × 4 điều kiện",
       "- Mọi điều kiện trả về đúng tập bạn tương ứng\n"
       "- Điều kiện「không có giá trị」trả về đúng các bạn chưa nhập trường đó",
       note="Nguồn: Improve filter friend info r3-r27. TC gốc 07/2023 → CẦN VERIFY LẠI."),

    tc("Filter theo friend info", "FUNC-MULTI-001", "Normal",
       "Filter nhiều điều kiện friend info cùng lúc (AND) → giao đúng tập bạn",
       "- U1 thỏa mãn cả 2 điều kiện, U2 chỉ thỏa mãn 1, U3 không thỏa mãn điều kiện nào",
       "1. Tạo filter gồm 2 điều kiện friend info (AND)\n2. Đọc số bạn thỏa mãn và danh sách\n"
       "3. Đối chiếu với danh sách tính tay",
       "Điều kiện 1: trường A có giá trị · Điều kiện 2: trường B ≥ 100",
       "- Chỉ U1 thỏa mãn\n- U2 và U3 không xuất hiện",
       note="Nguồn: Improve filter friend info r46 ('check filter cùng lúc nhiều điều kiện')."),

    tc("Filter theo friend info", "FUNC-MULTI-001", "Normal",
       "Filter OR nhiều điều kiện friend info → hợp đúng tập bạn",
       "- U1 thỏa mãn điều kiện 1, U2 thỏa mãn điều kiện 2, U3 không thỏa mãn",
       "1. Tạo filter OR gồm 2 điều kiện friend info\n2. Đọc số bạn và danh sách",
       "Điều kiện 1: trường A = option X · Điều kiện 2: trường B có giá trị",
       "- Trả về U1 và U2\n- U3 không xuất hiện\n- Số bạn thỏa mãn = 2",
       note="Nguồn: Modal Filter r74-r93 (Check filter OR) + Improve filter friend info r47-r93."),

    tc("Filter theo friend info", "REG-SHARED-001", "Normal",
       "Filter friend info hoạt động đúng ở TẤT CẢ màn có modal filter (phía web)",
       "- Cùng 1 bộ điều kiện friend info được tạo ở từng màn",
       "1. Tạo filter theo trường friend info ở từng màn trong danh sách\n"
       "2. Ở mỗi màn bấm xem số bạn thỏa mãn\n3. So sánh con số giữa các màn",
       "Màn: danh sách bạn bè · broadcast · kịch bản (step message) · remind · form answer (filter remind) · "
       "auto-reply · quản lý CSV · action schedule · phân tích chéo · filter trong dialog action",
       "- Tất cả các màn cho CÙNG số bạn thỏa mãn với cùng bộ điều kiện\n"
       "- Không màn nào lỗi khi mở modal filter hoặc khi tính số bạn",
       note="Các màn cùng 1 kết quả nên gộp 1 TC. Nguồn: Modal Filter r15-r57 + Feature #29832 r45-r131."),

    tc("Filter theo friend info", "JOB-001", "Normal",
       "Filter friend info áp dụng đúng phía JOB — bạn thỏa mãn được gửi, không thỏa mãn thì không",
       "- Broadcast, step message của kịch bản, remind, action schedule, auto-reply đều đặt filter "
       "theo trường friend info\n- Có 2 bạn thỏa mãn và 2 bạn không thỏa mãn",
       "1. Kích hoạt từng tính năng\n2. Kiểm tra LINE app của 4 bạn sau mỗi tính năng\n"
       "3. Đối chiếu số bạn đã gửi hiển thị trên màn tính năng",
       "5 tính năng × {2 bạn thỏa mãn, 2 bạn không}",
       "- Chỉ 2 bạn thỏa mãn nhận được tin nhắn/action ở mọi tính năng\n"
       "- 2 bạn không thỏa mãn KHÔNG nhận gì\n- Số bạn đã gửi hiển thị khớp với thực tế",
       env="PRODUCTION",
       note="RULE-06 + RULE-08 (job). Corpus ghi rõ logic filter phía job KHÁC nhau giữa 'filter all friend' "
            "(broadcast, remind, action schedule) và 'filter từng friend' (step message, filter action). "
            "Nguồn: Modal Filter r58-r93 + Feature #29832 r45 (block note)."),

    tc("Filter theo friend info", "COMPAT-LEGACY-001", "Normal",
       "Filter CŨ đã tạo trước đây vẫn mở được, sửa được và lọc đúng",
       "- Có filter cũ (tạo trước đợt improve) đang dùng điều kiện friend info",
       "1. Mở modal edit của filter cũ\n2. Đối chiếu điều kiện hiển thị với cấu hình ban đầu\n"
       "3. Sửa 1 điều kiện và lưu\n4. Bấm xem số bạn thỏa mãn\n5. Copy filter cũ và kiểm tra bản copy",
       "Filter cũ có điều kiện theo trường 年月日 và ポイント",
       "- Modal hiển thị đúng điều kiện cũ (đúng kiểu filter và giá trị đã set)\n"
       "- Sửa và lưu được, số bạn thỏa mãn tính đúng\n- Bản copy giữ đúng điều kiện",
       note="Nguồn: Modal Filter r14, r102 + Feature #29832 (check filter cũ)."),

    tc("Filter theo friend info", "DATA-BACKUP-001", "Normal",
       "Backup / khôi phục filter có điều kiện friend info → điều kiện giữ nguyên",
       "- Có filter mới và filter cũ dùng điều kiện friend info ở nhiều tính năng",
       "1. Thực hiện backup bot\n2. Khôi phục sang bot đích\n"
       "3. Mở modal filter của từng tính năng ở bot đích\n4. Bấm xem số bạn thỏa mãn",
       "Filter ở: kịch bản (step message) · remind · remind của form answer · auto-reply · dialog action",
       "- Toàn bộ điều kiện friend info được giữ đúng sau khôi phục\n"
       "- Filter trỏ đúng trường friend info tương ứng ở bot đích\n- Tính được số bạn thỏa mãn, không lỗi",
       env="PRODUCTION",
       note="Nguồn: Modal Filter r15-r57 (Test backup filter) + Feature #29832."),

    # ══════════════════ Chèn giá trị vào tin nhắn ══════════════════
    tc("Chèn giá trị vào tin nhắn", "MSG-001", "Normal",
       "Chèn mã giá trị friend info vào template text → khi gửi, LINE app hiển thị giá trị thật",
       "- Bạn U1 có giá trị ở trường I1\n- Template text có chèn mã giá trị của I1",
       "1. Tạo template text có chèn mã giá trị friend info\n2. Gửi test tới U1\n"
       "3. Đọc tin nhắn trên LINE app của U1\n4. Gửi cho bạn U2 CHƯA có giá trị và đọc tin",
       "U1 có giá trị · U2 chưa có giá trị",
       "- U1: tin nhắn hiển thị đúng giá trị thật, không còn mã chèn\n"
       "- U2: ghi nhận hành vi thực tế (hiển thị rỗng hay giữ mã)",
       env="PRODUCTION",
       note="RULE-06. Nguồn: Feature #29832 r164-r167. Vế U2 do AI bổ sung — cần Leader chốt."),

    tc("Chèn giá trị vào tin nhắn", "MSG-001", "Normal",
       "Mã chèn 5 trường địa chỉ hoạt động đúng ở template",
       "- Bạn U1 có đủ giá trị 5 trường địa chỉ",
       "1. Tạo template text chèn đủ 5 mã giá trị địa chỉ\n2. Gửi cho U1\n"
       "3. Đọc tin nhắn trên LINE app và đối chiếu từng giá trị với 友だち詳細",
       "5 mã: 郵便番号 · 都道府県名 · 市区町村名 · 町名/番地 · 建物名・部屋番号",
       "- Cả 5 vị trí hiển thị đúng giá trị tương ứng của U1\n"
       "- Không lẫn giá trị giữa các trường địa chỉ",
       env="PRODUCTION",
       note="Nguồn: Feature #29832 r164 (block liệt kê mã chèn của 5 trường địa chỉ)."),

    tc("Chèn giá trị vào tin nhắn", "COMPAT-LEGACY-001", "Normal",
       "Tin nhắn CŨ đang chèn mã giá trị địa chỉ cũ → vẫn thay thế đúng sau khi thêm folder địa chỉ mới",
       "- Có template/step message/broadcast/remind cũ đang chèn mã giá trị 都道府県名 (mã cũ)",
       "1. Gửi từng loại tin nhắn cũ cho bạn U1 có giá trị 都道府県名\n"
       "2. Đọc tin trên LINE app sau mỗi lần gửi",
       "4 nơi: template · step message của kịch bản · broadcast · remind",
       "- Cả 4 nơi: mã cũ vẫn thay thế đúng giá trị 都道府県名 của U1\n"
       "- Logic gửi không đổi so với trước khi thêm folder địa chỉ mới",
       env="PRODUCTION",
       note="Nguồn: Feature #29832 r167, r170, r173, r176."),

    tc("Chèn giá trị vào tin nhắn", "MSG-001", "Normal",
       "Chèn giá trị friend info trong step message của kịch bản / broadcast / remind → gửi bởi job vẫn thay thế đúng",
       "- Bạn U1 có giá trị ở trường I1 và các trường địa chỉ",
       "1. Tạo step message của kịch bản có chèn giá trị → chờ job gửi → đọc tin trên LINE app\n"
       "2. Tạo broadcast có chèn giá trị → gửi → đọc tin\n"
       "3. Tạo remind có chèn giá trị → chờ job gửi → đọc tin",
       "3 tính năng gửi qua job",
       "- Cả 3 tin nhắn hiển thị đúng giá trị thật của U1\n- Không tin nào còn mã chèn thô",
       env="PRODUCTION",
       note="RULE-08 (job). Nguồn: Feature #29832 r168-r176."),

    tc("Chèn giá trị vào tin nhắn", "MSG-001", "Normal",
       "Chèn giá trị friend info trong action text → gửi từ web và từ job đều thay thế đúng",
       "- Bạn U1 có giá trị ở trường I1",
       "1. Tạo action type text có chèn giá trị, gán vào 1 nút template\n"
       "2. Gửi trực tiếp từ web → đọc tin trên LINE app\n"
       "3. Để U1 bấm nút kích hoạt action (qua job) → đọc tin",
       "2 lối gửi: web và job",
       "- Cả 2 lối: tin nhắn hiển thị đúng giá trị thật của U1",
       env="PRODUCTION",
       note="Nguồn: Feature #29832 r177-r179."),

    tc("Chèn giá trị vào tin nhắn", "MSG-001", "Normal",
       "Chèn giá trị friend info trong message pattern của lesson / salon / form → mọi kịch bản gửi đều đúng",
       "- Lesson, salon, form đều có message pattern chèn giá trị friend info\n- Bạn U1 có giá trị",
       "1. Lesson: kích hoạt các kịch bản gửi (bạn book, admin book, yêu cầu book, duyệt, từ chối, "
       "hủy, remind, action của khóa học) → đọc tin trên LINE app\n"
       "2. Salon: lặp các kịch bản tương ứng (gồm action của nhân viên)\n"
       "3. Form: submit form, remind của form, action chẩn đoán → đọc tin",
       "Lesson 15 kịch bản · Salon 15 kịch bản · Form 3 kịch bản",
       "- Mọi tin nhắn đều hiển thị đúng giá trị thật của U1, không còn mã chèn\n"
       "- Không kịch bản nào bị lỗi gửi",
       env="PRODUCTION",
       note="Các kịch bản cùng 1 kết quả nên gộp 1 TC. Nguồn: Feature #29832 r180-r215."),

    tc("Chèn giá trị vào tin nhắn", "DATA-BACKUP-001", "Normal",
       "Backup / khôi phục action và template có chèn giá trị friend info → giữ đúng mã chèn",
       "- Bot nguồn có action, template và message pattern chèn giá trị friend info",
       "1. Backup bot nguồn → khôi phục sang bot đích\n"
       "2. Ở bot đích mở action và template, đối chiếu nội dung với bot nguồn\n"
       "3. Gửi thử cho 1 bạn ở bot đích có giá trị friend info → đọc tin trên LINE app\n"
       "4. Kiểm tra message pattern của lesson/salon/form",
       "Action · template · message pattern (lesson, salon, form)",
       "- Nội dung có mã chèn được giữ nguyên sau khôi phục\n"
       "- Gửi thử ở bot đích: giá trị được thay thế đúng theo dữ liệu của bot đích\n"
       "- Ghi nhận nơi nào KHÔNG được backup (theo corpus: message pattern của lesson/salon)",
       env="PRODUCTION",
       note="Nguồn: Feature #29832 r216-r220 (r218-r219 ghi 'không có backup' cho message pattern lesson/salon)."),
]
