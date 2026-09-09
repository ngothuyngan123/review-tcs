# -*- coding: utf-8 -*-
"""FA-010 テンプレート — Nhóm 10-13: màn list template con, quick test (tester + gửi), preview ở các màn.

Nguồn chính: 02. TCsLine_Template
  - tab「Improve list template」(12/2023 → 05/2026) — màn list template con, modal preview/send test,
    đăng ký tester, quick send (tối đa 3 user)
  - tab「Task nhỏ+ check Bug Kh」r45-r107 — ma trận preview template button standard ở 5 màn
    (Review #30710 + Review 11/2025)
"""
import re as _re

from _common import tc

ADM = ("- Đăng nhập admin (主管理者) bot A trên môi trường STAGING\n"
       "- Mở /basic/message-template")
GRP = (ADM + "\n- Folder F1 có group template G1「案内」\n"
       "- G1 đã có 3 template con: T1 dạng text, T2 dạng パネル・ボタン, T3 dạng 画像")
TESTER = (ADM + "\n- Bot A có ≥25 friend đã kết bạn, chưa ai được đăng ký làm クイックテストユーザー\n"
          "- Có ít nhất 1 friend tên LINE là「テスト太郎」")

S2 = [
    # ═════════════ 10. Màn list template con ═════════════
    tc("Màn list template con", "UI-001", "Normal",
       "Mở màn list template con (テンプレート作成) → hiện folder, 管理名 và danh sách template con từ cũ đến mới",
       GRP,
       "1. Ở màn list, click vào group G1\n2. Quan sát header màn hình (folder + 管理名)\n"
       "3. Quan sát danh sách template con và thứ tự hiển thị",
       "G1 có 3 template con T1 → T2 → T3 (tạo theo thứ tự đó)",
       "- Header hiện đúng tên folder F1 và 管理名「案内」của group\n"
       "- Danh sách hiện đủ 3 template con đã tạo, thứ tự TỪ CŨ ĐẾN MỚI (T1, T2, T3)\n"
       "- Giao diện khớp design",
       note="Nguồn: Improve list template r347-r355."),

    tc("Màn list template con", "UI-003", "Normal",
       "Group template chưa có template con → hiện「メッセージが登録されていません」",
       ADM + "\n- Group G9 vừa được tạo, chưa thêm template con nào",
       "1. Click vào group G9\n2. Quan sát vùng danh sách template con",
       "G9 = 0 template con",
       "- Không có dòng template con nào\n- Hiện đúng chuỗi「メッセージが登録されていません」",
       note="Nguồn: Improve list template r356."),

    tc("Màn list template con", "FUNC-001", "Normal",
       "Sửa 管理名 / folder ở màn list template con → cập nhật đúng ở màn list group",
       GRP,
       "1. Ở màn list template con của G1, sửa ô「管理名」\n2. Đổi「フォルダ」sang F2\n3. Bấm lưu\n"
       "4. Quan sát thông báo\n5. Về màn list group, kiểm tra F1 và F2",
       "管理名 mới =「案内2026」, folder F1 → F2",
       "- Hiện thông báo「変更内容が保存されました」\n"
       "- F1 không còn G1 và giảm 1 group; F2 có G1 với tên mới và tăng 1 group\n"
       "- Danh sách template con của G1 không bị ảnh hưởng",
       note="Nguồn: Improve list template r357-r361."),

    tc("Màn list template con", "FUNC-001", "Normal",
       "Tạo template con mới → nằm ở CUỐI danh sách template con, gửi được cho user",
       GRP,
       "1. Ở màn list template con của G1, bấm tạo template con mới\n2. Chọn loại「テキスト」, nhập nội dung, lưu\n"
       "3. Quan sát vị trí template mới trong danh sách\n"
       "4. Gửi quick test G1 cho 1 tester và quan sát tin nhắn trên LINE",
       "Nội dung text =「新しいメッセージです」",
       "- Template con mới hiện ở CUỐI danh sách (sau T3)\n"
       "- Quick test gửi đủ 4 tin, tin cuối là「新しいメッセージです」\n- Thứ tự tin nhắn khớp thứ tự danh sách",
       note="Nguồn: Improve list template r369-r372. RULE-06: xác nhận tới output cuối trên LINE app."),

    tc("Màn list template con", "FUNC-001", "Normal",
       "Sửa template con → nội dung mới hiển thị ở danh sách và trong tin nhắn gửi đi",
       GRP,
       "1. Bấm sửa template con T1\n2. Đổi nội dung text\n3. Lưu\n"
       "4. Quan sát dòng T1 trong danh sách\n5. Gửi quick test G1 và quan sát tin nhắn trên LINE",
       "Nội dung cũ「ご案内」→ mới「ご案内(改)」",
       "- Danh sách hiện đủ thông tin mới của T1\n"
       "- Tin nhắn nhận được trên LINE hiển thị nội dung ĐÃ SỬA, không phải nội dung cũ",
       note="Nguồn: Improve list template r380-r383. Cùng nhóm rủi ro với Bug KH #35871 "
            "(edit template rồi send không apply) — xem TC nhóm『Template legacy & tương thích』."),

    tc("Màn list template con", "UI-002", "Normal",
       "Link「テンプレートの配信カウントについて」mở đúng trang giới thiệu",
       GRP,
       "1. Ở màn list template con, tìm link「テンプレートの配信カウントについて」\n2. Click vào link",
       "—",
       "- Mở trang giới thiệu về số lần gửi mẫu (tab mới)\n- Màn list template con vẫn giữ nguyên trạng thái",
       note="Nguồn: Improve list template r379."),

    tc("Màn list template con", "LIST-001", "Normal",
       "Sắp xếp template con: move đầu/cuối + kéo-thả → thứ tự đổi đúng và giữ sau lưu",
       GRP,
       "1. Bấm「並べ替え」ở màn list template con\n2. Menu (...) của T3 →「一番上の移動」\n"
       "3. Menu (...) của T1 →「一番下の移動」\n4. Kéo-thả T2 xuống cuối\n5. Bấm lưu → reload màn hình",
       "3 template con, 3 thao tác đổi vị trí",
       "- Mỗi thao tác đưa template con về đúng vị trí, các template khác dịch đúng bậc\n"
       "- Sau lưu + reload, danh sách giữ đúng thứ tự mới\n- `position` của template con update khớp thứ tự",
       note="Nguồn: Improve list template r453-r463."),

    tc("Màn list template con", "LIST-001", "Abnormal",
       "Template con dạng クイックリプライ luôn nằm CUỐI danh sách, không kéo-thả được",
       GRP + "\n- G1 có thêm T4 dạng パネル・ボタン sub-type クイックリプライ",
       "1. Bấm「並べ替え」\n2. Thử kéo T4 (quick reply) lên đầu danh sách\n"
       "3. Thử kéo 1 template khác xuống dưới T4\n4. Lưu và quan sát danh sách",
       "T4 = quick reply",
       "- T4 KHÔNG kéo-thả được, luôn giữ vị trí CUỐI danh sách\n"
       "- Các template khác kéo-thả bình thường nhưng không thể xuống dưới T4\n"
       "- Sau lưu, T4 vẫn ở cuối",
       note="Nguồn: Improve list template r301 (Button quick sẽ ở cuối danh sách) + r464 "
            "(template quick reply cố định). Spec KHÔNG ghi rule này → xem MT-17."),

    tc("Màn list template con", "CONC-001", "Abnormal",
       "Double click nút「並べ替え」của template con → chỉ mở 1 popup",
       GRP,
       "1. Double click nhanh nút「並べ替え」\n2. Quan sát số popup mở ra",
       "double click",
       "- Chỉ mở 1 popup sắp xếp, không mở trùng lặp, không lỗi hệ thống",
       note="Nguồn: Improve list template r453."),

    tc("Màn list template con", "DATA-REF-001", "Normal",
       "Xóa 1 template con → mất khỏi danh sách và khỏi tin nhắn gửi đi của group",
       GRP + "\n- G1 đang được gắn vào 1 broadcast và 1 step scenario",
       "1. Bấm icon xóa ở dòng T2 → quan sát popup xác nhận → xác nhận\n2. Quan sát danh sách template con\n"
       "3. Gửi quick test G1 và quan sát tin nhắn trên LINE\n"
       "4. Chạy broadcast / scenario đã gắn G1 và quan sát tin nhắn",
       "T2 (パネル・ボタン) bị xóa",
       "- Popup xác nhận hiện đúng; sau xác nhận T2 mất khỏi danh sách\n"
       "- Quick test chỉ gửi 2 tin (T1, T3), KHÔNG còn tin của T2\n"
       "- Broadcast / scenario cũng không còn gửi nội dung T2, các tin khác vẫn gửi bình thường",
       note="Nguồn: Improve list template r473-r480. RULE-06 + RULE-07."),

    tc("Màn list template con", "BULK-001", "Normal",
       "Xóa hàng loạt template con → nút enable/disable đúng, xóa hết mục đã tick",
       GRP,
       "1. Không tick gì → quan sát nút「一括削除」\n2. Tick T1 + T2 → quan sát nút\n"
       "3. Bấm「一括削除」→ quan sát popup xác nhận → xác nhận\n4. Quan sát danh sách\n"
       "5. Gửi quick test G1 và quan sát tin nhắn",
       "2 template con được tick",
       "- Chưa tick: nút「一括削除」disable; tick ≥1: enable\n"
       "- Sau xác nhận: T1 và T2 mất khỏi danh sách, chỉ còn T3\n- Nút「一括削除」trở lại disable\n"
       "- Quick test chỉ gửi 1 tin của T3",
       note="Nguồn: Improve list template r481-r486."),

    tc("Màn list template con", "FUNC-001", "Normal",
       "Bấm「戻る」ở màn list template con → về đúng màn list group template trước đó",
       GRP,
       "1. Từ màn list group, mở G1\n2. Bấm「戻る」\n3. Quan sát màn hình",
       "—",
       "- Về đúng màn list group template, đang ở folder F1 như trước khi vào\n- Không mất trạng thái sort/search",
       note="Nguồn: Improve list template r491."),

    # ═════════════ 11. Quick test — tester ═════════════
    tc("Quick test — tester", "UI-001", "Normal",
       "Modal preview / send test mở được từ icon và từ nút ở cả 2 màn list",
       GRP,
       "1. Ở màn list group, bấm icon preview/test của G1 → quan sát\n2. Đóng modal\n"
       "3. Ở màn list template con, bấm nút preview/test → quan sát\n"
       "4. Ở màn list template con, bấm icon preview của riêng T2 → quan sát",
       "4 điểm mở modal",
       "- Cả 4 điểm đều mở màn/modal preview - send test đúng design\n"
       "- Modal mở từ icon của T2 chỉ preview nội dung T2; mở từ G1 preview toàn bộ template con",
       note="Nguồn: Improve list template r251-r252, r388-r389, r443-r444."),

    tc("Quick test — tester", "UI-002", "Normal",
       "Link「検索してもアカウントが表示されない場合はこちら」mở trang manual test_delivery ở tab mới",
       GRP,
       "1. Mở modal preview/send test\n2. Bấm link「検索してもアカウントが表示されない場合はこちら」",
       "—",
       "- Mở https://lme.jp/manual/test_delivery/ ở TAB MỚI\n- Modal vẫn giữ nguyên trạng thái",
       note="Nguồn: Improve list template r254, r391."),

    tc("Quick test — tester", "LIST-001", "Normal",
       "Ô tìm friend ở modal send test: click vào ô → tự hiện 20 friend đầu, scroll để load thêm",
       TESTER,
       "1. Mở modal preview/send test\n2. Click vào ô tìm kiếm (chưa nhập gì)\n3. Đếm số friend hiện ra\n"
       "4. Scroll xuống cuối danh sách gợi ý\n5. Quan sát placeholder của ô",
       "Bot A có 25 friend",
       "- Click vào ô → tự động hiện 20 friend đầu tiên trong danh sách bạn bè\n"
       "- Scroll xuống cuối → load thêm các friend còn lại (load more)\n- Ô có placeholder đúng design",
       note="Nguồn: Task nhỏ+ check Bug Kh r10 (yêu cầu suggestion giống booking calendar, load 20 rồi "
            "scroll load more) + Improve list template r255-r257, r392-r394."),

    tc("Quick test — tester", "FUNC-001", "Normal",
       "Search friend theo tên LINE (đúng / gần đúng) → ra kết quả, có scroll khi nhiều",
       TESTER,
       "1. Mở modal send test\n2. Nhập「テスト太郎」(toàn phần) → quan sát\n"
       "3. Nhập「テスト」(1 phần) → quan sát\n4. Nhập keyword khớp nhiều friend → scroll danh sách kết quả",
       "「テスト太郎」/「テスト」/ keyword khớp >20 friend",
       "- Search toàn phần và 1 phần đều trả về friend「テスト太郎」\n"
       "- Khi kết quả nhiều: danh sách có scroll, xem được hết kết quả",
       note="Nguồn: Improve list template r258-r262, r395-r399."),

    tc("Quick test — tester", "FUNC-001", "Abnormal",
       "Search tên LINE không tồn tại → không hiện friend nào",
       TESTER,
       "1. Mở modal send test\n2. Nhập「存在しない友だちXYZ」\n3. Quan sát danh sách gợi ý",
       "keyword không khớp friend nào",
       "- Danh sách gợi ý trống, không hiện friend nào\n- Không hiện lỗi hệ thống",
       note="Nguồn: Improve list template r263, r400."),

    tc("Quick test — tester", "FUNC-001", "Normal",
       "Đăng ký tài khoản test: search → bấm「追加」→ friend vào danh sách account test, nút add chuyển disable",
       TESTER,
       "1. Mở modal send test\n2. Search「テスト太郎」→ bấm「追加」\n"
       "3. Quan sát danh sách account test và nút「追加」của friend vừa add\n"
       "4. Search lại chính friend đó → quan sát nút「追加」",
       "friend「テスト太郎」",
       "- Danh sách account test có thêm「テスト太郎」\n"
       "- Nút「追加」của friend vừa add chuyển sang trạng thái DISABLE\n"
       "- Search lại friend đó vẫn thấy nút ở trạng thái disable",
       note="Nguồn: Improve list template r265-r267, r402-r405."),

    tc("Quick test — tester", "CONC-001", "Abnormal",
       "Double click nút「追加」(đang enable) → chỉ thêm 1 lần vào danh sách account test",
       TESTER,
       "1. Search「テスト太郎」\n2. Double click nhanh nút「追加」\n3. Đếm số dòng「テスト太郎」trong danh sách account test",
       "double click",
       "- Chỉ có ĐÚNG 1 dòng「テスト太郎」trong danh sách account test\n- Không tạo bản ghi tester trùng lặp",
       note="Nguồn: Improve list template r264, r401."),

    tc("Quick test — tester", "CONC-001", "Abnormal",
       "Double click nút「追加」khi đã DISABLE → không có tác dụng, không lỗi",
       TESTER + "\n- 「テスト太郎」đã được đăng ký làm account test",
       "1. Search「テスト太郎」→ nút「追加」đang disable\n2. Double click vào nút disable\n3. Quan sát danh sách",
       "double click trên nút disable",
       "- Không thêm bản ghi nào; danh sách account test không đổi\n- Không hiện lỗi hệ thống",
       note="Nguồn: Improve list template r267, r404."),

    tc("Quick test — tester", "FUNC-001", "Normal",
       "Xóa friend khỏi danh sách account test → mất khỏi danh sách, nút「追加」enable trở lại",
       TESTER + "\n- Đã đăng ký「テスト太郎」và 1 friend khác làm account test",
       "1. Mở modal send test\n2. Bấm icon xóa ở dòng「テスト太郎」→ xác nhận\n"
       "3. Quan sát danh sách account test\n4. Search lại「テスト太郎」→ quan sát nút「追加」",
       "2 account test, xóa 1",
       "- 「テスト太郎」mất khỏi danh sách account test, friend còn lại vẫn nguyên\n"
       "- Nút「追加」của「テスト太郎」trở lại trạng thái ENABLE",
       note="Nguồn: Improve list template r268, r281-r283, r405, r419-r421."),

    tc("Quick test — tester", "LIST-001", "Normal",
       "Danh sách account test: chưa scroll khi ít, có scroll khi nhiều",
       TESTER,
       "1. Đăng ký 3 account test → quan sát danh sách\n"
       "2. Đăng ký thêm cho tới 15 account test → quan sát danh sách",
       "3 rồi 15 account test",
       "- Với 3 account: danh sách hiện hết, không có thanh scroll\n"
       "- Với 15 account: danh sách có thanh scroll, scroll xem được đủ 15 dòng",
       note="Nguồn: Improve list template r269-r271, r406-r408."),

    tc("Quick test — tester", "FUNC-001", "Normal",
       "Bật quick send cho friend → hiện thông báo, tối đa 3 user được bật",
       TESTER + "\n- Đã đăng ký 5 account test, chưa ai bật quick send",
       "1. Mở modal send test\n2. Hover vào icon quick send của 1 friend → quan sát tooltip\n"
       "3. Click icon → quan sát trạng thái\n4. Bật tiếp cho friend thứ 2 và thứ 3\n"
       "5. Hover icon quick send của friend thứ 4 → quan sát tooltip\n6. Click vào icon của friend thứ 4",
       "5 account test, bật quick send lần lượt",
       "- Hover khi dưới 3 user: hiện tooltip「クイックテストユーザーに登録（3人まで)」, click được → icon enable\n"
       "- Sau khi có 3 user quick send: hover icon friend thứ 4 vẫn hiện tooltip nhưng "
       "KHÔNG bật được icon cho friend thứ 4 (chặn ở giới hạn 3 người)",
       note="Nguồn: Improve list template r284-r290, r422-r428. Giới hạn 3 user quick send KHÔNG có "
            "trong spec → xem MT-15."),

    tc("Quick test — tester", "FUNC-001", "Normal",
       "Tắt quick send cho friend đang bật → hiện thông báo giải trừ, friend rời khỏi list quick send",
       TESTER + "\n- Đã có 3 friend đang bật quick send",
       "1. Hover vào icon quick send của 1 friend ĐANG bật → quan sát tooltip\n2. Click icon\n"
       "3. Quan sát trạng thái icon và số lượng user quick send\n"
       "4. Hover icon của 1 friend chưa bật → click",
       "3 friend đang bật quick send",
       "- Hover friend đang bật: hiện tooltip「クイックテストユーザーの登録を解除」\n"
       "- Click → friend đó bị loại khỏi list quick send, còn 2 user\n"
       "- Sau đó bật được cho 1 friend khác (vì đã dưới 3)",
       note="Nguồn: Improve list template r287-r288, r425-r426."),

    tc("Quick test — tester", "UI-003", "Normal",
       "Chưa đăng ký tester → text「テストユーザーが登録されていません」click được để mở modal đăng ký",
       ADM + "\n- Bot A CHƯA đăng ký クイックテストユーザー nào\n- Folder F1 có group G1 dạng パネル・ボタン",
       "1. Mở màn list template\n2. Quan sát cột「クイックテスト」của dòng G1\n"
       "3. Click vào text「テストユーザーが登録されていません」\n4. Quan sát modal mở ra",
       "0 tester",
       "- Cột「クイックテスト」hiện text「テストユーザーが登録されていません」\n"
       "- Click → mở modal preview - send test, trong đó có phần tìm và đăng ký tester\n"
       "- Preview trong modal hiện đúng nội dung template button",
       note="Nguồn: Task nhỏ+ check Bug Kh r45 + Improve list template r253. "
            "Text tương ứng ở màn scenario là「クイックテストユーザー未登録」, ở broadcast là「クイックテスト未設定」."),

    # ═════════════ 12. Quick test — gửi & preview ═════════════
    tc("Quick test — gửi & preview", "MSG-001", "Normal",
       "Gửi test cho TỪNG friend → friend nhận đủ tin của mọi template con trong group",
       GRP + "\n- Đã đăng ký 1 account test là friend U1",
       "1. Mở modal send test của G1\n2. Quan sát trạng thái nút「テスト送信」\n"
       "3. Bấm「テスト送信」ở dòng U1\n4. Quan sát thông báo\n"
       "5. Mở LINE của U1 và đếm/đối chiếu từng tin nhận được\n6. Mở chat 1:1 của U1 trên tool",
       "G1 có 3 template con (text, パネル・ボタン, 画像)",
       "- Bấm「テスト送信」→ hiện thông báo gửi thành công\n"
       "- U1 nhận đúng 3 tin trên LINE, đúng thứ tự T1 → T2 → T3, nội dung khớp template\n"
       "- Chat 1:1 trên tool cũng hiện 3 tin vừa gửi\n- `bots.free_send_count` tăng đúng số lần gửi",
       note="Nguồn: Improve list template r272-r275, r410-r413. RULE-06 (đi tới LINE app) + "
            "RULE-07 (DB + màn hình + output)."),

    tc("Quick test — gửi & preview", "CONC-001", "Abnormal",
       "Double click nút「テスト送信」→ chỉ gửi 1 lần",
       GRP + "\n- Đã đăng ký account test U1",
       "1. Mở modal send test\n2. Double click nhanh nút「テスト送信」ở dòng U1\n"
       "3. Đếm số tin U1 nhận được trên LINE",
       "double click, group 3 template con",
       "- U1 nhận đúng 3 tin (1 lượt gửi), KHÔNG nhận 6 tin\n- Không hiện lỗi hệ thống",
       note="Nguồn: Improve list template r273, r411."),

    tc("Quick test — gửi & preview", "BULK-001", "Normal",
       "Gửi test hàng loạt (一括テスト送信): disable khi chưa tick, gửi đủ cho mọi friend đã tick",
       GRP + "\n- Đã đăng ký 3 account test U1, U2, U3",
       "1. Mở modal send test, không tick friend nào → quan sát nút「一括テスト送信」\n"
       "2. Tick U1 và U2 → quan sát nút\n3. Bấm「一括テスト送信」\n"
       "4. Mở LINE của U1, U2 và U3 → đối chiếu tin nhận được",
       "3 account test, tick 2",
       "- Chưa tick: nút「一括テスト送信」disable; tick ≥1: enable\n"
       "- U1 và U2 mỗi người nhận đủ 3 tin của G1, đúng thứ tự và nội dung\n"
       "- U3 (không tick) KHÔNG nhận tin nào",
       note="Nguồn: Improve list template r276-r280, r414-r418."),

    tc("Quick test — gửi & preview", "CONC-001", "Abnormal",
       "Double click nút「一括テスト送信」→ mỗi friend chỉ nhận 1 lượt tin",
       GRP + "\n- Đã đăng ký 2 account test U1, U2 và tick cả 2",
       "1. Double click nhanh nút「一括テスト送信」\n2. Đếm số tin U1 và U2 nhận được",
       "double click, 2 friend, group 3 template con",
       "- U1 và U2 mỗi người nhận đúng 3 tin, không bị 6 tin\n- Không hiện lỗi hệ thống",
       note="Nguồn: Improve list template r277, r415."),

    tc("Quick test — gửi & preview", "OUT-PREVIEW-001", "Normal",
       "Preview trong modal hiện đủ template con của group, đúng thứ tự, có scroll khi nhiều",
       GRP + "\n- Chuẩn bị thêm group G5 có 12 template con đủ các loại",
       "1. Mở modal preview của G1 → đếm và đối chiếu các khối preview\n"
       "2. Đóng, mở modal preview của G5 → scroll xuống cuối\n"
       "3. Đối chiếu thứ tự preview với thứ tự trong màn list template con",
       "G1 = 3 template con; G5 = 12 template con",
       "- Preview hiện đủ tất cả template con của group\n"
       "- Thứ tự preview KHỚP thứ tự trong màn list template con\n"
       "- Với 12 template con: vùng preview có scroll, xem được hết",
       note="Nguồn: Improve list template r291, r301-r303, r429, r439."),

    tc("Quick test — gửi & preview", "OUT-PREVIEW-001", "Normal",
       "Preview hiện đúng cho cả 4 sub-type button, 3 loại media, sticker và location",
       ADM + "\n- Group G6 có 9 template con: button standard / color / image / quick reply, "
             "image / video / audio, stamp, location",
       "1. Mở modal preview của G6\n2. Đối chiếu từng khối preview với dữ liệu đã cấu hình\n"
       "3. So sánh với tin nhận được trên LINE khi gửi test G6",
       "9 template con phủ đủ loại",
       "- Mỗi loại hiện đúng dạng preview đặc trưng (panel + nút, panel màu, panel ảnh, quick reply, "
       "ảnh, video có thumbnail, audio, sticker, bản đồ vị trí)\n"
       "- Nội dung preview khớp với tin thật nhận được trên LINE",
       note="Nguồn: Improve list template r292-r300, r430-r438."),

    tc("Quick test — gửi & preview", "MEDIA-001", "Normal",
       "Click vào ảnh / video / audio trong preview → mở xem được, double click không lỗi",
       ADM + "\n- Group G7 có 3 template con: 画像, 動画 (có thumbnail), 音声",
       "1. Mở modal preview của G7\n2. Click vào khối video → quan sát\n3. Đóng, click vào khối ảnh → quan sát\n"
       "4. Đóng ảnh bằng nút đóng và bằng click ra ngoài\n5. Click vào khối audio → quan sát\n"
       "6. Double click liên tiếp vào ảnh, video, audio",
       "3 template media",
       "- Click video → mở preview video, phát được\n- Click ảnh → mở ảnh full, đóng được bằng cả 2 cách\n"
       "- Click audio → phát được audio\n- Double click không mở trùng lặp, không lỗi",
       note="Nguồn: Improve list template r447-r452."),

    tc("Quick test — gửi & preview", "FUNC-001", "Normal",
       "Sửa template con rồi mở lại preview → preview cập nhật nội dung mới",
       GRP,
       "1. Mở modal preview của G1 → ghi nhận nội dung T1\n2. Đóng modal, vào sửa nội dung T1, lưu\n"
       "3. Mở lại modal preview của G1 → đối chiếu T1",
       "T1 đổi nội dung",
       "- Preview lần 2 hiện nội dung MỚI của T1, không còn nội dung cũ (không bị cache)",
       note="Nguồn: Improve list template r304."),

    # ═════════════ 13. Preview ở các màn khác ═════════════
    tc("Preview ở các màn khác", "OUT-PREVIEW-001", "Normal",
       "Preview template button standard ở 12 điểm của màn TEMPLATE → giống hệt tin gửi cho user",
       ADM + "\n- Có 4 template button standard: 1 panel không ảnh, 1 panel có ảnh, "
             "nhiều panel không ảnh, nhiều panel có ảnh\n- Bot A chưa đăng ký quick test user",
       "1. Màn list template: click text「テストユーザーが登録されていません」→ modal preview\n"
       "2. Màn list template: click icon preview\n3. Màn list template con: bấm nút「プレビュー・テスト」\n"
       "4. Màn list template con: click icon preview của 1 template con\n"
       "5. Màn TẠO template button: xem preview panel và preview khi scroll\n"
       "6. Màn SỬA template button: preview panel, preview khi scroll, và sau khi add thêm button\n"
       "7. Màn COPY template button: preview panel và preview khi scroll\n"
       "8. Gửi cùng template đó cho 1 friend và so sánh",
       "4 biến thể button standard × 12 điểm preview trong màn template",
       "- Preview ở cả 12 điểm hiện GIỐNG với tin nhắn thật khi gửi cho user\n"
       "- Text hiển thị màu xanh #3771BE, chữ gầy, background trắng, KHÔNG có border\n"
       "- Dưới title là gạch ngang, title KHÔNG có border",
       note="Nguồn: Task nhỏ+ check Bug Kh r45-r56 (Review #30710 + Review 11/2025). "
            "Gộp 12 điểm vì CÙNG 1 kết quả mong đợi; liệt kê đủ điểm ở cột Các bước."),

    tc("Preview ở các màn khác", "OUT-PREVIEW-001", "Normal",
       "Preview template button standard ở 16 điểm của màn SCENARIO → giống tin gửi cho user",
       ADM + "\n- Có scenario S1 với ≥2 step, mỗi step có ≥1 message dạng button standard\n"
             "- 4 biến thể button standard như trên",
       "1. Màn tạo template button trong scenario: preview panel + preview khi scroll\n"
       "2. Màn sửa template button trong scenario: preview panel, preview khi scroll, sau khi add button\n"
       "3. Modal chọn template để add vào step message → nút「プレビュー」\n"
       "4. Nút preview của 1 message trong step\n5. Icon menu 3 gạch → preview all message của 1 step\n"
       "6. Menu 3 gạch → send test → preview all message của step\n"
       "7. Nút「一括操作」→ nút preview\n8. 「一括操作」→「引用登録」→ preview ở modal copy step msg\n"
       "9. Nút「一括プレビュー」ở màn detail scenario\n10. 「一括プレビュー」→ nút edit → modal preview\n"
       "11. Click text「クイックテストユーザー未登録」\n12. Đổi đối tượng filter rồi lặp lại các preview trên",
       "4 biến thể button standard × 16 điểm preview trong scenario",
       "- Preview ở cả 16 điểm hiện GIỐNG tin nhắn thật khi gửi cho user\n"
       "- Text màu xanh #3771BE, chữ gầy, background trắng, KHÔNG border; dưới title là gạch ngang",
       note="Nguồn: Task nhỏ+ check Bug Kh r57-r72. ⚠ TC gốc r63 có note「Lệch ảnh」ở modal chọn "
            "template để add vào step → cần kiểm lại điểm này kỹ."),

    tc("Preview ở các màn khác", "OUT-PREVIEW-001", "Normal",
       "Preview template button standard ở 13 điểm của màn BROADCAST → giống tin gửi cho user",
       ADM + "\n- Có broadcast ở cả 3 trạng thái: đợi gửi, draft, đã gửi\n- 4 biến thể button standard",
       "1. Màn tạo template button trong broadcast: preview panel + preview khi scroll\n"
       "2. Màn sửa template button trong broadcast: preview panel, preview khi scroll, sau khi add button\n"
       "3. Màn list broadcast → nút preview ở list đợi gửi / list draft / list đã gửi\n"
       "4. Modal chọn template để add vào broadcast → nút「プレビュー」\n"
       "5. Click text「クイックテスト未設定」→ modal preview-send test\n"
       "6. Nút「配信内容を確認して送信に進む」\n7. Nút「プレビューとテスト」",
       "4 biến thể button standard × 13 điểm preview trong broadcast",
       "- Preview ở cả 13 điểm hiện GIỐNG tin nhắn thật khi gửi cho user\n"
       "- Text màu xanh #3771BE, chữ gầy, background trắng, KHÔNG border; dưới title là gạch ngang",
       note="Nguồn: Task nhỏ+ check Bug Kh r73-r85."),

    tc("Preview ở các màn khác", "OUT-PREVIEW-001", "Normal",
       "Preview template button standard ở 8 điểm của màn REMIND → giống tin gửi cho user",
       ADM + "\n- Có 1 remind với ≥2 step message dạng button standard",
       "1. Màn tạo template button trong remind: preview panel + preview khi scroll\n"
       "2. Màn sửa template button trong remind: preview panel + preview khi scroll\n"
       "3. Modal chọn template để add vào remind → nút「プレビュー」\n"
       "4. Màn edit message của 1 step remind → nút「プレビュー」\n"
       "5. Màn list step của remind: icon preview của 1 step và nút preview all",
       "4 biến thể button standard × 8 điểm preview trong remind",
       "- Preview ở cả 8 điểm hiện GIỐNG tin nhắn thật khi gửi cho user\n"
       "- Text màu xanh #3771BE, chữ gầy, background trắng, KHÔNG border; dưới title là gạch ngang",
       note="Nguồn: Task nhỏ+ check Bug Kh r86-r93."),

    tc("Preview ở các màn khác", "OUT-PREVIEW-001", "Normal",
       "Preview ở màn CHAT 1:1 giữ nguyên style CŨ (không đổi theo Review #30710)",
       ADM + "\n- 4 biến thể button standard đã tạo",
       "1. Mở chat 1:1 của 1 friend\n2. Bấm「テンプレート送信」→ chọn template button standard\n"
       "3. Quan sát preview trong modal\n4. So sánh với preview ở màn template",
       "4 biến thể button standard",
       "- Preview ở chat 1:1 giữ style CŨ, KHÔNG áp style mới (text xanh #3771BE / bỏ border)\n"
       "- Đây là hành vi chủ ý, không phải bug",
       note="Nguồn: Task nhỏ+ check Bug Kh r94 (「màn chat 1:1 preview vẫn như cũ, không sửa」)."),

    tc("Preview ở các màn khác", "REG-SHARED-001", "Normal",
       "Preview các sub-type button KHÁC (color / image / quick reply) không bị đổi so với trước",
       ADM + "\n- Có template button color, button ảnh, button quick reply",
       "1. Mở preview 3 loại button trên ở màn template\n2. Lặp lại ở màn scenario\n"
       "3. Lặp lại ở màn broadcast\n4. Lặp lại ở màn remind",
       "3 sub-type × 4 màn",
       "- Cả 4 màn: preview 3 sub-type này hiện như TRƯỚC khi áp thay đổi của Review #30710\n"
       "- Không loại nào bị đổi màu chữ / bỏ border ngoài ý muốn",
       note="Nguồn: Task nhỏ+ check Bug Kh r95-r98. regression — chỉ button standard được đổi style."),

    tc("Preview ở các màn khác", "OUT-PREVIEW-001", "Normal",
       "Preview template button ở màn edit group / list template với folder 未分類 (group = 0) có nhánh code riêng",
       ADM + "\n- Folder 未分類 có group G0 chứa 4 template con: button standard / color / image / quick reply\n"
             "- Folder F1 (category_id > 0) có group G1 chứa 4 template con tương tự",
       "1. Mở màn edit group của G0 (thuộc 未分類) → xem preview 4 loại button\n"
       "2. Mở màn list template của 未分類 → xem preview 4 loại button\n"
       "3. Lặp lại bước 1-2 với G1 thuộc folder F1\n4. So sánh preview của 2 nhóm",
       "G0 ở 未分類 (category_id = 0) và G1 ở F1 (category_id > 0)",
       "- Preview 4 loại button ở 未分類 GIỐNG hệt preview ở folder thường\n"
       "- Không có loại nào bị mất ảnh / mất nút / sai màu ở nhánh 未分類",
       note="Nguồn: Task nhỏ+ check Bug Kh r1049-r1124 (TC gốc ghi rõ「folder chưa phân loại — "
            "do chỗ này code riêng」). Rủi ro nhánh code riêng của category_id = 0 → xem MT-18."),

    tc("Preview ở các màn khác", "MSG-001", "Normal",
       "Sau khi đổi style preview → gửi template button qua web và job vẫn bình thường",
       ADM + "\n- Có template button standard đã cấu hình đủ panel + nút + action",
       "1. Gửi qua web: send test, send ở màn chat 1:1, gửi bằng action\n"
       "2. Gửi qua job: step message của scenario, broadcast, remind, action theo lịch\n"
       "3. Với mỗi lượt, quan sát tin trên LINE của friend",
       "7 đường gửi (3 web + 4 job)",
       "- Cả 7 đường gửi đều gửi được template button bình thường\n"
       "- Tin trên LINE hiện đủ panel, ảnh, title, nội dung và các nút; bấm nút vẫn ra action đã set",
       note="Nguồn: Task nhỏ+ check Bug Kh r101-r107. regression sau Review #30710. "
            "Gộp 7 đường gửi vì CÙNG 1 kết quả mong đợi."),
]

