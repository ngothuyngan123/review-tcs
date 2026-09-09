# -*- coding: utf-8 -*-
"""FA-001 Chat 1:1 — Nhóm 1: vào màn, filter, tìm kiếm, danh sách friend/group, load more."""
from _common import tc

BOT = "- Đăng nhập admin (user chính), đang chọn bot A\n- Màn hình /basic/chat-v3"
BOT_DATA = (BOT + "\n- Bot A có ≥25 friend để phát sinh load more (mỗi page 20)\n"
            "- Có ≥3 friend chưa xác nhận, ≥3 friend đã xác nhận, ≥1 friend đang ẩn,\n"
            "  ≥1 friend đã đặt lịch gửi, ≥1 nhóm LINE")
TAGSET = ("- Folder tag F1 có tag T1, T2; folder tag F2 có tag T3\n"
          "- Friend A gắn T1; friend B gắn T1+T2; friend C gắn T3; friend D không tag")

S1 = [
    # ═══════════════ Vào màn & layout 3 cột ═══════════════
    tc("Vào màn & layout 3 cột", "UI-001", "Normal",
       "Mở /basic/chat-v3 — hiển thị đủ 3 cột: danh sách bạn bè / khung hội thoại / panel thông tin",
       BOT_DATA,
       "1. Đăng nhập admin, chọn bot A\n"
       "2. Vào menu メインサービス → 1:1チャット\n"
       "3. Quan sát 3 cột của màn hình ở độ phân giải 1366px",
       "Màn hình 1366×768",
       "- Cột trái (~25%): ô tìm kiếm + dropdown filter + icon 絞り込み + danh sách bạn bè\n"
       "- Cột giữa (~45%): header hội thoại + lịch sử tin nhắn + ô nhập tin\n"
       "- Cột phải (~30%): panel thông tin bạn bè với 5 tab (基本情報 / 友だち情報 / タグ管理 / フォーム回答 / メモ)\n"
       "- Không vỡ layout, không tràn ngang, icon không bị vỡ",
       note="Nguồn: Leftbar+Header r3 「CHECK MÀN 1366」. Evidence: ảnh full màn 1366px. "
            "Feature #35547 mục 4 có ghi lỗi icon vỡ ở màn 14 inch → cần chụp cả 1366 và 1920"),

    tc("Vào màn & layout 3 cột", "FUNC-001", "Normal",
       "Mở màn Chat lần đầu — tự động chọn hội thoại đầu tiên trong danh sách",
       BOT_DATA,
       "1. Mở /basic/chat-v3\n2. Quan sát hội thoại được chọn sẵn ở cột giữa\n"
       "3. Đối chiếu với dòng đầu tiên của danh sách bạn bè",
       "Danh sách sắp xếp mặc định: bookmark trước, sau đó theo tin nhắn cuối",
       "- Hội thoại đầu tiên trong danh sách được auto select (highlight)\n"
       "- Cột giữa hiển thị đúng lịch sử chat + tên + avatar của bạn bè đó\n"
       "- Cột phải hiển thị đúng thông tin của bạn bè đó",
       note="Nguồn: Content: Hiển thị msg r1597 (TC029 của Bug KH #36859)"),

    tc("Vào màn & layout 3 cột", "FUNC-001", "Normal",
       "Mở màn Chat khi bản ghi đầu danh sách là nhóm LINE — auto select đúng nhóm",
       BOT_DATA + "\n- Nhóm LINE G1 có tin nhắn mới nhất (đứng đầu danh sách)",
       "1. Cho nhóm G1 gửi tin đến bot để G1 lên đầu danh sách\n2. Reload /basic/chat-v3\n"
       "3. Quan sát hội thoại được auto select",
       "G1 = nhóm LINE, conversation_kind = 1",
       "- Auto select đúng nhóm G1, KHÔNG nhảy sang friend khác\n"
       "- Header hiển thị tên nhóm + icon nhóm, không hiển thị tên friend",
       note="Nguồn: Content: Hiển thị msg r1598 (TC030). Đây là biến thể của Bug KH #36859"),

    tc("Vào màn & layout 3 cột", "UI-002", "Normal",
       "Bạn bè chưa có tin nhắn nào — khung hội thoại hiển thị empty state",
       BOT + "\n- Friend E vừa kết bạn, chưa có tin nhắn nào ngoài message hệ thống",
       "1. Mở /basic/chat-v3\n2. Chọn friend E ở danh sách\n3. Quan sát cột giữa và dòng của E ở cột trái",
       "Friend E: 0 tin nhắn hội thoại",
       "- Cột trái: dòng của E hiển thị tên ở giữa vùng avatar, không có dòng tin nhắn cuối\n"
       "- Cột giữa: không có bong bóng tin nhắn nào (chỉ có message hệ thống kết bạn nếu có)\n"
       "- Không lỗi JS, không màn trắng",
       note="Nguồn: Leftbar+Header r155 (trang 11)"),

    tc("Vào màn & layout 3 cột", "REG-URL-001", "Normal",
       "Mở màn chat 1:1 từ màn my_page của friend — hiển thị đúng lịch sử của friend đó",
       BOT + "\n- Friend F đã có ≥10 tin nhắn\n- Đang ở màn my_page (chi tiết bạn bè) của F",
       "1. Ở màn my_page của F, click nút mở chat 1:1\n"
       "2. Quan sát cột giữa và header hội thoại\n3. Reload trang, kiểm tra lại",
       "Friend F",
       "- Chuyển sang /basic/chat-v3 và tự chọn đúng hội thoại của F\n"
       "- Hiển thị đúng lịch sử chat và đúng tên/avatar của F\n"
       "- Sau reload vẫn đúng F",
       note="Nguồn: Test fix bug Kh r1604 (TC036) + Bug KH #33113"),

    tc("Vào màn & layout 3 cột", "DATA-TEXT-001", "Abnormal",
       "Mở chat 1:1 từ my_page khi tên friend chứa ký tự đặc biệt — không lỗi, hiển thị đủ lịch sử",
       BOT + "\n- Tạo/sửa tên các friend theo danh sách ở cột Dữ liệu test, mỗi tên 1 friend, mỗi friend có ≥3 tin nhắn",
       "1. Vào my_page từng friend trong danh sách\n2. Click mở chat 1:1\n"
       "3. Kiểm tra lịch sử chat và tên hiển thị ở header",
       "Lần lượt: `a/b` · `a*b` · `a\\b` · `a:b` · `a?b` · ``a`~!@#$%^&()+=_<>{}[].,b`` và ký tự gạch đứng · "
       "`まことボット智恵助` · `チャット・ボットーさん` · `【テスト】（木）～！＠＃＄％＾＆＊` · `■FLOA Japan.` · "
       "`∞TO.KI.YO∞` · `《Teoria -ﾃｵﾘｱ-》` · `YOKO 3y's` · `AIボット🤖_Ver1` · `こーだい/プレゼント専用🎁` · "
       "`戸張賢治🏀&🍻` · `Nguyễn Văn Đức` · `スーパーインテリジェントチくお願いします`",
       "- Với TẤT CẢ tên trên: mở được màn chat 1:1, hiển thị đủ lịch sử chat, tên header đúng nguyên văn\n"
       "- Không màn trắng, không lỗi JS ở console\n"
       "- Ký tự `&` hiển thị đúng, không thành `&amp;`",
       note="Gộp 19 điểm dữ liệu vì CÙNG 1 kết quả mong đợi. Nguồn: Test fix bug Kh r66-r84 (Bug KH #33113 12/2025)"),

    tc("Vào màn & layout 3 cột", "REG-URL-001", "Normal",
       "Mở chat 1:1 từ màn chi tiết booking event và từ màn talk list",
       BOT + "\n- Friend G có 1 booking event và ≥1 tin nhắn ở talk list",
       "1. Vào màn chi tiết booking event của G → click mở chat 1:1 → kiểm tra\n"
       "2. Quay lại, vào màn talk list → click vào tin nhắn của G để mở chat 1:1 → kiểm tra",
       "Friend G",
       "- Cả 2 đường vào đều mở đúng hội thoại của G, hiển thị đủ lịch sử chat và đúng tên/avatar",
       note="Gộp 2 điểm vì cùng kết quả. Nguồn: Test fix bug Kh r85, r86"),

    tc("Vào màn & layout 3 cột", "SEC-001", "Abnormal",
       "Lỗi JavaScript khi render màn chat — có notify Chatwork, không im lặng",
       BOT + "\n- Dev bật cờ giả lập lỗi JS ở màn chat (theo cách của Bug #31202)",
       "1. Mở /basic/chat-v3 khi đang bật giả lập lỗi\n2. Quan sát màn hình\n"
       "3. Kiểm tra group Chatwork 「SNS Line Exception Javascript」",
       "Bot A, account admin",
       "- Có bản tin notify Chatwork ở group 「SNS Line Exception Javascript」\n"
       "- Nội dung notify chứa email của account đang thao tác\n"
       "- Không nuốt lỗi im lặng",
       env="STAGING", spec="Spec không ghi",
       note="Nguồn: Test fix bug Kh r63 + Leftbar+Header r506-r540 (Bug #31202). "
            "Spec chat-11 KHÔNG mô tả cơ chế notify Chatwork này"),

    # ═══════════════ Filter danh sách bạn bè ═══════════════
    tc("Filter danh sách bạn bè", "UI-003", "Normal",
       "Dropdown filter — giá trị mặc định và đủ 5 lựa chọn",
       BOT_DATA,
       "1. Mở /basic/chat-v3\n2. Đọc giá trị đang hiển thị trên dropdown filter\n3. Click mở dropdown, đọc danh sách lựa chọn",
       "Bot A vừa mở màn lần đầu",
       "- Mặc định hiển thị 「全ての友だち（非表示除く）」\n"
       "- Dropdown có đúng 5 lựa chọn, đúng thứ tự: 全ての友だち（非表示除く） / 未確認 / 確認済み / 非表示中 / 送信予約中の友だち",
       note="Nguồn: Leftbar+Header r6-r7"),

    tc("Filter danh sách bạn bè", "LIST-001", "Normal",
       "Filter 全ての友だち（非表示除く） — hiện mọi bạn bè trừ bạn bè đang ẩn",
       BOT_DATA,
       "1. Chọn filter 全ての友だち（非表示除く）\n2. Đếm số bạn bè hiển thị, cuộn hết danh sách\n"
       "3. Đối chiếu với friend đang ẩn đã chuẩn bị",
       "Bot A có 25 friend, trong đó 2 friend đang ẩn",
       "- Danh sách hiện 23 friend (25 − 2 friend ẩn)\n"
       "- 2 friend đang ẩn KHÔNG xuất hiện trong danh sách",
       note="Nguồn: Leftbar+Header r69, r148"),

    tc("Filter danh sách bạn bè", "LIST-001", "Normal",
       "Filter 未確認 — chỉ hiện bạn bè còn tin nhắn chưa xác nhận",
       BOT_DATA,
       "1. Chọn filter 未確認\n2. Ghi lại danh sách friend hiển thị\n"
       "3. Với 1 friend trong danh sách: mở hội thoại và bấm xác nhận\n4. Chọn lại filter 未確認",
       "3 friend chưa xác nhận: A có 1 tin chưa đọc, B có 2 tin, C có 5 tin",
       "- Bước 2: hiện đủ cả 3 friend A, B, C — KHÔNG chỉ hiện friend có đúng 1 tin chưa đọc\n"
       "- Bước 4: friend vừa xác nhận biến mất khỏi danh sách, còn 2 friend",
       spec="Đã hỏi leader",
       note="MT-19: spec ghi điều kiện `confirm_count = 1` (feature-spec.md:121) — nếu đúng thì friend có 2-5 tin "
            "chưa đọc sẽ bị lọt. Nguồn: Leftbar+Header r70 + SpecImprove #33731 r74 + improve count comfirm_message r3"),

    tc("Filter danh sách bạn bè", "LIST-001", "Normal",
       "Filter 確認済み — chỉ hiện bạn bè đã xác nhận hết tin nhắn",
       BOT_DATA,
       "1. Chọn filter 確認済み\n2. Đối chiếu danh sách với các friend đã xác nhận\n"
       "3. Cho 1 friend trong danh sách gửi tin mới đến bot\n4. Chọn lại filter 確認済み",
       "3 friend đã xác nhận (confirm_count = 0)",
       "- Bước 2: chỉ hiện 3 friend đã xác nhận\n"
       "- Bước 4: friend vừa nhận tin mới rời khỏi danh sách 確認済み",
       note="Nguồn: Leftbar+Header r71"),

    tc("Filter danh sách bạn bè", "LIST-001", "Normal",
       "Filter 非表示中 — chỉ hiện bạn bè đang bị ẩn",
       BOT_DATA,
       "1. Chọn filter 非表示中\n2. Đối chiếu danh sách hiển thị\n"
       "3. Kiểm tra DB: SELECT id, is_hide FROM conversation WHERE bot_id = <A>",
       "2 friend đang ẩn",
       "- Danh sách chỉ hiện đúng 2 friend đang ẩn\n"
       "- Đúng 2 bản ghi conversation có is_hide = 1, khớp với 2 friend hiển thị",
       note="Verify 2 tầng DB + màn hình (RULE-07). Nguồn: Leftbar+Header r72, r149"),

    tc("Filter danh sách bạn bè", "LIST-001", "Normal",
       "Filter 送信予約中の友だち — lọc theo trạng thái lịch gửi, KHÔNG theo ngày gửi",
       BOT_DATA + "\n- Friend H đặt lịch gửi vào NGÀY MAI (chưa gửi)\n"
                  "- Friend I đặt lịch gửi vào 10 NGÀY SAU (chưa gửi)\n"
                  "- Friend J đã có lịch nhưng đã gửi xong",
       "1. Chọn filter 送信予約中の友だち\n2. Đối chiếu danh sách hiển thị\n"
       "3. Kiểm tra DB: SELECT conversation_id, status FROM schedule_send_chat WHERE bot_id = <A>",
       "H (lịch ngày mai), I (lịch 10 ngày sau), J (đã gửi)",
       "- Danh sách hiện cả H và I — không phụ thuộc lịch gần hay xa\n"
       "- KHÔNG hiện J (đã gửi xong)\n"
       "- Điều kiện lọc là trạng thái lịch còn chờ gửi, không phải khoảng ngày",
       note="Nguồn: Leftbar+Header r73 — TC gốc ghi rõ 「check hiển thị theo status không check theo ngày」"),

    tc("Filter danh sách bạn bè", "LIST-001", "Normal",
       "Filter グループ — chỉ hiện nhóm LINE, không lẫn friend cá nhân",
       BOT_DATA + "\n- Bot A đang ở trong ≥2 nhóm LINE",
       "1. Chọn filter グループ\n2. Đối chiếu danh sách hiển thị\n"
       "3. Kiểm tra DB: SELECT id, conversation_kind FROM conversation WHERE bot_id = <A>",
       "2 nhóm LINE + 23 friend cá nhân",
       "- Danh sách chỉ hiện 2 nhóm LINE, mỗi dòng có icon nhóm\n"
       "- Đúng 2 bản ghi conversation có conversation_kind = 1",
       note="Verify DB + màn hình. Nguồn: Leftbar+Header r79, r521 + Group chat r3"),

    tc("Filter danh sách bạn bè", "COMPAT-LEGACY-001", "Normal",
       "5 filter chạy đúng trên cả bot cũ (dữ liệu trước cải tiến) và bot mới",
       BOT + "\n- Bot CŨ (tạo trước đợt improve 10/2024, có dữ liệu hội thoại cũ)\n- Bot MỚI vừa tạo, có ≥5 friend",
       "1. Ở bot cũ: chạy lần lượt 5 filter, ghi lại số friend mỗi filter\n"
       "2. Chuyển sang bot mới: lặp lại bước 1\n3. Đối chiếu với dữ liệu thực tế của từng bot",
       "5 filter: 全ての友だち（非表示除く） / 未確認 / 確認済み / 非表示中 / 送信予約中の友だち",
       "- Cả 2 bot: mỗi filter trả về đúng tập friend tương ứng, không lỗi, không danh sách rỗng bất thường",
       spec="Spec không ghi",
       note="Gộp vì cùng kết quả. Nguồn: Leftbar+Header r69-r73 (cột 'check bot mới, bot cũ')"),

    tc("Filter danh sách bạn bè", "UI-003", "Normal",
       "Icon 絞り込み đổi màu khi đang áp dụng bộ lọc tag/trạng thái",
       BOT_DATA + "\n" + TAGSET,
       "1. Khi chưa có filter nào: quan sát màu icon filter bên phải và menu của icon\n"
       "2. Áp dụng filter tag T1 → quan sát lại màu icon và menu",
       "Tag T1",
       "- Khi CHƯA có filter: icon màu xám; menu chỉ có 2 mục 「絞り込み」và「全て確認済みに変更」\n"
       "- Khi ĐANG có filter: icon chuyển màu xanh; menu có 3 mục 「絞り込み」「絞り込みを削除」「全て確認済みに変更」",
       note="Tách riêng vì 2 state có expected khác nhau. Nguồn: Leftbar+Header r8, r9, r10"),

    tc("Filter danh sách bạn bè", "STATE-CLEAN-001", "Normal",
       "絞り込みを削除 — xoá bộ lọc, danh sách trở về mặc định",
       BOT_DATA + "\n" + TAGSET + "\n- Đang áp dụng filter tag T1 (danh sách chỉ còn A, B)",
       "1. Click icon filter bên phải → chọn 絞り込みを削除\n2. Quan sát danh sách bạn bè và màu icon filter\n"
       "3. Mở lại modal 絞り込み kiểm tra mục đã chọn",
       "Filter đang là tag T1",
       "- Bộ lọc bị xoá ngay, không hiện popup xác nhận\n"
       "- Danh sách trở về mặc định (đủ 23 friend của filter 全ての友だち)\n"
       "- Icon filter về màu xám; trong modal 絞り込み mục 選択済みの項目 hiện 選択されていません",
       note="Nguồn: Leftbar+Header r16, r17, r23"),

    # ═══════════════ Modal 絞り込み — tag & trạng thái ═══════════════
    tc("Modal 絞り込み — tag & trạng thái", "UI-001", "Normal",
       "Modal 絞り込み — hiển thị đủ folder/tag và đủ danh sách 対応ステータス, có scroll khi nhiều",
       BOT + "\n" + TAGSET + "\n- Bot A có ≥8 対応ステータス (5 mặc định + 3 tự tạo)",
       "1. Click icon filter → 絞り込み\n2. Ở tab lọc theo tag: kiểm tra đủ folder, đúng thứ tự, đủ tag trong từng folder, thử cuộn\n"
       "3. Chuyển sang phần lọc theo 対応ステータス: kiểm tra đủ và đúng thứ tự, thử cuộn",
       "2 folder tag (F1: T1,T2 · F2: T3) · 8 対応ステータス",
       "- Tab tag: hiện đủ 2 folder đúng thứ tự như màn Quản lý thẻ, đủ 3 tag trong đúng folder, danh sách dài thì có scroll\n"
       "- Phần 対応ステータス: hiện đủ 8 status đúng thứ tự như màn cài đặt, danh sách dài thì có scroll",
       note="Nguồn: Leftbar+Header r22-r25, r46"),

    tc("Modal 絞り込み — tag & trạng thái", "DATA-REF-001", "Normal",
       "Modal 絞り込み luôn lấy dữ liệu mới nhất sau khi thêm/sửa/xoá/sắp xếp tag và status",
       BOT + "\n" + TAGSET,
       "1. Mở modal 絞り込み, ghi lại danh sách tag và status\n"
       "2. Sang màn Quản lý thẻ: thêm tag T4, đổi tên T1 → T1_new, xoá T3, đổi thứ tự folder\n"
       "3. Sang màn cài đặt chat: thêm status S9, đổi tên 1 status, xoá 1 status\n"
       "4. Quay lại chat 1:1, mở lại modal 絞り込み",
       "Tag T4 mới · T1 đổi tên · T3 bị xoá · status S9 mới",
       "- Modal hiển thị T4 và S9 mới thêm\n- T1 hiện tên mới T1_new\n"
       "- T3 và status đã xoá không còn trong modal\n- Thứ tự folder khớp thứ tự vừa sắp xếp",
       note="Nguồn: Leftbar+Header r26, r47"),

    tc("Modal 絞り込み — tag & trạng thái", "FUNC-002", "Normal",
       "Lọc theo tag — điều kiện OR: chọn nhiều tag khác folder, friend chỉ cần có 1 tag là hiện",
       BOT + "\n" + TAGSET,
       "1. Mở modal 絞り込み → tab điều kiện OR\n2. Tick T1 (folder F1) và T3 (folder F2)\n"
       "3. Click 絞り込み表示\n4. Đối chiếu danh sách friend",
       "T1 (A, B có) · T3 (C có) · D không tag",
       "- Danh sách hiện A, B, C (có ít nhất 1 trong 2 tag)\n- KHÔNG hiện D\n- Modal đóng lại, icon filter chuyển xanh",
       note="Nguồn: Leftbar+Header r28-r30"),

    tc("Modal 絞り込み — tag & trạng thái", "FUNC-002", "Normal",
       "Lọc theo tag — điều kiện AND: friend phải có ĐỦ tất cả tag đã chọn",
       BOT + "\n" + TAGSET,
       "1. Mở modal 絞り込み → tab điều kiện AND\n2. Tick T1 và T2 (cùng folder F1)\n"
       "3. Click 絞り込み表示\n4. Lặp lại với T1 (F1) + T3 (F2)",
       "T1: A, B · T2: B · T3: C",
       "- Với T1+T2: chỉ hiện B (friend duy nhất có cả 2 tag), KHÔNG hiện A\n"
       "- Với T1+T3: không friend nào có cả 2 tag → danh sách rỗng, không lỗi",
       note="Tách khỏi TC OR vì kết quả mong đợi khác hẳn. Nguồn: Leftbar+Header r37-r39"),

    tc("Modal 絞り込み — tag & trạng thái", "STATE-CLEAN-001", "Abnormal",
       "Chọn tag rồi đóng modal bằng X — không áp dụng, modal reset về trạng thái trước",
       BOT + "\n" + TAGSET + "\n- Chưa áp dụng filter nào",
       "1. Mở modal 絞り込み, tick T1\n2. KHÔNG click 絞り込み表示, click X đóng modal\n"
       "3. Quan sát danh sách friend\n4. Mở lại modal, kiểm tra tick",
       "Tag T1",
       "- Danh sách friend không đổi (vẫn đủ mọi friend)\n- Icon filter vẫn xám\n"
       "- Mở lại modal: T1 KHÔNG còn tick, modal về trạng thái ban đầu",
       note="Nguồn: Leftbar+Header r27, r36 (áp dụng cho cả tab OR và AND)"),

    tc("Modal 絞り込み — tag & trạng thái", "STATE-DEP-001", "Abnormal",
       "Đang có filter tag, bỏ tick hết rồi 絞り込み表示 — filter trống, hiện lại toàn bộ",
       BOT + "\n" + TAGSET + "\n- Đang áp dụng filter tag T1",
       "1. Mở modal 絞り込み\n2. Bỏ tick T1, không chọn tag mới\n3. Click 絞り込み表示",
       "Từ T1 → không tag nào",
       "- Bộ lọc trở về trống\n- Danh sách hiện lại toàn bộ friend\n- Icon filter về màu xám",
       note="Nguồn: Leftbar+Header r34, r43"),

    tc("Modal 絞り込み — tag & trạng thái", "STATE-DEP-001", "Abnormal",
       "Đang có filter tag, bỏ tick rồi đóng bằng X — GIỮ NGUYÊN filter cũ",
       BOT + "\n" + TAGSET + "\n- Đang áp dụng filter tag T1 (danh sách chỉ còn A, B)",
       "1. Mở modal 絞り込み\n2. Bỏ tick T1\n3. Click X đóng modal (không bấm 絞り込み表示)\n"
       "4. Quan sát danh sách friend và mở lại modal",
       "Từ T1 → bỏ tick → đóng X",
       "- Danh sách VẪN chỉ có A, B (filter T1 cũ được giữ)\n- Icon filter vẫn xanh\n- Mở lại modal: T1 vẫn đang tick",
       note="Cặp đối lập với TC trên — mỗi kết quả 1 TC riêng. Nguồn: Leftbar+Header r32, r41"),

    tc("Modal 絞り込み — tag & trạng thái", "FUNC-002", "Normal",
       "Đổi tag đang lọc: bỏ T1 chọn T2 → danh sách theo tag mới",
       BOT + "\n" + TAGSET + "\n- Đang áp dụng filter tag T1",
       "1. Mở modal 絞り込み\n2. Bỏ tick T1, tick T2\n3. Click 絞り込み表示",
       "T1: A, B · T2: B",
       "- Danh sách chỉ còn B (friend có T2), A biến mất\n- Mở lại modal: chỉ T2 đang tick",
       note="Nguồn: Leftbar+Header r33, r42"),

    tc("Modal 絞り込み — tag & trạng thái", "FUNC-002", "Normal",
       "Lọc theo 対応ステータス điều kiện OR — chọn nhiều status, friend có 1 trong số đó là hiện",
       BOT + "\n- Friend A có status 対応中, B có status フォロー, C không có status",
       "1. Mở modal 絞り込み\n2. Ở phần 対応ステータス tab điều kiện OR: tick 対応中 và フォロー\n"
       "3. Click 絞り込み表示",
       "対応中 (A) · フォロー (B) · C không status",
       "- Ở tab OR, 対応ステータス hiển thị dạng checkbox (chọn được nhiều)\n"
       "- Danh sách hiện A và B, KHÔNG hiện C",
       note="Nguồn: Leftbar+Header r48-r50"),

    tc("Modal 絞り込み — tag & trạng thái", "UI-INPUT-001", "Boundary",
       "Lọc theo 対応ステータス điều kiện AND — chỉ chọn được 1 status (radio)",
       BOT + "\n- Friend A có status 対応中, B có status フォロー",
       "1. Mở modal 絞り込み → phần 対応ステータス, chuyển sang tab điều kiện AND\n"
       "2. Thử tick 対応中 rồi tick tiếp フォロー\n3. Click 絞り込み表示",
       "Thử chọn 2 status ở tab AND",
       "- Ở tab AND, 対応ステータス hiển thị dạng radio: tick フォロー thì 対応中 tự bỏ tick\n"
       "- Chỉ áp dụng được 1 status; danh sách hiện friend có status được chọn cuối",
       note="Khác hẳn tab OR (checkbox) → tách TC riêng. Nguồn: Leftbar+Header r55-r58"),

    tc("Modal 絞り込み — tag & trạng thái", "STATE-DEP-001", "Abnormal",
       "Tab AND của status: bỏ tick status đang lọc → filter trống dù trước đó đã có status",
       BOT + "\n- Đang lọc theo status 対応中 ở tab AND",
       "1. Mở modal 絞り込み → tab AND\n2. Bỏ tick 対応中\n3. Click 絞り込み表示",
       "Từ 対応中 → bỏ tick",
       "- Bộ lọc status về trống\n- Danh sách hiện lại toàn bộ friend (KHÔNG giữ status cũ)",
       spec="Đã hỏi leader",
       note="Hành vi NGƯỢC với tab OR của tag (giữ filter cũ khi đóng X) và khác tab OR của status. "
            "Nguồn: Leftbar+Header r59, r60 vs r51, r52 — cần Leader chốt là chủ ý hay lỗi"),

    tc("Modal 絞り込み — tag & trạng thái", "FUNC-MULTI-001", "Normal",
       "Kết hợp filter tag và filter 対応ステータス — quan hệ AND giữa 2 nhóm",
       BOT + "\n" + TAGSET + "\n- Friend A: tag T1 + status 対応中\n- Friend B: tag T1+T2, không status\n"
       "- Friend C: tag T3 + status 対応中",
       "1. Mở modal 絞り込み\n2. Chọn tag T1 (điều kiện OR)\n3. Chọn status 対応中 (điều kiện OR)\n"
       "4. Click 絞り込み表示",
       "Tag T1 + status 対応中",
       "- Chỉ hiện A (thoả cả 2 nhóm điều kiện)\n- KHÔNG hiện B (thiếu status), KHÔNG hiện C (thiếu tag)",
       note="Nguồn: Leftbar+Header r65, r66"),

    tc("Modal 絞り込み — tag & trạng thái", "REG-SPEC-001", "Abnormal",
       "Tổ hợp chéo tag OR + status AND (và ngược lại) — hành vi chưa được xác nhận",
       BOT + "\n" + TAGSET + "\n- Friend A: tag T1 + status 対応中\n- Friend B: tag T2 + status フォロー",
       "1. Chọn tag ở tab OR (T1, T2)\n2. Chọn status ở tab AND (対応中)\n3. Click 絞り込み表示, ghi lại kết quả\n"
       "4. Làm ngược lại: tag ở tab AND, status ở tab OR, ghi lại kết quả",
       "Tổ hợp 1: tag OR + status AND · Tổ hợp 2: tag AND + status OR",
       "- Ghi nhận kết quả thực tế của cả 2 tổ hợp và đối chiếu với quyết định của Leader ở MT-12\n"
       "- Nếu hệ thống chưa hỗ trợ: phải chặn rõ ràng hoặc thông báo, KHÔNG trả kết quả sai âm thầm",
       spec="Đã hỏi leader",
       note="MT-12: TC gốc ghi 「hiện tại mình chưa làm 2 case này」→ chưa ai xác nhận hành vi. "
            "Nguồn: Leftbar+Header r67, r68"),

    tc("Modal 絞り込み — tag & trạng thái", "CONC-001", "Abnormal",
       "Double click nút 絞り込み表示 — chỉ áp dụng 1 lần",
       BOT + "\n" + TAGSET,
       "1. Mở modal 絞り込み, tick T1\n2. Double click nhanh nút 絞り込み表示\n"
       "3. Quan sát modal và danh sách friend, mở DevTools → Network",
       "Double click trong < 300ms",
       "- Chỉ phát sinh 1 request lấy danh sách bạn bè\n- Modal đóng 1 lần, danh sách áp dụng đúng filter T1\n"
       "- Không nhân đôi dòng, không lỗi JS",
       note="Nguồn: Leftbar+Header r35, r44, r63"),

    # ═══════════════ 全て確認済みに変更 ═══════════════
    tc("全て確認済みに変更", "UI-004", "Normal",
       "Popup xác nhận của 全て確認済みに変更 — không bấm 決定 thì không có gì đổi",
       BOT_DATA,
       "1. Ghi lại số friend chưa xác nhận\n2. Click icon filter → 全て確認済みに変更\n"
       "3. Quan sát popup xác nhận\n4. Đóng popup mà KHÔNG bấm 決定\n5. Kiểm tra lại danh sách",
       "3 friend chưa xác nhận",
       "- Popup xác nhận hiển thị đúng thiết kế\n"
       "- Sau khi đóng: 3 friend vẫn ở trạng thái chưa xác nhận, badge số tin chưa đọc không đổi",
       note="Nguồn: Leftbar+Header r11, r12"),

    tc("全て確認済みに変更", "BULK-001", "Normal",
       "全て確認済みに変更 khi KHÔNG có filter — xác nhận toàn bộ bạn bè của bot",
       BOT_DATA,
       "1. Chọn filter 全ての友だち（非表示除く）, không áp dụng tag/status\n"
       "2. Click icon filter → 全て確認済みに変更 → 決定\n"
       "3. Quan sát danh sách, badge ở menu 1:1チャット\n"
       "4. Kiểm tra DB: SELECT confirm_count FROM conversation WHERE bot_id=<A>; SELECT count_user_unconfirm FROM bots WHERE id=<A>",
       "3 friend chưa xác nhận (1 tin, 2 tin, 5 tin)",
       "- Toàn bộ friend chuyển sang đã xác nhận, không dòng nào còn chấm xanh\n"
       "- Badge số tin chưa đọc ở menu 1:1チャット về 0 (không hiển thị)\n"
       "- DB: mọi conversation có confirm_count = 0; bots.count_user_unconfirm = 0",
       note="Verify 3 tầng DB + màn hình + badge menu (RULE-07). Nguồn: Leftbar+Header r14, r543 (SpecImprove #35144)"),

    tc("全て確認済みに変更", "BULK-001", "Normal",
       "全て確認済みに変更 khi ĐANG filter — chỉ xác nhận bạn bè thoả filter",
       BOT_DATA + "\n" + TAGSET + "\n- A (tag T1) và D (không tag) đều đang chưa xác nhận",
       "1. Áp dụng filter tag T1 (danh sách còn A, B)\n"
       "2. Click 全て確認済みに変更 → 決定\n3. Xoá filter, quan sát trạng thái của A và D\n"
       "4. Kiểm tra DB confirm_count của A và D + bots.count_user_unconfirm",
       "A: tag T1, 2 tin chưa đọc · D: không tag, 3 tin chưa đọc",
       "- A chuyển sang đã xác nhận (confirm_count = 0)\n"
       "- D VẪN chưa xác nhận (confirm_count = 3), badge của D không đổi\n"
       "- bots.count_user_unconfirm giảm đúng số friend đã được xác nhận, không về 0",
       note="Nguồn: Leftbar+Header r15, r544-r550 (SpecImprove #35144 — bug cũ là set count_user_unconfirm = 0 luôn)"),

    tc("全て確認済みに変更", "BULK-001", "Normal",
       "全て確認済みに変更 áp dụng đúng với từng loại filter danh sách",
       BOT_DATA + "\n- Mỗi loại filter đều có ≥1 friend chưa xác nhận",
       "1. Với mỗi filter trong cột Dữ liệu test: chọn filter → 全て確認済みに変更 → 決定\n"
       "2. Sau mỗi lần: kiểm tra friend thoả filter đã xác nhận, friend ngoài filter giữ nguyên\n"
       "3. Kiểm tra bots.count_user_unconfirm sau mỗi lần",
       "5 filter: 未確認 · 確認済み · 非表示中 · 送信予約中の友だち · グループ (test lần lượt, reset dữ liệu giữa các lần)",
       "- Mỗi lần: chỉ friend/nhóm thoả filter được xác nhận; friend ngoài filter giữ nguyên confirm_count\n"
       "- bots.count_user_unconfirm cập nhật đúng theo số thực tế đã xác nhận",
       note="Gộp 5 điểm vì CÙNG kết quả mong đợi. Nguồn: Leftbar+Header r544-r548 + Test fix bug Kh r132-r136"),

    tc("全て確認済みに変更", "BULK-001", "Normal",
       "全て確認済みに変更 khi đang tìm kiếm — chỉ xác nhận bạn bè khớp từ khoá",
       BOT_DATA,
       "1. Nhập từ khoá tìm kiếm khớp 2 friend (trong đó có friend chưa xác nhận)\n"
       "2. Click 全て確認済みに変更 → 決定\n3. Xoá từ khoá, kiểm tra các friend còn lại",
       "Từ khoá khớp 2 friend; ngoài danh sách còn 1 friend chưa xác nhận khác",
       "- 2 friend khớp từ khoá được xác nhận\n- Friend ngoài kết quả tìm kiếm vẫn chưa xác nhận",
       note="Nguồn: Leftbar+Header r551"),

    tc("全て確認済みに変更", "BULK-001", "Normal",
       "全て確認済みに変更 khi kết hợp tìm kiếm + nhiều filter cùng lúc",
       BOT_DATA + "\n" + TAGSET,
       "1. Với mỗi tổ hợp ở cột Dữ liệu test: áp dụng đủ điều kiện → 全て確認済みに変更 → 決定\n"
       "2. Kiểm tra chỉ friend thoả TẤT CẢ điều kiện được xác nhận",
       "Tổ hợp: (未確認 + tag) · (非表示中 + 対応ステータス) · (search + tag) · (search + 未確認) · "
       "(search + 送信予約中 + tag) · (グループ + 対応ステータス)",
       "- Mỗi tổ hợp: chỉ friend thoả đủ mọi điều kiện được xác nhận\n"
       "- Friend thoả một phần điều kiện KHÔNG bị xác nhận",
       note="Gộp 6 tổ hợp vì cùng kết quả. Nguồn: Leftbar+Header r552-r557"),

    tc("全て確認済みに変更", "BULK-001", "Abnormal",
       "全て確認済みに変更 khi filter không khớp hội thoại nào — không lỗi, không đụng dữ liệu",
       BOT_DATA + "\n" + TAGSET,
       "1. Áp dụng filter tag T3 kết hợp status không friend nào có (kết quả rỗng)\n"
       "2. Click 全て確認済みに変更 → 決定\n"
       "3. Kiểm tra các conversation khác trong DB (confirm_count, updated_at)",
       "Bộ lọc cho kết quả 0 friend",
       "- Không phát sinh lỗi, không màn trắng\n"
       "- Không conversation nào bị thay đổi confirm_count hay updated_at",
       note="Nguồn: Leftbar+Header r561 + Test fix bug Kh r130, r131, r142, r143"),

    tc("全て確認済みに変更", "DATA-001", "Normal",
       "全て確認済みに変更 chỉ động vào hội thoại chưa xác nhận — updated_at của hội thoại đã xác nhận không đổi",
       BOT_DATA + "\n- Có sẵn 3 hội thoại ĐÃ xác nhận và 3 hội thoại CHƯA xác nhận",
       "1. Ghi lại updated_at của 3 hội thoại đã xác nhận và 3 hội thoại chưa xác nhận\n"
       "2. Click 全て確認済みに変更 → 決定\n"
       "3. So sánh lại updated_at của cả 6 hội thoại\n"
       "4. Kiểm tra bảng unconfirm_message",
       "3 hội thoại đã xác nhận + 3 chưa xác nhận",
       "- updated_at của 3 hội thoại ĐÃ xác nhận KHÔNG thay đổi\n"
       "- updated_at của 3 hội thoại CHƯA xác nhận được cập nhật\n"
       "- Bản ghi unconfirm_message của 3 hội thoại vừa xác nhận bị xoá đúng, KHÔNG xoá thừa của hội thoại khác",
       note="Nguồn: Test fix bug Kh r137-r140 (Bug tự detect #39257 — performance confirmReadMessage)"),

    tc("全て確認済みに変更", "CONC-002", "Abnormal",
       "Có tin nhắn mới đến trong lúc đang chạy 全て確認済みに変更 — không mất dữ liệu",
       BOT_DATA,
       "1. Chuẩn bị bot có ≥200 hội thoại chưa xác nhận (để thao tác đủ lâu)\n"
       "2. Click 全て確認済みに変更 → 決定\n"
       "3. NGAY trong lúc đang xử lý: cho friend X gửi 1 tin nhắn mới đến bot\n"
       "4. Sau khi xong: kiểm tra trạng thái của X và bots.count_user_unconfirm",
       "200 hội thoại + 1 tin mới đến giữa chừng",
       "- Không mất tin nhắn của X (vẫn nằm trong lịch sử chat)\n"
       "- Trạng thái của X phản ánh đúng thực tế (chưa xác nhận nếu tin đến sau khi X đã được xử lý)\n"
       "- bots.count_user_unconfirm khớp với số friend thực sự còn chưa xác nhận",
       env="PRODUCTION",
       note="Race condition → RULE-08 bắt buộc PRODUCTION. Nguồn: Test fix bug Kh r144"),

    tc("全て確認済みに変更", "STATE-001", "Normal",
       "Sau 全て確認済みに変更, reload màn hình — trạng thái đã xác nhận được giữ",
       BOT_DATA,
       "1. Click 全て確認済みに変更 → 決定\n2. Reload trang /basic/chat-v3\n"
       "3. Quan sát danh sách và badge ở menu\n4. Mở lần lượt vài hội thoại kiểm tra chi tiết",
       "Bot A sau khi xác nhận toàn bộ",
       "- Không hội thoại nào hiện lại chấm xanh chưa đọc\n- Badge ở menu vẫn là 0\n"
       "- Chi tiết từng hội thoại hiển thị đúng trạng thái đã xác nhận",
       note="Nguồn: Leftbar+Header r558, r562 + Test fix bug Kh r141"),

    tc("全て確認済みに変更", "CONC-001", "Abnormal",
       "Double click nút 決定 của popup 全て確認済みに変更 — chỉ tính 1 lần",
       BOT_DATA,
       "1. Click 全て確認済みに変更\n2. Double click nhanh nút 決定\n"
       "3. Quan sát Network và bots.count_user_unconfirm",
       "Double click trong < 300ms",
       "- Chỉ phát sinh 1 request xác nhận\n- count_user_unconfirm không bị trừ 2 lần, không âm",
       note="Nguồn: Leftbar+Header r13"),

    # ═══════════════ Tìm kiếm bạn bè ═══════════════
    tc("Tìm kiếm bạn bè", "FUNC-002", "Normal",
       "Tìm kiếm theo LINE名 / システム表示名 — các dạng nhập đều ra kết quả đúng",
       BOT + "\n- Friend K có LINE名「山田太郎」, システム表示名「ヤマダ」\n- Friend L có LINE名「Yamada Hanako」, không có システム表示名",
       "1. Với mỗi cách nhập ở cột Dữ liệu test: gõ vào ô tìm kiếm\n"
       "2. Quan sát danh sách kết quả",
       "Copy-paste nguyên tên · gõ tay · nhập nửa tên (`山田`) · hoa/thường (`yamada` vs `YAMADA`) · "
       "có khoảng trắng đầu/cuối (`␣山田␣`) · tên tiếng Nhật · システム表示名 có khoảng trắng",
       "- Với mọi cách nhập trên đều hiện đúng friend khớp (tìm gần đúng, không phân biệt hoa/thường)\n"
       "- Khoảng trắng đầu/cuối được bỏ qua, vẫn ra kết quả",
       note="Gộp 7 điểm vì cùng kết quả. Nguồn: Leftbar+Header r126, r128-r133"),

    tc("Tìm kiếm bạn bè", "LIST-001", "Abnormal",
       "Tìm kiếm không có kết quả — hiển thị thông báo, không danh sách trống trơn",
       BOT,
       "1. Nhập từ khoá chắc chắn không tồn tại vào ô tìm kiếm\n2. Quan sát vùng danh sách bạn bè",
       "Từ khoá `zzzz_khong_ton_tai_9999`",
       "- Hiển thị thông báo 「検索ワードに一致する 友だちは見つかりませんでした」\n"
       "- Không lỗi JS, không loading vô hạn",
       note="Nguồn: Leftbar+Header r134"),

    tc("Tìm kiếm bạn bè", "FUNC-MULTI-001", "Normal",
       "Tìm kiếm kết hợp filter — kết quả phải thoả cả từ khoá lẫn bộ lọc",
       BOT_DATA + "\n" + TAGSET,
       "1. Với mỗi tổ hợp ở cột Dữ liệu test: nhập từ khoá + áp dụng filter tương ứng\n"
       "2. Đối chiếu danh sách kết quả với dữ liệu thực tế",
       "Tổ hợp: LINE名 + filter dropdown · LINE名 + filter tag/status · LINE名 + cả 2 loại filter · "
       "システム表示名 + từng loại filter (lặp lại 3 tổ hợp trên)",
       "- Mọi tổ hợp: chỉ hiện friend thoả ĐỒNG THỜI từ khoá và toàn bộ điều kiện lọc",
       note="Gộp 6 tổ hợp vì cùng kết quả. Nguồn: Leftbar+Header r135-r140, r108-r122"),

    tc("Tìm kiếm bạn bè", "STATE-CLEAN-001", "Normal",
       "Xoá từ khoá tìm kiếm — danh sách trở lại theo filter đang áp dụng",
       BOT_DATA + "\n" + TAGSET + "\n- Đang áp dụng filter tag T1",
       "1. Nhập từ khoá khớp 1 friend trong tập T1\n2. Xoá sạch ô tìm kiếm\n3. Quan sát danh sách",
       "Filter T1 giữ nguyên, từ khoá bị xoá",
       "- Danh sách trở lại đúng tập của filter T1 (A, B)\n"
       "- KHÔNG trở về toàn bộ friend, KHÔNG mất filter",
       note="Nguồn: Leftbar+Header r516 + Content: Hiển thị msg r1593 (TC025)"),

    tc("Tìm kiếm bạn bè", "PERF-LARGE-001", "Normal",
       "Tìm kiếm trên bot nhiều bạn bè — dùng read replica, thời gian phản hồi chấp nhận được",
       "- Bot PRODUCTION có ≥50.000 friend\n- Đăng nhập admin, màn /basic/chat-v3",
       "1. Nhập từ khoá khớp nhiều friend\n2. Đo thời gian từ lúc gõ xong tới lúc danh sách hiện\n"
       "3. Lặp lại 3 lần với 3 từ khoá khác nhau\n4. Cuộn để load thêm kết quả",
       "Bot ≥50.000 friend, 3 từ khoá độ phổ biến khác nhau",
       "- Kết quả trả về trong ngưỡng chấp nhận được (ghi lại số đo thực tế làm evidence)\n"
       "- Không timeout, không trắng màn\n- Load more kết quả tìm kiếm chạy đúng",
       env="PRODUCTION",
       note="RULE-08: performance bắt buộc PRODUCTION. Spec BR-03 (feature-spec.md:465) nói khi có keyword thì "
            "dùng read replica — cần Dev xác nhận query thực chạy trên replica"),

    # ═══════════════ Danh sách bạn bè — hiển thị ═══════════════
    tc("Danh sách bạn bè — hiển thị", "UI-FIELD-001", "Normal",
       "Avatar bạn bè — có ảnh thì hiện ảnh, không có thì hiện ảnh mặc định",
       BOT + "\n- Friend M có avatar LINE\n- Friend N chưa đặt avatar (avatar_url rỗng)",
       "1. Mở danh sách bạn bè\n2. Quan sát ô avatar của M và N",
       "M có avatar · N không avatar",
       "- M: hiện đúng ảnh đại diện LINE của M\n- N: hiện ảnh mặc định của hệ thống\n"
       "- Cả 2 đều không có viền xanh khi đã xác nhận hết tin",
       note="Nguồn: Leftbar+Header r141, r142"),

    tc("Danh sách bạn bè — hiển thị", "UI-FIELD-001", "Normal",
       "Tên hiển thị — ưu tiên システム表示名, không có thì lấy LINE名",
       BOT + "\n- Friend K: LINE名「山田太郎」+ システム表示名「ヤマダ」\n- Friend L: chỉ có LINE名「Yamada Hanako」",
       "1. Mở danh sách bạn bè\n2. Đọc tên hiển thị của K và L\n"
       "3. Sang tab 基本情報 của K, xoá システム表示名 → quay lại danh sách",
       "K có cả 2 tên · L chỉ có LINE名",
       "- K hiển thị 「ヤマダ」 (システム表示名)\n- L hiển thị 「Yamada Hanako」 (LINE名)\n"
       "- Sau khi xoá システム表示名 của K: K hiển thị 「山田太郎」",
       note="Nguồn: Leftbar+Header r143, r144"),

    tc("Danh sách bạn bè — hiển thị", "UI-FIELD-001", "Normal",
       "対応ステータス hiển thị phía trên tên — đúng text và đúng màu, cả status mặc định và tự tạo",
       BOT + "\n- 5 status mặc định: 見込みあり / 対応中 / フォロー / トラブル / 対応完了\n"
       "- Thêm status tự tạo「保留」màu khác\n- Gán mỗi status cho 1 friend; 1 friend để không status",
       "1. Mở danh sách bạn bè\n2. Với từng friend: đọc text và màu badge status phía trên tên\n"
       "3. Quan sát friend không có status",
       "6 status (5 mặc định + 1 tự tạo) + 1 friend không status",
       "- Friend có status: hiện badge đúng text và đúng màu đã cấu hình, nằm phía trên tên\n"
       "- Friend KHÔNG có status: không hiện badge nào, layout không lệch",
       note="Gộp 6 status vì cùng kết quả; tách riêng case không status vì kết quả khác. "
            "Nguồn: Leftbar+Header r145-r147"),

    tc("Danh sách bạn bè — hiển thị", "UI-002", "Normal",
       "Chấm xanh chưa đọc — có khi còn tin chưa xác nhận, mất khi đã xác nhận",
       BOT + "\n- Friend O có 2 tin chưa xác nhận",
       "1. Quan sát dòng của O trong danh sách\n2. Mở hội thoại O, bấm xác nhận\n3. Quan sát lại dòng của O",
       "Friend O: 2 tin chưa đọc → xác nhận",
       "- Trước: dòng O có chấm xanh ở avatar, nền dòng màu trắng #FFFFFF\n"
       "- Sau khi xác nhận: chấm xanh biến mất",
       note="Nguồn: Leftbar+Header r150, r151"),

    tc("Danh sách bạn bè — hiển thị", "UI-002", "Normal",
       "Icon đồng hồ 送信予約 — chỉ hiện với bạn bè đang có lịch gửi chờ",
       BOT + "\n- Friend P đã đặt lịch gửi chưa tới giờ\n- Friend Q chưa đặt lịch nào",
       "1. Quan sát dòng của P và Q trong danh sách\n"
       "2. Huỷ lịch gửi của P → quan sát lại",
       "P có lịch chờ · Q không lịch",
       "- P: có icon hình đồng hồ màu #5799DB\n- Q: KHÔNG có icon đồng hồ\n"
       "- Sau khi huỷ lịch của P: icon đồng hồ của P biến mất",
       note="Nguồn: Leftbar+Header r152, r153"),

    tc("Danh sách bạn bè — hiển thị", "MSG-003", "Normal",
       "Tin nhắn cuối hiển thị ở danh sách — cắt bớt khi dài",
       BOT + "\n- Friend R có tin nhắn cuối dài > 60 ký tự",
       "1. Cho friend R gửi 1 tin dài (ví dụ 100 ký tự)\n2. Quan sát dòng của R trong danh sách\n"
       "3. Đo số ký tự hiển thị trước dấu ba chấm",
       "Tin nhắn 100 ký tự tiếng Nhật",
       "- Dòng R hiển thị phần đầu tin nhắn + dấu ... , không xuống dòng, không vỡ layout\n"
       "- Ghi lại số ký tự thực tế hiển thị làm evidence",
       spec="Spec không ghi",
       note="TC gốc để dấu hỏi 「độ dài ? ký tự」 → chưa ai chốt con số. Nguồn: Leftbar+Header r156"),

    tc("Danh sách bạn bè — hiển thị", "MSG-003", "Normal",
       "Bạn bè thu hồi tin nhắn — dòng danh sách đổi thành thông báo thu hồi",
       BOT + "\n- Friend S vừa gửi tin cho bot",
       "1. Với mỗi loại tin ở cột Dữ liệu test: cho S gửi rồi thu hồi trên app LINE\n"
       "2. Quan sát dòng của S trong danh sách bạn bè",
       "Loại tin bị thu hồi: text · video · audio · pdf · ảnh",
       "- Với mọi loại: nội dung tin nhắn cuối ở danh sách đổi thành 「友だちがメッセージを送信取り消しました」\n"
       "- Thời gian tin nhắn cuối không đổi",
       note="Gộp 5 loại vì cùng kết quả. Nguồn: Leftbar+Header r154 + Content: Hiển thị msg r71, r72"),

    tc("Danh sách bạn bè — hiển thị", "MSG-003", "Normal",
       "Bạn bè thu hồi TOÀN BỘ tin nhắn — dòng danh sách hiện 送信取消されました",
       BOT + "\n- Friend T có đúng 2 tin nhắn, đều do T gửi",
       "1. Cho T thu hồi cả 2 tin trên app LINE\n2. Quan sát dòng của T trong danh sách và trong khung hội thoại",
       "Thu hồi toàn bộ tin nhắn của hội thoại",
       "- Dòng của T ở danh sách hiển thị 「送信取消されました」\n"
       "- Khung hội thoại vẫn mở được, không lỗi",
       note="Tách riêng vì text khác case thu hồi 1 tin. Nguồn: Leftbar+Header r157"),

    tc("Danh sách bạn bè — hiển thị", "MSG-003", "Normal",
       "Thu hồi 1 phần tin nhắn — thời gian tin nhắn cuối cập nhật đúng vị trí còn lại",
       BOT + "\n- Friend U có ≥5 tin nhắn trong ngày hôm nay",
       "1. Ghi lại nội dung + thời gian tin nhắn cuối ở danh sách\n"
       "2. Thu hồi tin ĐẦU cuộc hội thoại → kiểm tra dòng danh sách\n"
       "3. Thu hồi tin ở GIỮA → kiểm tra\n4. Thu hồi tin CUỐI CÙNG của ngày → kiểm tra",
       "5 tin nhắn, thu hồi lần lượt vị trí đầu / giữa / cuối",
       "- Thu hồi tin đầu và giữa: nội dung + thời gian tin nhắn cuối ở danh sách KHÔNG đổi\n"
       "- Thu hồi tin cuối: nội dung đổi thành thông báo thu hồi, thời gian giữ nguyên của tin đó",
       note="Nguồn: Leftbar+Header r158-r161"),

    tc("Danh sách bạn bè — hiển thị", "FRIEND-001", "Normal",
       "Bạn bè bị block — hiển thị thông báo block ở danh sách và khung hội thoại",
       BOT + "\n- Friend V: bot đã block V\n- Friend W: W đã block bot",
       "1. Quan sát dòng của V và W trong danh sách\n2. Mở hội thoại của V rồi W\n"
       "3. Thử gõ tin nhắn ở cả 2 hội thoại",
       "V: bot block friend · W: friend block bot",
       "- Cả 2 dòng hiển thị thông báo trạng thái block kèm thời điểm block\n"
       "- Khung hội thoại hiển thị message hệ thống block\n"
       "- Không gửi được tin nhắn ở cả 2 hội thoại",
       note="Nguồn: Leftbar+Header r163, r164 + Content: Hiển thị msg r44-r52"),

    tc("Danh sách bạn bè — hiển thị", "UI-002", "Normal",
       "Icon bookmark ở danh sách — mặc định ẩn, hiện khi được đánh dấu",
       BOT + "\n- Friend X chưa bookmark, friend Y đã bookmark",
       "1. Quan sát góc trên bên phải dòng của X và Y",
       "X chưa bookmark · Y đã bookmark",
       "- X: không hiện icon bookmark\n- Y: hiện icon bookmark ở góc trên bên phải, màu #5799DB",
       note="Nguồn: Leftbar+Header r165, r166"),

    tc("Danh sách bạn bè — hiển thị", "LIST-001", "Normal",
       "Bạn bè bookmark luôn nằm đầu danh sách, sau đó sắp theo tin nhắn cuối",
       BOT + "\n- Friend Y đã bookmark, tin nhắn cuối CŨ nhất\n- Friend Z không bookmark, tin nhắn cuối MỚI nhất",
       "1. Mở danh sách bạn bè với filter mặc định\n2. Đọc thứ tự Y và Z\n"
       "3. Bỏ bookmark Y → reload → đọc lại thứ tự",
       "Y: bookmark + tin cũ · Z: không bookmark + tin mới",
       "- Khi Y còn bookmark: Y đứng TRÊN Z dù tin nhắn cuối cũ hơn\n"
       "- Sau khi bỏ bookmark Y: Z lên trên Y",
       note="Nguồn: Leftbar+Header r165, r166 + spec BR-02 (feature-spec.md:464)"),

    # ═══════════════ Danh sách nhóm — hiển thị ═══════════════
    tc("Danh sách nhóm — hiển thị", "UI-FIELD-001", "Normal",
       "Dòng nhóm LINE — icon nhóm + tên nhóm + avatar (hoặc ảnh mặc định)",
       BOT + "\n- Bot A ở trong nhóm G1 (có ảnh nhóm) và G2 (không có ảnh nhóm)",
       "1. Chọn filter グループ\n2. Quan sát dòng của G1 và G2\n"
       "3. Kiểm tra DB: SELECT name FROM line_user WHERE ... (bản ghi của nhóm)",
       "G1 có ảnh · G2 không ảnh",
       "- G1: hiện ảnh nhóm; G2: hiện ảnh mặc định\n"
       "- Cả 2 hiện icon nhóm + tên nhóm, tên khớp line_user.name",
       note="Nguồn: Leftbar+Header r169-r171"),

    tc("Danh sách nhóm — hiển thị", "SYNC-APP-001", "Abnormal",
       "Đổi tên nhóm LINE — tên trên chat 1:1 có tự cập nhật không",
       BOT + "\n- Bot A ở trong nhóm G1",
       "1. Ghi lại tên G1 hiển thị ở chat 1:1 và giá trị line_user.name\n"
       "2. Trên app LINE: đổi tên nhóm G1 thành tên mới\n"
       "3. Reload chat 1:1, đọc lại tên hiển thị và line_user.name\n"
       "4. Nếu chưa đổi: cho nhóm gửi 1 tin đến bot rồi kiểm tra lại",
       "Tên cũ「テストグループ」→ tên mới「テストグループ2026」",
       "- Ghi nhận thực tế: tên hiển thị và line_user.name có cập nhật hay không, cập nhật ở thời điểm nào\n"
       "- Đối chiếu với quyết định của Leader",
       spec="Đã hỏi leader",
       note="TC gốc ghi 「Spect cũ: bảng line_user cột name chưa tự động update」nhưng expect lại là "
            "「Hiển thị tên mới」→ mâu thuẫn nội bộ. Nguồn: Leftbar+Header r172"),

    tc("Danh sách nhóm — hiển thị", "UI-FIELD-001", "Normal",
       "対応ステータス của nhóm — hiển thị như friend, cả status mặc định và tự tạo",
       BOT + "\n- Nhóm G1 gán status 対応中; nhóm G2 gán status tự tạo「保留」; nhóm G3 không status",
       "1. Chọn filter グループ\n2. Đọc badge status của G1, G2, G3",
       "3 nhóm với 3 tình trạng status khác nhau",
       "- G1, G2: hiện badge đúng text + đúng màu phía trên tên nhóm\n- G3: không hiện badge",
       note="Nguồn: Leftbar+Header r173-r175"),

    tc("Danh sách nhóm — hiển thị", "LIST-001", "Normal",
       "Ẩn/hiện nhóm — filter 全ての友だち không hiện nhóm ẩn, filter 非表示中 thì hiện",
       BOT + "\n- Nhóm G2 đang bị ẩn",
       "1. Chọn filter 全ての友だち（非表示除く）→ tìm G2\n2. Chọn filter 非表示中 → tìm G2",
       "Nhóm G2 đang ẩn",
       "- Filter 全ての友だち: KHÔNG hiện G2\n- Filter 非表示中: hiện G2",
       note="Nguồn: Leftbar+Header r176, r177"),

    tc("Danh sách nhóm — hiển thị", "UI-002", "Normal",
       "Nhóm — chấm xanh chưa đọc, icon lịch gửi, icon bookmark hoạt động như friend",
       BOT + "\n- Nhóm G1 có tin chưa xác nhận, đã đặt lịch gửi và đã bookmark\n- Nhóm G3 không có gì",
       "1. Quan sát dòng G1: chấm xanh, icon đồng hồ, icon bookmark\n2. Quan sát dòng G3\n"
       "3. Xác nhận tin của G1, huỷ lịch, bỏ bookmark → quan sát lại",
       "G1 đủ 3 dấu hiệu · G3 không có",
       "- G1: có chấm xanh ở avatar, icon đồng hồ, icon bookmark góc trên phải\n"
       "- G3: không có dấu hiệu nào\n- Sau khi gỡ hết: G1 hiển thị giống G3",
       note="Gộp 3 dấu hiệu vì đều là hiển thị của cùng 1 dòng. Nguồn: Leftbar+Header r178-r181, r192, r193"),

    tc("Danh sách nhóm — hiển thị", "FRIEND-001", "Normal",
       "Bot bị xoá khỏi nhóm — hội thoại nhóm chuyển sang trạng thái block",
       BOT + "\n- Bot A đang ở trong nhóm G4",
       "1. Trên app LINE: xoá bot A khỏi nhóm G4\n2. Quan sát dòng G4 ở chat 1:1\n"
       "3. Kiểm tra DB: SELECT is_blocked FROM conversation WHERE ... (G4)\n"
       "4. Thêm lại bot vào G4 → kiểm tra lại",
       "Nhóm G4: xoá bot → thêm lại bot",
       "- Sau khi bot bị xoá khỏi nhóm: dòng G4 hiển thị trạng thái block; conversation.is_blocked = 1\n"
       "- Sau khi thêm lại bot: is_blocked = 0, hội thoại dùng lại được",
       note="Verify DB + màn hình. Nguồn: Leftbar+Header r185 + Group chat r4, r6"),

    # ═══════════════ Load more & chuyển hội thoại ═══════════════
    tc("Load more & chuyển hội thoại", "LIST-001", "Normal",
       "Load more danh sách bạn bè — chỉ hiện nút/hành vi load thêm khi danh sách vượt 1 trang",
       BOT + "\n- Bot NHIỀU friend: ≥25 friend\n- Bot ÍT friend: ≤10 friend",
       "1. Ở bot ít friend: cuộn hết danh sách, kiểm tra có nút/hành vi load more không\n"
       "2. Ở bot nhiều friend: cuộn xuống cuối danh sách\n3. Kích hoạt load more, đếm số friend sau khi load",
       "Bot ≤10 friend · bot ≥25 friend (page size 20)",
       "- Bot ít friend: không hiện load more\n"
       "- Bot nhiều friend: hiện load more; sau khi load thêm, danh sách nối tiếp thêm friend ở dưới, KHÔNG lặp friend đã có",
       note="Nguồn: Leftbar+Header r167, r168"),

    tc("Load more & chuyển hội thoại", "LIST-001", "Boundary",
       "Phân trang danh sách bạn bè — mỗi lần tải đúng 20 bản ghi",
       BOT + "\n- Chuẩn bị 3 bot: bot có đúng 20 friend · bot có 21 friend · bot có 41 friend",
       "1. Với bot 20 friend: mở danh sách, đếm số dòng, kiểm tra có load more không\n"
       "2. Với bot 21 friend: đếm số dòng lần đầu, tải thêm rồi đếm lại\n"
       "3. Với bot 41 friend: tải thêm 2 lần, đếm số dòng sau mỗi lần\n"
       "4. Kiểm tra không có bản ghi nào bị lặp hoặc bị thiếu",
       "Bot 20 friend · bot 21 friend · bot 41 friend (kích thước trang = 20)",
       "- Bot 20 friend: hiện đủ 20, KHÔNG có load more\n"
       "- Bot 21 friend: lần đầu 20 dòng, sau khi tải thêm đủ 21 dòng\n"
       "- Bot 41 friend: 20 → 40 → 41 dòng\n"
       "- Không lặp, không thiếu bản ghi nào",
       note="Biên phân trang theo spec (feature-spec.md:124 — 20 items/page). Nguồn: Leftbar+Header r167, r168"),

    tc("Load more & chuyển hội thoại", "STATE-001", "Normal",
       "Load more xong rồi chọn hội thoại ở page 1 và ở page vừa load — đều hiển thị đúng",
       BOT + "\n- Bot có ≥45 friend (≥3 page)",
       "1. Load more 1 lần (có 40 friend)\n2. Click hội thoại ĐẦU TIÊN của danh sách → kiểm tra lịch sử + tên\n"
       "3. Click hội thoại CUỐI CÙNG (thuộc page vừa load) → kiểm tra lịch sử + tên\n"
       "4. Load more tiếp rồi lặp lại bước 2-3",
       "Bot ≥45 friend",
       "- Cả 2 lần chọn đều hiển thị ĐÚNG lịch sử chat và ĐÚNG tên/avatar của hội thoại được click\n"
       "- Không hiện nhầm dữ liệu của hội thoại khác",
       note="Nguồn: Content: Hiển thị msg r1586, r1587, r1589, r1590 (Bug KH #36859 TC021-TC022)"),

    tc("Load more & chuyển hội thoại", "STATE-001", "Abnormal",
       "Load more khi đang mở 1 hội thoại — không bị nhảy sang hội thoại khác",
       BOT + "\n- Bot có ≥45 friend, trong đó có nhóm LINE",
       "1. Mở hội thoại của friend A (nằm ở page 1)\n2. Cuộn danh sách và load more nhiều lần liên tiếp\n"
       "3. Quan sát cột giữa và cột phải\n4. Lặp lại với hội thoại đang mở là NHÓM LINE",
       "Hội thoại đang mở: friend A · sau đó nhóm G1 (có bot_line_user_id rỗng)",
       "- Trong và sau khi load more: hội thoại đang chọn KHÔNG đổi, lịch sử ở cột giữa giữ nguyên\n"
       "- Không bị reset về hội thoại đầu tiên\n- Đúng cả khi hội thoại đang mở là nhóm LINE",
       note="Nguồn: Content: Hiển thị msg r1581-r1585, r1588 (Bug KH #36859)"),

    tc("Load more & chuyển hội thoại", "CONC-003", "Abnormal",
       "Chuyển hội thoại khi hội thoại trước chưa load xong — chỉ hiện dữ liệu hội thoại sau",
       BOT + "\n- Friend A và friend B đều có ≥50 tin nhắn\n- DevTools bật throttling mạng chậm",
       "1. Mở DevTools → Network → throttle Slow 3G\n2. Click hội thoại A\n"
       "3. NGAY khi A còn đang loading, click hội thoại B\n4. Chờ cả 2 response về, quan sát cột giữa và header",
       "A và B, mạng chậm để response A về SAU response B",
       "- Cột giữa chỉ hiển thị lịch sử của B\n- Header hiển thị tên + avatar của B\n"
       "- Response của A về sau bị bỏ qua, KHÔNG ghi đè lên B",
       note="Nguồn: Content: Hiển thị msg r1567, r1569, r1570 (Bug KH #36859 TC003, TC005, TC006)"),

    tc("Load more & chuyển hội thoại", "CONC-003", "Abnormal",
       "Click liên tiếp 3 hội thoại A → B → C — chỉ hiện dữ liệu của C",
       BOT + "\n- 3 hội thoại A, B, C đều có lịch sử chat khác nhau rõ rệt",
       "1. Click nhanh liên tiếp A → B → C (mỗi lần cách nhau < 200ms)\n"
       "2. Chờ mọi response về\n3. Quan sát lịch sử và header\n"
       "4. Lặp lại thao tác A ↔ B nhiều lần liên tục",
       "3 hội thoại, click liên tiếp; sau đó A ↔ B lặp 10 lần",
       "- Chỉ hiển thị dữ liệu của C (hội thoại click cuối cùng)\n"
       "- Sau khi A ↔ B nhiều lần: luôn hiển thị đúng hội thoại đang chọn, không lẫn lịch sử",
       note="Nguồn: Content: Hiển thị msg r1568, r1571 (TC004, TC007)"),

    tc("Load more & chuyển hội thoại", "CONC-003", "Abnormal",
       "Chuyển giữa nhóm LINE và bạn bè cá nhân — không hiện nhầm tên/lịch sử",
       BOT + "\n- Nhóm G1 và friend B đều có lịch sử chat",
       "1. Mở nhóm G1\n2. Ngay lập tức click friend B\n3. Quan sát lịch sử, tên, avatar ở cột giữa và cột phải\n"
       "4. Làm ngược lại: mở B rồi click G1",
       "Nhóm G1 ↔ friend B",
       "- Luôn hiển thị đúng lịch sử, tên và avatar của hội thoại được chọn sau cùng\n"
       "- Không hiện tên nhóm khi đang mở friend và ngược lại",
       note="Đây chính là hiện tượng của Bug KH #36859 (06/2026). Nguồn: Content: Hiển thị msg r1572 (TC008)"),

    tc("Load more & chuyển hội thoại", "CONC-003", "Abnormal",
       "Gửi tin ở hội thoại A rồi chuyển ngay sang B — dữ liệu A không tràn sang B",
       BOT + "\n- Friend A và B đều có lịch sử chat",
       "1. Mở A, gõ và gửi 1 tin nhắn\n2. NGAY sau khi bấm gửi, click sang B\n"
       "3. Quan sát khung hội thoại B\n4. Quay lại A kiểm tra tin vừa gửi",
       "Tin nhắn `test-chuyen-hoi-thoai`",
       "- Khung B KHÔNG xuất hiện tin nhắn vừa gửi cho A\n"
       "- Quay lại A: tin nhắn hiển thị đúng trong lịch sử của A",
       note="Nguồn: Content: Hiển thị msg r1575, r1576 (TC011, TC012)"),

    tc("Load more & chuyển hội thoại", "CONC-003", "Abnormal",
       "Đang mở hội thoại A, friend B gửi tin đến — A không bị chèn tin của B",
       BOT + "\n- Friend A và B đều là bạn bè của bot",
       "1. Mở hội thoại của A\n2. Cho A gửi 1 tin đến bot → kiểm tra A nhận realtime\n"
       "3. Chuyển sang hội thoại B\n4. Cho A gửi tiếp 1 tin nữa → quan sát khung B và dòng A ở danh sách",
       "A gửi 2 tin ở 2 thời điểm",
       "- Bước 2: khung A hiển thị tin mới realtime\n"
       "- Bước 4: khung B KHÔNG hiện tin của A; dòng A ở danh sách cập nhật tin nhắn cuối và badge chưa đọc",
       env="PRODUCTION",
       note="Cần socket thật → RULE-08. Nguồn: Content: Hiển thị msg r1607, r1608 (TC039, TC040)"),

    tc("Load more & chuyển hội thoại", "CONC-003", "Abnormal",
       "Mở chat 1:1 cùng bot trên 2 tab, thao tác chéo — mỗi tab giữ đúng hội thoại của mình",
       BOT + "\n- Cùng account, cùng bot, mở 2 tab trình duyệt\n- Có ≥2 hội thoại: A (friend) và B (nhóm LINE)",
       "1. Tab 1 mở hội thoại A\n2. Tab 2 mở hội thoại B\n3. Quay lại Tab 1: cuộn danh sách / reload\n"
       "4. Quay sang Tab 2: quan sát hội thoại đang mở\n5. Lặp lại 3-4 vài lần",
       "2 tab, hội thoại A (friend) và B (nhóm)",
       "- Tab 1 luôn giữ hội thoại A, Tab 2 luôn giữ hội thoại B\n"
       "- Không tab nào nhảy sang hội thoại của tab kia, không hiện nhầm tên/lịch sử",
       spec="Spec không ghi",
       note="TC do AI bổ sung theo hướng root cause đa tab của Bug KH #36859, CẦN LEADER XÁC NHẬN. "
            "Nguồn: Content: Hiển thị msg r1609 (TC-NEW-01)"),

    tc("Load more & chuyển hội thoại", "CONC-003", "Abnormal",
       "Friend A và nhóm B cùng nhận tin qua socket khi đang xem A",
       "- Môi trường có socket hoạt động (Staging/Production)\n- Đang mở hội thoại friend A\n"
       "- Bot cũng ở trong nhóm B",
       "1. Mở hội thoại friend A\n2. Cho A và nhóm B gửi tin tới bot gần như đồng thời\n"
       "3. Quan sát khung hội thoại A và dòng của B ở danh sách",
       "A và B gửi tin cách nhau < 1 giây",
       "- Khung A CHỈ nhận tin của A; tin của nhóm B không chèn vào khung A\n"
       "- Dòng B ở danh sách cập nhật tin nhắn cuối, không lẫn vào A",
       env="PRODUCTION",
       spec="Spec không ghi",
       note="TC do AI bổ sung (nhánh root cause thay thế của #36859), CẦN LEADER XÁC NHẬN. "
            "Nguồn: Content: Hiển thị msg r1610 (TC-NEW-04)"),

    tc("Load more & chuyển hội thoại", "STATE-001", "Normal",
       "Tìm kiếm / lọc khi đang mở 1 hội thoại — hội thoại đang chọn không bị đổi",
       BOT_DATA + "\n" + TAGSET + "\n- Đang mở hội thoại nhóm G1",
       "1. Mở hội thoại nhóm G1\n2. Nhập từ khoá tìm kiếm → quan sát cột giữa\n"
       "3. Xoá từ khoá → quan sát\n4. Áp dụng filter tag T1 → quan sát\n5. Xoá filter → quan sát",
       "Hội thoại đang mở: nhóm G1; thao tác search và filter",
       "- Sau mỗi thao tác search/filter/clear: cột giữa VẪN hiển thị hội thoại G1\n"
       "- Danh sách bên trái đổi theo điều kiện, nhưng hội thoại đang chọn không bị đổi ngoài ý muốn",
       note="Nguồn: Content: Hiển thị msg r1592, r1595 (TC024, TC027)"),

    tc("Load more & chuyển hội thoại", "STATE-001", "Normal",
       "Có bạn bè mới kết bạn khi đang mở 1 hội thoại — hội thoại đang chọn giữ nguyên",
       BOT + "\n- Đang mở hội thoại của friend A",
       "1. Mở hội thoại của friend A\n2. Cho 1 tài khoản LINE mới kết bạn với bot\n"
       "3. Quan sát cột giữa và danh sách bên trái\n4. Reload trang → quan sát danh sách",
       "1 friend mới kết bạn trong lúc đang mở A",
       "- Hội thoại A vẫn được giữ, không bị nhảy sang friend mới\n"
       "- Friend mới chỉ xuất hiện trong danh sách sau khi reload màn hình",
       note="Nguồn: Content: Hiển thị msg r1606 (TC038)"),
]
