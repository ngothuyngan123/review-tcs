# -*- coding: utf-8 -*-
"""FA-031 契約プラン・決済情報 (Bill tiền tool) — Các điểm MÂU THUẪN giữa kho TCs tổng hợp và spec-features.
Trạng thái: TOÀN BỘ đang CHỜ QUYẾT ĐỊNH của Leader (chưa mục nào được chốt).

Nguồn TCs: TCsLine_Bill tiền_Improve2025 (9 tab) + TCsLine_Bill tiền (21 tab).
Nguồn spec: spec-features/admin/billing-plan/ (feature-spec.md · web/logic-spec.md · web/api-spec.md ·
            job/job-spec.md · db/db-mapping.md · ui/ui-spec.md).
"""

COLS = ["ID", "Mức độ", "Trạng thái", "Chủ đề", "TCs nói gì (nguồn)", "Spec nói gì (nguồn)",
        "Vì sao mâu thuẫn", "TC liên quan", "QUYẾT ĐỊNH CỦA LEADER",
        "Việc phải làm tiếp"]

W = "⏳ CHỜ QUYẾT ĐỊNH"

CONFLICTS = [
    # ══════════════ PHẠM VI (scope) — quyết trước, ảnh hưởng cả kho ══════════════
    ["MT-00", "CAO", W,
     "PHẠM VI: màn mua mới / upgrade plan có thuộc FA-031 không?",
     "Tab「Màn hình bill tiền」(531 TC lá) và「List main case」(347 dòng) là bộ TC lớn nhất của corpus, "
     "toàn bộ nói về màn「プラン選択」, màn xác nhận plan, màn nhập thẻ, màn thông tin chuyển khoản — "
     "tức luồng TẠO hợp đồng mới và UPGRADE.",
     "`feature-spec.md:26` §1 Phạm vi ghi rõ: 「Không bao gồm: **tạo hợp đồng mới**, thay đổi thẻ thanh toán "
     "(endpoint chưa phân tích đầy đủ — xem mục 9)」. Danh sách màn hình §1 chỉ có 5 màn SCR-BLP-01..05, "
     "KHÔNG có màn chọn plan / màn xác nhận plan.",
     "Nếu theo spec thì phải loại ~250 TC khỏi kho FA-031 và mở 1 kho riêng; nếu theo corpus thì phải "
     "bổ sung spec cho 4 màn còn thiếu. Đây là quyết định về ranh giới feature, ảnh hưởng toàn bộ kho — "
     "phải chốt TRƯỚC khi review nội dung từng TC.",
     "Toàn bộ nhóm『Màn chọn plan』『Rule slot trống & bot free』『Xác nhận plan — mua mới』"
     "『Xác nhận plan — upgrade』『Nhập thẻ & 3D Secure』『Chuyển khoản — tạo & thông tin tài khoản』", "",
     ""],

    ["MT-00b", "CAO", W,
     "PHẠM VI: refund + affiliate + màn admin nội bộ có thuộc FA-031 không?",
     "TCsLine_Bill tiền có 3 tab thao tác từ ADMIN PORTAL NỘI BỘ: 「Logic refund」(21 TC), "
     "「Refund update 1.0」(12 TC), 「Bill tiền/ phân bổ/ TOP」(18 TC — màn bill tiền / phân bổ / TOP của admin). "
     "Refund làm thay đổi trực tiếp `bot_contracts` (status=3, contract_type=free, expired_date lùi kỳ).",
     "`feature-spec.md:20` §1 Actors chỉ có Admin (chủ tài khoản LME), Staff, System Jobs — KHÔNG có "
     "super-admin/OEM. `feature-spec.md` §2 chỉ mô tả 5 màn thuộc portal `/basic/` và `/admin/plan-estimation`.",
     "Refund là thao tác của người vận hành nội bộ nhưng HẬU QUẢ nằm hết trong FA-031 (trạng thái hợp đồng, "
     "hóa đơn, hoa hồng). Bỏ hẳn thì mất mảng rủi ro tiền bạc lớn; giữ lại thì kho FA-031 lẫn màn của portal khác.",
     "Toàn bộ nhóm『Hoàn tiền』(7 TC)", "",
     ""],

    ["MT-00c", "TRUNG BÌNH", W,
     "PHẠM VI: Tutorial onboarding (tab Campaign + Tutorial) có thuộc FA-031 không?",
     "Tab「Campaign + Tutorial」(265 TC) gộp 2 chủ đề: (a) Campaign 初月無料 khi upgrade plan — "
     "gắn trực tiếp với hợp đồng; (b) Tutorial onboarding (modal ようこそ, floating banner, "
     "job ScanHasTutorial) — hoàn toàn về trải nghiệm người dùng mới, không liên quan tiền.",
     "`feature-spec.md` KHÔNG nhắc campaign lẫn tutorial ở bất kỳ mục nào; job §7 không có "
     "`job:ScanHasCampaign` / `job:ScanHasTutorial`.",
     "Kho hiện GIỮ phần campaign (13 TC, vì ảnh hưởng expired_date và số tiền) và LOẠI phần tutorial. "
     "Cần Leader xác nhận cách chia này, hoặc tách tutorial sang kho onboarding (`TCsLine_AddBot`).",
     "Nhóm『Campaign 初月無料』(13 TC); phần Tutorial hiện KHÔNG có TC nào trong kho", "",
     ""],

    # ══════════════ Mức CAO ══════════════
    ["MT-01", "CAO", W,
     "Nút 振込キャンセル: chỉ hiện cho mua mới, hay còn hiện cho hợp đồng chờ chuyển khoản khác?",
     "「Quản lý hợp đồng」r1515 (Specchange 03/2026, 20/04/2026) ghi RÕ: 「Nút hủy chuyển khoản 振込キャンセル "
     "**chỉ hiển thị cho case mua hợp đồng lần đầu** (Không hiển thị cho các case update hợp đồng, bill job...)」, "
     "r1523-r1528 xác nhận case update chỉ hiện 契約詳細.\n"
     "NHƯNG r1525-r1526 lại ghi hợp đồng lại (再契約) — vốn KHÔNG phải mua lần đầu — VẪN hiện 振込キャンセル.\n"
     "Và Bug KH #36835 (28/05/2026, sau spec change 1 tháng) báo ngược: 「Status chuyển khoản NH đang là "
     "入金待ち nhưng nút Hủy chuyển khoản KHÔNG hiển thị」.",
     "`feature-spec.md:123` bảng 'Nút Action theo trạng thái' ghi 「振込キャンセル | Status là 入金待ち "
     "(**điều kiện cụ thể chưa xác nhận đầy đủ**)」. `feature-spec.md` §9 [N11] tự nhận: 「Điều kiện cụ thể "
     "hiển thị button 振込キャンセル vs 契約詳細 khi status 入金待ち — cần xem code」.",
     "Nút này XÓA HẲN bản ghi hợp đồng ở case mua mới. Hiện sai chỗ → user hủy nhầm hợp đồng đang chờ tiền; "
     "ẩn sai chỗ → user không hủy được và bị treo tiền. Spec tự nhận không biết điều kiện, corpus thì có 3 "
     "phát biểu không thống nhất.",
     "Nhóm『Hủy chuyển khoản』TC 1-3", "",
     ""],

    ["MT-02", "CAO", W,
     "Hủy chuyển khoản khi hợp đồng cũ quá hạn: mốc 7 ngày cho kết quả gì?",
     "「List main case」r35-r37 ghi 3 nhánh RÕ RÀNG: Case1 `expired > now` → back về hợp đồng cũ; "
     "Case2 `expired < now && expired+7 > now` → **Overdue**; Case3 `expired+7 < now` → **Đã hủy**.\n"
     "NHƯNG「Quản lý hợp đồng」r81-r86 (28 dòng) chỉ ghi 2 nhánh và ĐẢO chiều bất đẳng thức: "
     "「1. Expired_date > now → Back về hợp đồng cũ; 2. **Expired_date + 7 > now → Hiển thị Status = Đã hủy**」\n"
     "Trong khi r95-r102 (cùng tab, khối 口座発行中) lại ghi đủ 3 nhánh giống List main case.",
     "`feature-spec.md:606` BR-05 chỉ mô tả khôi phục theo `reason` (upgradeFromFree / upgradeFromStandard / "
     "extendContract / mặc định hủy hoàn toàn), **KHÔNG nhắc mốc 7 ngày** và không nêu điều kiện overdue.",
     "Cùng 1 nút, cùng 1 tab, 2 khối viết ngược nhau về mốc 7 ngày. Member chạy theo khối r81-r86 sẽ báo PASS "
     "khi hệ thống hủy hợp đồng của khách vẫn còn trong 7 ngày ân hạn — mất hợp đồng đang có tiền.",
     "Nhóm『Hủy chuyển khoản』TC 5-7", "",
     ""],

    ["MT-03", "CAO", W,
     "Upgrade bằng chuyển khoản mà callback FAIL: về plan cũ hay giữ plan mới rồi cancel?",
     "「Màn hình bill tiền」r414, r418, r423, r427 (luồng upgrade thường): 「Hợp đồng KHÔNG được upgrade: "
     "Hiển thị plan hợp đồng là **free**, các tính năng vẫn bị giới hạn theo bot free」.\n"
     "「Bill max friend」r15, r17 (luồng upgrade do vượt mốc bạn bè) ghi NGƯỢC: 「**Spec mới**: bot vẫn giữ "
     "nguyên plan pro và chuyển thành **cancel hợp đồng**」.",
     "`feature-spec.md:606` BR-05 chỉ nói 「Upgrade từ free (upgradeFromFree) → Về lại free plan, "
     "contract_bill_type=month, payment_method=card」— tức theo phương án 1, KHÔNG có nhánh 'giữ plan + cancel'.",
     "Cùng một sự kiện (callback fail sau upgrade transfer) nhưng 2 luồng cho ra 2 trạng thái cuối khác nhau. "
     "Nếu thực tế chỉ có 1 nhánh mà TC viết 2 kiểu thì một trong hai bộ TC sẽ báo PASS sai. Ảnh hưởng trực tiếp "
     "tới quyền dùng tính năng của khách.",
     "Nhóm『Xác nhận plan — upgrade』TC 8; nhóm『Bill max friend — cảnh báo & upgrade』TC 6", "",
     ""],

    ["MT-04", "CAO", W,
     "Lịch retry khi bill lỗi: đếm theo 'ngày 1/2/3/6/7' hay theo status_payment_fail 1→5?",
     "「Màn hình bill tiền」r448-r453, r584-r591 mô tả theo NGÀY: 「fail ngày 1 · fail ngày 2 · fail ngày 3 · "
     "fail ngày 6 · **fail ngày 7 → update status =3 (hủy hợp đồng)**」— tức 7 lần chạy job.",
     "`feature-spec.md:585` BR-03 mô tả theo `status_payment_fail`: 「1 → retry ngay hôm đó (23:59:59) | "
     "2 → retry sau **+2 ngày** | 3 → retry sau **+5 ngày** | 4 → retry sau **+6 ngày** | "
     "5 → **force cancel**」— tức chỉ 5 lần thử, trải trên ~14 ngày.",
     "Hai cách đếm cho ra tổng số ngày ân hạn hoàn toàn khác nhau (7 ngày vs ~14 ngày) và số lần charge thẻ "
     "khách khác nhau (7 vs 5). Đồng thời mốc 'expired + 7 ngày' dùng ở nhiều chỗ khác (banner 強制解約, "
     "hủy chuyển khoản, chặn trang LINE user) — nếu BR-03 đúng thì các mốc kia sai, và ngược lại.",
     "Nhóm『Job bill định kỳ — thẻ』TC 6; nhóm『Cưỡng chế hủy & màn account đã hủy』TC 5", "",
     ""],

    ["MT-05", "CAO", W,
     "Job bill Stripe: đã dừng hay vẫn chạy?",
     "「Màn hình bill tiền」r575-r582 có 8 TC THẬT cho 「Check job bill tiền stripe」(bill tháng/năm, "
     "success/fail ngày 1/ngày 7), kèm bước 「check trên stripe: có 1 giao dịch」. "
     "Tab「Logic refund」r42 cũng ghi: 「Trước đây bill bằng stripe (hiện tại chuyển sang univapay) => "
     "nên hiện tại **vẫn có các bot được bill tự động (sau khi hết expired date) bằng job**」.",
     "`feature-spec.md:702` bảng Commands ghi `AutoPaymentJob` (`job:check_auto_payment`) = "
     "「**Đã comment — không chạy**」, Legacy Stripe — deprecated.\n"
     "NHƯNG `feature-spec.md:711` lại mô tả `AutoPaymentJobUnivapay` **Phase 1: Charge bằng Stripe (legacy)** "
     "→ `StripePayment::autoPaymentIntents(...)`. `feature-spec.md` §10 Open Question #6 cũng hỏi lại chính điều này.",
     "Spec tự mâu thuẫn trong cùng 1 mục (§7): command Stripe ghi không chạy nhưng Phase 1 của job đang chạy "
     "lại charge Stripe. Nếu Stripe còn sống mà QA bỏ test thì mọi lỗi trên nhánh này lọt hết ra khách; "
     "nếu đã chết mà vẫn test thì tốn công vô ích.",
     "Nhóm『Job bill định kỳ — thẻ』TC 11", "",
     ""],

    ["MT-06", "CAO", W,
     "Công thức tính expired_date khi datetime_first_payment là ngày 29/30/31",
     "「Màn hình bill tiền」r497-r548 liệt kê BẢNG GIÁ TRỊ CỤ THỂ cho từng tháng, nhưng quy luật không nhất quán:\n"
     "- ngày 29: 「Bill đúng vào ngày 29 → **next expired_date = ngày 28**」(lùi 1 ngày ở MỌI tháng)\n"
     "- ngày 30: tháng 2→30/3, tháng 3→**29/4**, tháng 4→30/5, tháng 5→**29/6** (lúc 29 lúc 30)\n"
     "- ngày 31: tháng 3→30/4, tháng 4→31/5, tháng 5→30/6 (lùi về ngày cuối rồi quay lại 31)\n"
     "Tab「Cố định ngày bill tiền」r5, r6 (07/2023) lại mô tả quy tắc khác: 「Tháng tiếp theo nếu không có "
     "ngày 31 thì expired_date sẽ là ngày 30 của tháng đó; lần bill tiếp theo nữa nếu tháng có ngày 31 thì "
     "**lấy lại ngày 31**」.",
     "`feature-spec.md` KHÔNG có mục nào mô tả cách tính `expired_date_contract` theo ngày trong tháng. "
     "`db-mapping.md` chỉ khai báo cột. Cột `datetime_first_payment` cũng KHÔNG có trong Field Traceability Matrix §4.",
     "Đây là công thức tính NGÀY TRỪ TIỀN của khách. Sai 1 ngày = trừ tiền sớm/muộn hoặc khóa tài khoản sai ngày "
     "(chính là Bug KH #26511 và Bug KH #35467 trong Info của file nguồn). Corpus có bảng giá trị nhưng không "
     "suy ra được công thức; spec không có gì để đối chiếu.",
     "Nhóm『Ngày bill & expired_date』TC 3, 4, 5", "",
     ""],

    ["MT-07", "CAO", W,
     "Số tiền bill max friend: 361円/ngày và 11.000円/tháng lấy từ đâu?",
     "「Bill max friend」r109, r151 ghi công thức: 「số tiền = **361 × số ngày remain**」với ví dụ "
     "「日割り 361円/日 × 356日 = 128.516円 (税込)」. r196-r205 ghi kỳ tiếp theo: 「số tiền bill = **11.000円**」. "
     "r105-r106 ghi bậc bạn bè: 10~20万人 / 20~30万人.",
     "`feature-spec.md:576` BR-02 chỉ ghi 「Phí tính bằng `calculateBillMaxFriend(totalFriend)` × 12 nếu year "
     "contract」— KHÔNG có con số, KHÔNG có bảng bậc, KHÔNG có đơn giá theo ngày. "
     "`feature-spec.md:597` BR-04 ghi 「Không có bảng plans/pricing riêng — giá hardcode trong config và helper」.",
     "Tester không có cách nào tự kiểm tra số tiền đúng hay sai ngoài việc tin vào con số trong TC cũ (12/2025). "
     "Nếu đơn giá đổi mà TC không đổi thì mọi lần test đều PASS sai. Đây là tiền thật của khách.",
     "Nhóm『Bill max friend — thanh toán & job』TC 1, 6", "",
     ""],

    ["MT-08", "CAO", W,
     "Bill max friend từ WEB: thẻ chính lỗi có fallback sang thẻ phụ không?",
     "「Bill max friend」r120 ghi nguyên văn câu hỏi–trả lời của tester: 「Bill maincard fail không chuyển sang "
     "bill subcard à? => **Không nhé**, vì trong design chỉ có 1 option là bill card thì bill bằng main card thôi」. "
     "r122, r163, r165: thẻ chính lỗi → 「Báo lỗi => Hiện màn nhập card mới」.\n"
     "NHƯNG r183, r188 (job bill max friend) lại ghi: 「bill main card fail → **Bill tiếp bằng sub card** success」.",
     "`feature-spec.md:731` §7 HandleBillMaxFriend ghi: 「Charge thẻ Univapay → **Fallback: charge thẻ phụ "
     "(SubcardBotContract)**」— tức spec CHỈ mô tả nhánh JOB, không mô tả nhánh web.",
     "Cùng một khoản phí, thanh toán từ web thì không fallback nhưng job thì có. Nếu đây là chủ ý thì phải ghi "
     "rõ vào spec; nếu là lỗi thì khách bị bill lỗi oan dù đã đăng ký thẻ phụ.",
     "Nhóm『Bill max friend — thanh toán & job』TC 4, 6", "",
     ""],

    ["MT-09", "CAO", W,
     "Mốc 30 ngày ân hạn của bot vượt 100.000 bạn bè",
     "「Bill max friend」r99-r103, r140-r145: 「check ngày hiện tại - ngày detect = 29 ngày → User access được "
     "các màn bình thường; = 30 ngày → bình thường; = **31 ngày → User KHÔNG được access các màn, redirect "
     "sang màn point-setting**」.",
     "`feature-spec.md:570` BR-02 chỉ mô tả 4 giá trị `bots.max_friend_plan` (0/1/2/3) và điều kiện tính phí "
     "khi vượt 100.000 — **KHÔNG có mốc 30 ngày ân hạn** và không mô tả cơ chế chặn truy cập màn.",
     "Mốc 30 ngày quyết định khi nào khách bị khóa toàn bộ tính năng. Không có trong spec nghĩa là không ai "
     "đối chiếu được nếu code đổi. Cũng cần làm rõ 'ngày detect' lấy từ cột nào.",
     "Nhóm『Bill max friend — cảnh báo & upgrade』TC 8", "",
     ""],

    ["MT-10", "CAO", W,
     "Mốc expired_date + 7 ngày chặn trang phía LINE user của 5 tính năng khác",
     "Tab「Logic chung」(08/2025, 104 dòng) mô tả ma trận đầy đủ: với bot plan trả phí, "
     "`expired_date + 7d > now` thì LINE user mở được trang; `= now` hoặc `< now` thì KHÔNG mở được. "
     "Áp cho Lesson, Salon, Form, Item (màn mua / bill UnivaPay / bill Stripe / Cancel), Booking Event. "
     "Bot plan free thì mở được ở mọi mốc.",
     "`feature-spec.md` §8 'Phụ thuộc chéo' chỉ liệt kê Richmenu, Affiliate, Staff Management, Univapay Webhook — "
     "**KHÔNG nhắc việc hợp đồng hết hạn chặn trang LINE user của Lesson/Salon/Form/Item/Event**.",
     "Đây là ảnh hưởng ra NGƯỜI DÙNG CUỐI của 5 tính năng khác. Spec FA-031 không ghi, spec của 5 feature kia "
     "cũng chưa chắc ghi → vùng mù giữa các spec. Nếu code đổi mốc 7 ngày thì không đội nào phát hiện.",
     "Nhóm『Hợp đồng hết hạn ảnh hưởng tính năng』TC 1-5", "",
     ""],

    ["MT-11", "CAO", W,
     "Vào detail hợp đồng bằng URL + nhập thẻ lỗi + bấm back → XÓA HẲN hợp đồng",
     "「Quản lý hợp đồng」r321, r322: 「check khi vào detail bằng id bot contract / check khi nhập card false: "
     "4111 1111 1111 1111 => nhấn back về ==> **xóa luôn detail hợp đồng bot contract id đó**」— áp cho cả "
     "trạng thái chưa phát hành STK và đã phát hành STK.",
     "`feature-spec.md` không mô tả bất kỳ luồng nào xóa `bot_contracts` khi người dùng bấm back. "
     "§7 chỉ có DELETE trong Phase 5 của job (khi không còn bot_slot).",
     "Thao tác vô hại của người dùng (bấm back sau khi nhập nhầm thẻ) lại xóa dữ liệu hợp đồng. Nếu hợp đồng đó "
     "đã phát hành số tài khoản chuyển khoản thì khách có thể đã chuyển tiền vào tài khoản của một hợp đồng "
     "không còn tồn tại.",
     "Nhóm『Detail hợp đồng — standard/pro』TC 6", "",
     ""],

    ["MT-12", "CAO", W,
     "Hợp đồng lại bằng chuyển khoản, callback FAIL: có update lại status không?",
     "「Quản lý hợp đồng」r787 ghi expected 「trạng thái cancel hợp đồng, ngày hết hạn = ngày hết hạn cũ」 "
     "nhưng ngay trong cùng ô lại ghi chú của tester: 「**Check Logic từ trước đang không update lại status "
     "của hợp đồng**」— tức hiện trạng KHÁC expected.",
     "`feature-spec.md` không mô tả luồng 再契約 (hợp đồng lại). §6 danh sách 12 endpoint KHÔNG có "
     "`/basic/re-contract/{id}` dù corpus r825 xác nhận URL này tồn tại.",
     "Corpus tự ghi nhận hiện trạng không khớp expected nhưng không có ticket bug đi kèm. Nếu status không được "
     "update, hợp đồng có thể mắc kẹt ở trạng thái trung gian sau khi khách không chuyển tiền.",
     "Nhóm『Hợp đồng lại』TC 7", "",
     ""],

    ["MT-13", "CAO", W,
     "Callback UnivaPay đến MUỘN hoặc có 2 charge transfer song song: xử lý ra sao?",
     "「Improve bill tiền 12/2024」r483-r493 liệt kê 6 kịch bản: bill1 success/bill2 success; "
     "bill1 success/bill2 fail; bill1 fail/bill2 success; cả 2 fail; bill1 chưa callback/bill2 success; "
     "bill2 success rồi bill1 mới fail; và case 「status_payment=6, user nhấn hủy hợp đồng => nhưng sau đó có "
     "callback của univapay」. **Cột Expect Result của các dòng này để TRỐNG hoặc chỉ ghi 1 câu chung chung**.",
     "`feature-spec.md` §8 chỉ ghi 「Webhook `charge_finished` từ Univapay cập nhật trạng thái "
     "`bot_contracts.status_payment`」— KHÔNG mô tả xử lý callback trùng, callback muộn, hay thứ tự callback.",
     "Đây là nhóm race condition trên tiền thật. Corpus đã liệt kê đúng các tổ hợp nguy hiểm nhưng bỏ trống "
     "kết quả mong đợi → tester không có cách nào đánh giá PASS/FAIL. Kho hiện viết expected theo nguyên tắc "
     "idempotent, cần Dev xác nhận.",
     "Nhóm『Xác nhận plan — upgrade』TC 12, 13", "",
     ""],

    ["MT-14", "CAO", W,
     "Mua hợp đồng enterprise: mở form OEM hay mua trực tiếp trên tool?",
     "「Màn hình bill tiền」r383 (12/2025): 「4. Mua mới hợp đồng enterprise ==> **Mở link form của OEM** "
     "https://tayori.com/form/e7166cd66118f681415917e9c952befc3fcbaffa」.\n"
     "「Quản lý hợp đồng」r242 (Feature #37085, 06/2026, mới hơn 6 tháng): 「**Link mua hợp đồng enterprise**: "
     "/admin/confirm-contract-standard/enterprise/month」và r243-r244 test luồng mua trực tiếp trên tool.",
     "`feature-spec.md` không mô tả luồng mua enterprise. §2 SCR-BLP-05 có option plan おまとめ ở màn báo giá "
     "nhưng không nói mua ở đâu.",
     "TC mới (06/2026) thắng TC cũ theo quy tắc niên đại, nhưng cần xác nhận: link OEM còn dùng cho khách mới "
     "không, hay đã bỏ hẳn? Nếu cả 2 cùng tồn tại thì phải phân biệt điều kiện hiển thị.",
     "Nhóm『Màn chọn plan』TC 7; nhóm『Detail hợp đồng — enterprise』TC 7", "",
     ""],

    ["MT-15", "CAO", W,
     "Spec thiếu ít nhất 8 endpoint / màn thao tác hợp đồng",
     "「Quản lý hợp đồng」r820-r827 liệt kê 8 URL có thật cần kiểm middleware: `/basic/detail-contract/`, "
     "`/basic/change-bill-type/`, `/basic/change-payment-method/`, `/basic/detail/extend-contract/`, "
     "`/basic/detail-contract/{id}/cancel`, `/basic/re-contract/`, `/basic/change-card/`, "
     "`/basic/sub-card-setting/`. Corpus có TC đầy đủ cho cả 8 màn.",
     "`feature-spec.md:660` §6 chỉ liệt kê 12 endpoint, trong đó chỉ có `detail-contract` và "
     "`detail-contract/{id}/cancel`. §9 [M1] tự nhận thiếu 4 endpoint (đổi thẻ chính/phụ, coupon, đổi admin, "
     "POST hủy hợp đồng) và đề xuất grep source.",
     "Spec mô tả thiếu hơn nửa số màn thao tác của tính năng. Mọi phân tích ảnh hưởng dựa trên spec này đều "
     "sẽ bỏ sót. Corpus TCs chính là nguồn lấp được gap [M1] — nên dùng để bổ sung spec.",
     "Nhóm『Phân quyền & staff』TC 8", "",
     ""],

    ["MT-16", "CAO", W,
     "Công thức 日割り khi upgrade giữa kỳ",
     "「Quản lý hợp đồng」r843 (SpecImprove #33149, 21/10/2025): cột 備考 hiện "
     "「アップグレード 日割り（xxx日分）」với 「xxx: số ngày còn lại」, lưu ở `payment_histories.remain_day_upgrade`. "
     "「List main case」r32 xác nhận: 「check remain days khi upgrade ==> add thêm text 日分 phía sau số ngày remain」. "
     "**Không tab nào ghi công thức tính SỐ TIỀN**.",
     "`feature-spec.md:597` BR-04 chỉ nói phí lấy từ `users.basic_fee`, config `sns-line.plan_pro_fee` và "
     "`calculateSaleEnterprise()` — KHÔNG có công thức 日割り. Cột `remain_day_upgrade` cũng KHÔNG có trong "
     "Field Matrix §4 và db-mapping.",
     "Số tiền upgrade giữa kỳ là khoản khách bị trừ ngay lập tức. Không có công thức thì tester chỉ kiểm được "
     "'có hiện số ngày' chứ không kiểm được 'số tiền có đúng không'.",
     "Nhóm『Xác nhận plan — upgrade』TC 2", "",
     ""],

    ["MT-17", "CAO", W,
     "User chuyển khoản SAU khi hợp đồng đã bị hủy (quá expired_date + 8 ngày) thì tiền đi đâu?",
     "「Màn hình bill tiền」r482-r487 liệt kê 6 mốc chuyển khoản hợp lệ (trước hạn → +7 ngày) đều "
     "「Hợp đồng được gia hạn success」. r488 liệt kê mốc **+8 ngày** nhưng **cột Expect Result để TRỐNG**. "
     "r492 ghi mốc quá hạn 7 ngày → callback fail → status=3.",
     "`feature-spec.md` không mô tả xử lý khoản chuyển khoản đến sau khi hợp đồng bị hủy. "
     "§7 Phase 5 chỉ mô tả hủy hợp đồng, không nhắc hoàn tiền.",
     "Khách có thể chuyển tiền muộn 1-2 ngày (đặc biệt qua cuối tuần/ngày lễ — chính tooltip 入金待ち cũng "
     "cảnh báo điều này). Nếu hệ thống nhận tiền mà không kích hoạt lại hợp đồng và cũng không hoàn tiền thì "
     "là rủi ro khiếu nại tiền bạc.",
     "Nhóm『Job bill định kỳ — chuyển khoản』TC 3", "",
     ""],

    # ══════════════ Mức TRUNG BÌNH ══════════════
    ["MT-18", "TRUNG BÌNH", W,
     "8 cột DB corpus dùng nhưng db-mapping KHÔNG có",
     "Corpus dùng thường xuyên 8 cột để kiểm kết quả: `bill_type_old` (r483, r503), `payment_method_old` "
     "(r556, r577), `datetime_first_payment` (r595, tab Cố định ngày bill tiền), `release_date_transfer` (r603), "
     "`bank_branch_code` + `bank_account_holder_name` (r324-r349), `payment_histories.last_four_card` (r1292), "
     "`payment_histories.remain_day_upgrade` (r843).",
     "`feature-spec.md:387` ER Diagram và §4 Field Traceability Matrix (36 dòng) KHÔNG có cột nào trong 8 cột "
     "trên. `db/db-mapping.md` cũng không liệt kê. §10 tự đánh giá DB Mapping 9/10, thiếu `strip_bots` và "
     "`rich_menus` — nhưng chưa nhắc 8 cột này.",
     "Spec bỏ sót đúng những cột quyết định hành vi 'đăng ký đổi kỳ/phương thức nhưng chưa áp dụng' và "
     "'snapshot thẻ tại thời điểm thanh toán'. Người đọc spec sẽ không hiểu vì sao UI hiện kỳ cũ trong khi "
     "DB đã đổi.",
     "Nhóm『Đổi kỳ thanh toán』TC 1, 3; 『Đổi phương thức thanh toán』TC 3; "
     "『Chuyển khoản — tạo & thông tin tài khoản』TC 4; 『Lịch sử thao tác hợp đồng』TC 9", "",
     ""],

    ["MT-19", "TRUNG BÌNH", W,
     "Chế độ 月次決済一覧 và bộ lọc 絞り込み của màn hóa đơn không có trong spec",
     "Tab「Improve màn download quản lý hóa đơn」r131-r167 mô tả cả 1 chế độ hiển thị thứ hai "
     "「月次決済一覧」với Calendar From~To, checkbox 全期間, nút 絞り込み mở modal lọc theo 料金プラン / "
     "決済方法 / danh sách bot, kèm phân trang 10/20/50/100 và sort.",
     "`feature-spec.md:246` §2 SCR-BLP-03 chỉ mô tả 2 panel: panel trái 年間決済一覧 (12 tháng) và panel phải "
     "chi tiết tháng với 2 tab 一括発行/個別発行. **KHÔNG có chế độ 月次決済一覧, không có filter modal, "
     "không có 全期間**.",
     "Spec mô tả thiếu khoảng một nửa chức năng của màn hóa đơn. Đây là màn khách hàng dùng để lấy chứng từ "
     "kế toán — thiếu mô tả nghĩa là không ai kiểm được khi có thay đổi.",
     "Nhóm『Lịch sử thanh toán — theo tháng & lọc』(12 TC)", "",
     ""],

    ["MT-20", "TRUNG BÌNH", W,
     "3 lỗi hiển thị modal lịch sử đã ghi nhận nhưng không thấy ticket bug",
     "Tab「Check lịch sử hợp đồng」ghi 3 nhận xét của tester ngay trong cột ghi chú:\n"
     "- r10: 「Modal này c đang thấy **thiếu thông tin cột お支払い期間**」\n"
     "- r14: 「Upgrade plan từ free lên pro năm nhưng lại **có 1 lịch sử gia hạn hợp đồng**」\n"
     "- r34, r37: 「Recontract bill tháng và năm/card, **bị hiển thị thêm lịch sử thay đổi main card**」\n"
     "- r39, r40: 「**Không get được thông tin thời gian extend**」/「Không get được thông tin bot」",
     "`feature-spec.md:216` §2 liệt kê 8 loại sự kiện quan sát được trong production và ghi 「28 loại type」 "
     "ở Field Matrix #25 — không mô tả nội dung chi tiết từng modal nên không có gì để đối chiếu.",
     "Đây là các lỗi hiển thị lịch sử — khách dùng chính màn này để đối soát vì sao bị trừ tiền. "
     "Lịch sử thừa/thiếu làm sai lệch bằng chứng khi có khiếu nại.",
     "Nhóm『Lịch sử thao tác hợp đồng』TC 4; 『Môi trường & regression』TC 4", "",
     ""],

    ["MT-21", "TRUNG BÌNH", W,
     "Trùng mã type trong bot_life_cycles",
     "「Quản lý hợp đồng」r632 ghi 「xóa sub card / status:3 / **type:24**」nhưng r638 lại ghi "
     "「thêm staff / status:3 / **type:24**」. Tương tự r636 ghi 「đổi kỳ tháng→năm / **type:16**」 "
     "và r637 ghi 「change LOA / **type:16**」.",
     "`feature-spec.md:216` §2 bảng loại sự kiện chỉ liệt kê 8 type (7, 11, 12, 13, 15, 20, 23) và ghi "
     "「クーポンコードの適用 | (chưa xác định type)」. Không có type 16 hay 24 trong bảng.",
     "Hoặc corpus ghi nhầm, hoặc hệ thống thật sự dùng chung mã type cho 2 sự kiện khác nhau — trường hợp sau "
     "thì filter lịch sử theo loại sẽ trả về lẫn lộn. Cần Dev cung cấp bảng enum type đầy đủ (28 loại).",
     "Nhóm『Lịch sử thao tác hợp đồng』TC 5", "",
     ""],

    ["MT-22", "TRUNG BÌNH", W,
     "Vùng mù: 4 khu vực có trong spec nhưng corpus KHÔNG có TC nào",
     "Rà toàn bộ 30 tab của 2 file nguồn: KHÔNG có TC nào cho (a) màn 接続解除履歴 (SCR-BLP-04) ngoài 2 dòng "
     "điều hướng; (b) job `recover:RecoverUpdateInfoUnivapay` (5 phút/lần); "
     "(c) job `univapay:check_status_webhook` (01:00); (d) hiệu năng màn list hợp đồng.",
     "`feature-spec.md:295` §2 mô tả đầy đủ SCR-BLP-04 (3 cột, nguồn JSON snapshot, cảnh báo không khôi phục "
     "được). §7 mô tả đầy đủ 2 job trên.",
     "Đây là chiều ngược lại của mâu thuẫn: spec có, TCs không có. Kho hiện đã viết 6 TC dựa THUẦN TÚY trên "
     "spec (đánh dấu rõ ở Ghi chú) — cần Leader xác nhận trước khi giao member chạy.",
     "Nhóm『Lịch sử ngắt kết nối LOA』TC 2, 4; 『Job bill định kỳ — chuyển khoản』TC 7, 8; "
     "『Môi trường & regression』TC 6", "",
     ""],

    ["MT-23", "TRUNG BÌNH", W,
     "Coupon code: cả spec lẫn TCs đều bỏ trống",
     "Rà 30 tab: **KHÔNG có bất kỳ TC nào** về nút 「クーポンコードを入力する」hay sự kiện "
     "「クーポンコードの適用」. Tab「Coupon」thuộc file TCsLine_Admin (portal khác) chưa được đưa vào phạm vi.",
     "`feature-spec.md:775` §9 [M2] ghi rõ: UI có button 「クーポンコードを入力する」và log sự kiện "
     "「クーポンコードの適用」trong production, nhưng 「API Spec: Không tìm thấy endpoint xử lý coupon; "
     "DB: không tìm thấy cột `coupon_code` trong `bot_contracts` (52 cột), không tìm thấy bảng `coupons`」.",
     "Chức năng có trên UI production, có log sự kiện thật, nhưng không ai biết nó lưu ở đâu và cũng không ai "
     "test. Nếu coupon áp sai thì tiền thu của khách sai mà không có TC nào bắt được.",
     "KHÔNG có TC nào trong kho", "",
     ""],

    ["MT-24", "TRUNG BÌNH", W,
     "Mục お住まい: TC yêu cầu marker 必須 và nền trắng, thực tế KHÔNG có",
     "Tab「Feature #36994」(07/2026) là bộ TC do AI viết theo yêu cầu, cột Actual Result ghi kết quả THẬT:\n"
     "- TC-CARD-001 expect 「Có marker 必須」 → thực tế 「**Không có marker 必須** — vì lấy từ Univapay nên "
     "không can thiệp được vào」\n"
     "- TC-CARD-005/006 expect 「màu nền textbox #FFFFFF」 → thực tế 「**Màu nền mỗi textbox = #F9F9F9** — "
     "anh Tư báo: nó là input của form nằm trong form của univapay rồi」\n"
     "- TC-CARD-007 (hover nút) → kết quả **NG**",
     "`feature-spec.md` không mô tả widget nhập thẻ (thuộc UnivaPay). §9 [N1] ghi 「Modal thay đổi thẻ chính/phụ "
     "— nội dung chưa quan sát được」.",
     "3 TC được đánh dấu OK dù kết quả thực tế KHÁC expected (tester chấp nhận vì do widget bên thứ ba). "
     "Nếu giữ nguyên expected, lần test sau sẽ FAIL lại; nếu sửa expected thì mất yêu cầu gốc của CR.",
     "Nhóm『Nhập thẻ & 3D Secure』TC 2", "",
     ""],

    ["MT-25", "TRUNG BÌNH", W,
     "Bot chỉ có thẻ phụ (không có thẻ chính) thì job bill thế nào?",
     "「Màn hình bill tiền」Bug tự detect #38298 TC09: 「Bot chỉ có Sub Card / Bot không có Main Card → "
     "Bill bằng Sub Card bình thường (**nếu hệ thống hỗ trợ Sub Card là card thanh toán chính khi không có "
     "Main Card**)」— chính TC cũng đặt điều kiện nghi vấn.",
     "`feature-spec.md:722` §7 Phase 3 mô tả 「Charge thẻ Univapay Card → **Fallback**: SubcardBotContract → "
     "charge thẻ phụ」— tức thẻ phụ chỉ là fallback, không nói tới trường hợp không có thẻ chính.",
     "Tình huống này xảy ra được khi user xóa thẻ chính hoặc thẻ chính bị hệ thống gỡ. Nếu job không xử lý thì "
     "hợp đồng bị bill lỗi dù khách vẫn có thẻ hợp lệ.",
     "Nhóm『Job bill định kỳ — thẻ』TC 4", "",
     ""],

    ["MT-26", "TRUNG BÌNH", W,
     "Bot cũ đã có bill max friend: đổi thẻ chính có cập nhật thẻ bill max friend không?",
     "「Bill max friend」r213: 「Check các bot cũ trước đó đã có bill max friend / Bot bill tháng ==> "
     "**Recover card bill max friend sẽ cùng với card bill hợp đồng**」.\n"
     "NHƯNG r223 (cùng tab): 「Check với bot bill max friend cũ ==> Khi change maincard sẽ **KHÔNG update "
     "thông tin card ở bảng bot_card_bill_friend**」.",
     "`feature-spec.md:576` BR-02 và §7 HandleBillMaxFriend không mô tả quan hệ giữa thẻ của hợp đồng và thẻ "
     "của khoản max friend. Bảng `bot_card_bill_friend` trong ER Diagram có cột `payment_method` nhưng không "
     "có cột thẻ.",
     "Hai dòng trong cùng 1 tab nói ngược nhau. Nếu thẻ max friend không được cập nhật khi khách đổi thẻ thì "
     "kỳ bill max friend tiếp theo sẽ charge vào thẻ đã hủy.",
     "Nhóm『Bill max friend — thanh toán & job』TC 9", "",
     ""],

    ["MT-27", "TRUNG BÌNH", W,
     "2 job scan campaign/tutorial không có trong danh sách job của spec",
     "Tab「Campaign + Tutorial」r305-r326 (SpecImprove #33838, 13/03/2026) mô tả 2 job: "
     "`job:ScanHasCampaign` (scan hằng ngày, lúc 02:00 theo r145) và `job:ScanHasTutorial`, "
     "kèm bộ TC đầy đủ cho cả nhánh scan và nhánh recover. Ticket ghi 「Chuyển job scan campain + tutorial "
     "sang **java**」.",
     "`feature-spec.md:696` §7 khẳng định 「**Tất cả billing jobs của FA-031 là Laravel Artisan Console "
     "Commands**... **KHÔNG phải Spring Boot**」và liệt kê đúng 5 command, không có 2 job này.",
     "Nếu 2 job này đã chuyển sang Java (Spring Boot) thì phát biểu tuyệt đối của spec §7 sai, và ranh giới "
     "'job nào chạy ở đâu' bị nhòe — ảnh hưởng cách dựng môi trường test (RULE-08).",
     "Nhóm『Campaign 初月無料』TC 11, 12", "",
     ""],

    ["MT-28", "TRUNG BÌNH", W,
     "Refund hợp đồng năm: 2 màn hiển thị 2 con số khác nhau",
     "Tab「Logic refund」r33, r34: 「mh bill tiền phân bổ / bill theo tháng ==> refund số tiền = **số tiền đã "
     "nhập** (trường refund_amount)」; 「bill theo năm ==> refund số tiền = **số tiền đã phân bổ** (trường "
     "amount)... số tiền bill theo tháng ở mh top: khi có refund theo năm sẽ trừ số tiền đã phân bổ」.",
     "`feature-spec.md:614` BR-06 chỉ nêu điều kiện lọc `status_refund=0` và `parent_month=1`; "
     "không mô tả cách hiển thị số tiền refund trên các màn.",
     "Cùng 1 giao dịch refund nhưng màn bill tiền chung và màn phân bổ hiện 2 con số khác nhau. Người đối soát "
     "sẽ nghĩ là lệch dữ liệu. Cần chốt con số nào là chuẩn để đối soát kế toán.",
     "Nhóm『Hoàn tiền』TC 3", "",
     ""],

    ["MT-29", "TRUNG BÌNH", W,
     "Hóa đơn CŨ sau SpecChange #32268 dùng địa chỉ cũ hay địa chỉ mới?",
     "Tab「Logic chung」r95-r126 (SpecChange #32268, 04/10/2025 — 「Thay đổi địa chỉ trong file export hóa đơn "
     "và estimation」) có dòng r117 「Check hiển thị các hóa đơn cũ」nhưng **cột Expect Result chỉ ghi "
     "「Check địa chỉ mới」** cho khối chung, không tách riêng nhánh hóa đơn cũ.",
     "`feature-spec.md` không mô tả nội dung file 領収書 / 見積書 (chỉ nói tải PDF).",
     "Hóa đơn là chứng từ kế toán. Nếu in lại hóa đơn cũ bằng địa chỉ mới thì chứng từ không khớp thời điểm "
     "phát sinh; nếu giữ địa chỉ cũ thì phải có cơ chế lưu snapshot địa chỉ — cả 2 đều không được ghi ở đâu.",
     "Nhóm『Hợp đồng hết hạn ảnh hưởng tính năng』TC 7", "",
     ""],

    ["MT-30", "TRUNG BÌNH", W,
     "Giá plan trên tài liệu TC Estimation là giá năm 2023",
     "Tab「Estimation」r17, r18, r31, r32 (09/2023) ghi giá: standard tháng = **4.500**, standard năm = "
     "**48.600**, pro tháng = 33.000, pro năm = 356.400, EP standard tháng (10 slot) = 40.500.\n"
     "「Màn hình bill tiền」r38, r39 (12/2025) ghi giá PRODUCTION: standard tháng = **10.780**, "
     "năm 10%OFF = 9.702/tháng (tổng 116.424) — và ghi chú 「dev và stg là 4050/4500」.",
     "`feature-spec.md:597` BR-04: 「Không có bảng plans/pricing riêng — giá hardcode trong config và helper "
     "functions」, phí cơ bản lấy từ `users.basic_fee` của admin id=1.",
     "Giá 4.500 trong TC Estimation trùng đúng giá DEV/STAGING của năm 2025 → nhiều khả năng TC 2023 viết trên "
     "môi trường dev và đã lỗi thời. Nếu member chạy theo, báo giá gửi khách sẽ sai số tiền.",
     "Nhóm『Phát hành báo giá』TC 5, 6", "",
     ""],

    ["MT-31", "TRUNG BÌNH", W,
     "Khối『Check bill tiền bot』của job Monitor bill tiền chưa được đọc chi tiết",
     "Tab「Monitor bill tiền」(gid=1905032532, trùng nhau giữa TCsLine_Improve chung và TCsLine_JOB) có "
     "khối `Check bill tiền bot` r11-r65 — đối soát giao dịch hợp đồng BOT với UnivaPay/Stripe qua bảng "
     "`payment_history`. Khối này đã bị kho FA-026 (bill item) **loại khỏi phạm vi với lý do 'thuộc FA-031'**.",
     "`feature-spec.md` §7 KHÔNG có job monitor/đối soát nào trong 5 command được liệt kê.",
     "Kho FA-031 hiện chỉ viết 1 TC KHUNG cho job này vì chưa đọc chi tiết 55 dòng của khối. "
     "Cần bổ sung để không lặp lại tình trạng 'quả bóng bị đá qua đá lại giữa 2 kho'.",
     "Nhóm『Job bill định kỳ — chuyển khoản』TC 9", "",
     ""],

    ["MT-32", "TRUNG BÌNH", W,
     "Cột LOA接続日 khi hợp đồng chưa kết nối bot",
     "「List main case」r29: 「Check cột LOA接続日 / Logic ==> - Lấy theo ngày add bot - **Case không có bot "
     "thì hiển thị ngày thanh toán**」.",
     "`feature-spec.md:104` bảng cột SCR-BLP-01 và Field Matrix #10 chỉ ghi nguồn là "
     "`bot_contracts.date_add_loa` — KHÔNG có nhánh fallback sang ngày thanh toán.",
     "Slot đã mua nhưng chưa kết nối LOA là trạng thái phổ biến (chính là bối cảnh Bug KH #36303). "
     "Nếu hiển thị nhầm nguồn ngày thì khách hiểu sai ngày bắt đầu tính phí.",
     "Nhóm『Cột & trạng thái hợp đồng』TC 13", "",
     ""],

    ["MT-33", "TRUNG BÌNH", W,
     "Modal sắp xếp hợp đồng: những trạng thái nào được kéo thả?",
     "「List main case」r28: 「Check modal sắp xếp hợp đồng ==> - **Chỉ có hợp đồng có status != overdue, đang "
     "chờ ck, chờ phát hành, hủy thường, hủy cưỡng chế** trong modal - Khi sắp xếp > save không làm xáo trộn "
     "vị trí của các status cố định」— dùng cách diễn đạt phủ định chồng nhau, khó suy ra danh sách chính xác.",
     "`feature-spec.md:562` BR-01 mô tả 6 nhóm phân loại và thứ tự query "
     "`ORDER BY position DESC, date_cancel_contract DESC, id DESC`, nhưng KHÔNG nói nhóm nào được kéo thả.",
     "Nếu modal cho kéo thả một trạng thái vốn bị ghim, thứ tự sau khi save sẽ khác thứ tự hiển thị — "
     "user tưởng thao tác không có tác dụng.",
     "Nhóm『Sắp xếp, tìm kiếm & phân trang』TC 5", "",
     ""],

    # ══════════════ Mức THẤP ══════════════
    ["MT-34", "THẤP", W,
     "2 dòng TC filter checkbox ghi ngược kết quả",
     "「Quản lý hợp đồng」r11: 「Check khi bỏ tích check box / **契約中 Đang hđ** ==> Chỉ hiển thị **List hợp "
     "đồng đã hủy**」— đúng logic.\n"
     "r12: 「**解約済み Đã hủy hđ** ==> Chỉ hiển thị **List đang hợp đồng**」— cũng đúng logic nếu hiểu "
     "'bỏ tích', nhưng cách viết ở r11/r12 không thống nhất chủ ngữ (lúc là checkbox bị bỏ tích, lúc là "
     "kết quả), dễ đọc nhầm thành ngược.",
     "`feature-spec.md:94` §2 chỉ mô tả 「Bộ lọc: Checkbox 契約中 | Checkbox 解約済み | Textbox tìm kiếm」, "
     "không mô tả hành vi khi bỏ tích.",
     "Không ảnh hưởng hành vi hệ thống, nhưng câu chữ mập mờ khiến member dễ ghi nhận sai kết quả. "
     "Kho đã viết lại theo nghĩa đúng.",
     "Nhóm『Màn list hợp đồng — hiển thị & lọc』TC 6, 7", "",
     ""],

    ["MT-35", "THẤP", W,
     "Empty state màn list hợp đồng dùng text nào?",
     "「Quản lý hợp đồng」r13 (bỏ tích cả 2 checkbox) → 「Hiển thị ra màn **アカウントが接続されていません**」; "
     "r23 (search không ra kết quả) → cùng text đó; "
     "r16 → 「Check khi chưa có data nào ==> Hiển thị text **まだデータがありません**」nhưng dòng này nằm "
     "trong khối 接続解除履歴.",
     "`feature-spec.md` không mô tả empty state của SCR-BLP-01; SCR-BLP-04 có cảnh báo "
     "「接続解除したLINE公式アカウントの復元はできません。」nhưng không nêu text khi rỗng.",
     "Chỉ là text hiển thị, nhưng nếu 2 màn dùng nhầm text của nhau thì thông điệp gây hiểu lầm "
     "(chưa kết nối account ≠ chưa có dữ liệu lịch sử).",
     "Nhóm『Màn list hợp đồng — hiển thị & lọc』TC 8, 10; 『Lịch sử ngắt kết nối LOA』TC 3", "",
     ""],

    ["MT-36", "THẤP", W,
     "Chiều sort mặc định của cột ngày ở 2 màn",
     "Màn list hợp đồng: r1060-r1063 có nút sort ở cột 次回決済(更新)日 nhưng **không ghi chiều mặc định**.\n"
     "Màn hóa đơn: r64 ghi 「Sắp xếp default: **từ bé cũ nhất >> mới nhất**」nhưng r67/r100/r183 (cùng tab) "
     "lại ghi 「Default: **Hiển thị theo ngày tạo mới nhất**」.",
     "`feature-spec.md:262` §2 SCR-BLP-03 ghi request mặc định 「order[column]=created_at&order[dir]=**DESC**」 "
     "— tức mới nhất trước.",
     "Corpus tự mâu thuẫn trong cùng tab; spec có câu trả lời cho màn hóa đơn (DESC) nhưng không có cho màn "
     "list hợp đồng. Ảnh hưởng nhỏ nhưng làm member ghi kết quả không nhất quán.",
     "Nhóm『Sắp xếp, tìm kiếm & phân trang』TC 8; 『Lịch sử thanh toán — theo tháng & lọc』TC 12", "",
     ""],

    ["MT-37", "THẤP", W,
     "Nút 閉じる của modal filter hóa đơn: lần đầu và các lần sau hành vi khác nhau",
     "Tab「Improve màn download quản lý hóa đơn」r164: 「btn closed 閉じる / Khi có chọn các option ==> "
     "**Cài filter lần 1: Không lọc kqua từ filter đó, giữ nguyên màn hình; Cài lần n: hiển thị lần lọc "
     "hiện tại**」.",
     "`feature-spec.md` không mô tả modal filter (xem MT-19).",
     "Cùng 1 nút mà lần đầu và lần sau xử lý khác nhau là hành vi phản trực giác. Cần Leader xác nhận đây là "
     "chủ ý (giữ lại kết quả lọc trước) hay là lỗi trạng thái.",
     "Nhóm『Lịch sử thanh toán — theo tháng & lọc』TC 8", "",
     ""],

    ["MT-38", "THẤP", W,
     "Double-click nút tải hóa đơn: tải 2 lần có phải hành vi mong muốn?",
     "Tab hóa đơn r124: 「Btn download / **Double click** ==> **Download 2 hóa đơn** tương ứng với dòng được "
     "click」; r178: 「Btn download hàng loạt / double click ==> **Download 2 lần** các hóa đơn đã chọn」— "
     "tức corpus coi việc tải 2 lần là ĐÚNG.",
     "`feature-spec.md` không mô tả chống double submit ở màn nào.",
     "Với thao tác chỉ đọc (tải file) thì tải 2 lần không gây hại dữ liệu, nhưng khác hẳn nguyên tắc chống "
     "double-click ở các nút thanh toán. Cần chốt để TC nhất quán.",
     "Nhóm『Tải lãnh thụ thư』TC 14", "",
     ""],

    ["MT-39", "THẤP", W,
     "Format hiển thị calendar ở khu lịch sử thao tác hợp đồng",
     "「Quản lý hợp đồng」r174 (khối detail plan free): 「format ==> **2025/12/16（火） から 2026/01/14（水）**」 "
     "— có thứ trong tuần.\n"
     "r226, r230 (khối detail enterprise, cùng chức năng): 「Format ==> **yyyy.mm.dd**」— không có thứ, "
     "dùng dấu chấm.",
     "`feature-spec.md:225` §2 chỉ ghi 「Date picker 開始日 và 終了日」, không nêu format.",
     "Nếu 2 màn thật sự dùng 2 format khác nhau thì đó là lỗi nhất quán UI; nếu chỉ là TC ghi khác nhau thì "
     "cần thống nhất để member không ghi FAIL oan.",
     "Nhóm『Detail hợp đồng — plan free』TC 7", "",
     ""],

    ["MT-40", "THẤP", W,
     "1 kết quả NG chưa rõ trạng thái trong ma trận lịch sử",
     "Tab「Check lịch sử hợp đồng」r21: 「Mua mới slot trống: pro năm - bill transfer」có cột "
     "「Brach rls」= **NG** trong khi các cột khác = OK và các dòng lân cận đều OK. "
     "Không có ticket bug hay ghi chú kèm theo.",
     "Không liên quan spec.",
     "Một kết quả NG không có ticket là dấu hiệu bug bị bỏ quên khi release. Cần tra lại lịch sử hoặc "
     "chạy lại chính xác case này.",
     "Nhóm『Môi trường & regression』TC 3", "",
     ""],

    ["MT-41", "THẤP", W,
     "User đã có bot free: nút plan free bị disable hay báo lỗi?",
     "「Màn hình bill tiền」r17: 「user đã có bot free sau 1/7/2021 / chọn add bot free ==> Không được tạo free "
     "nữa **Disable btn ご利用中のプランです**」.\n"
     "r359 (cùng tab, khối logic bill tiền): 「user đã có 1 bot free -> nhấn add bot free ==> **Không cho phép "
     "add, báo lỗi 現在のプランは利用できない機能…**」.",
     "`feature-spec.md` không mô tả quy tắc giới hạn bot free theo mốc 01/07/2021.",
     "Disable nút và báo lỗi sau khi bấm là 2 trải nghiệm khác nhau. Nếu nút disable thì dòng r359 không thể "
     "xảy ra — một trong hai TC đã lỗi thời.",
     "Nhóm『Rule slot trống & bot free』TC 2", "",
     ""],

    ["MT-42", "THẤP", W,
     "Truy cập màn detail bằng URL khi hợp đồng chờ chuyển khoản: chặn tới mức nào?",
     "「Quản lý hợp đồng」r317, r318: 「check khi vào bằng domain, gán id bot contract ==> - vẫn có thể vào màn "
     "detail - disable không cho phép click - **chặn cả bên trong màn không cho phép nhập**」— "
     "không nói rõ 'chặn' là ở client hay server.",
     "`feature-spec.md:642` BR-07 mô tả `authenticationBotContract()` kiểm tra quyền theo hợp đồng "
     "(404 nếu không có quyền) nhưng không mô tả chặn theo TRẠNG THÁI hợp đồng.",
     "Nếu chỉ disable phía client thì bỏ thuộc tính `disabled` bằng DevTools là submit được — đây là lỗ hổng "
     "sửa hợp đồng đang chờ tiền. Kho đã thêm bước bypass DevTools vào TC, cần Leader xác nhận mức chặn "
     "server-side.",
     "Nhóm『Detail hợp đồng — standard/pro』TC 5", "",
     ""],

    ["MT-43", "THẤP", W,
     "Message lỗi thanh toán từng hiển thị tiếng Anh trên staging",
     "Tab「Bill tiền univapay: 3D secure」r14 ghi ở cột Note (staging): "
     "「**đang hiện msg lỗi tiếng anh**」cho case upgrade standard → pro bằng thẻ cũ, bill success.",
     "`feature-spec.md` không mô tả bộ message lỗi thanh toán.",
     "Message lỗi lọt tiếng Anh làm khách Nhật không hiểu và tăng ticket support. Ghi nhận từ 03/2025, "
     "không rõ đã fix chưa.",
     "Nhóm『Nhập thẻ & 3D Secure』TC 10", "",
     ""],
]