# ── Cột「Trạng thái đánh giá spec」──
# Quy tắc: TC tham chiếu ít nhất 1 mã MÂU THUẪN thuộc nhóm SPEC-SILENT (spec không ghi / spec tự
# nhậ­n chưa rõ) →「Spec không ghi」. Các MT còn lại là trưồng hợp spec CÓ ghi nhưng LỆCH với TC
# → giữ「Spec ghi rõ」. TC do AI suy luậ­n mà cả corpus và spec đều không có cũng đánh「Spec không ghi」.
_SPEC_SILENT_MT = {
    "MT-04", "MT-08", "MT-09", "MT-10", "MT-11", "MT-12", "MT-13", "MT-14", "MT-15", "MT-16",
    "MT-17", "MT-18", "MT-19", "MT-20", "MT-21", "MT-22", "MT-23", "MT-24", "MT-25", "MT-26",
    "MT-27", "MT-28", "MT-29", "MT-30", "MT-31", "MT-32", "MT-34", "MT-35", "MT-36", "MT-37",
    "MT-39", "MT-41", "MT-42", "MT-43", "MT-45", "MT-47", "MT-48", "MT-49",
}
_AI_INFER = "SUY LUẬN CỦA AI"
for _r in S2:
    _mts = set(_re.findall(r"MT-\d+", _r["note"]))
    if _mts & _SPEC_SILENT_MT or _AI_INFER in _r["note"]:
        _r["spec"] = "Spec không ghi"
