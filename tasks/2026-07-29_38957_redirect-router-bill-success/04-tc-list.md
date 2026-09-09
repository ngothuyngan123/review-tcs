<!-- sync-target: https://docs.google.com/spreadsheets/d/1p1tI1UUR3f9AEHKEqPZ6YpfInFEa-Us1a7x4oLvRoRk/edit?gid=412698763#gid=412698763 -->
<!-- sync-tcs: url=https://docs.google.com/spreadsheets/d/1p1tI1UUR3f9AEHKEqPZ6YpfInFEa-Us1a7x4oLvRoRk/edit?gid=412698763#gid=412698763 | sheet=Màn hình bill tiền | anchor=Main Function -->

# 04 — TC List (HUMAN — fetch read-only từ master sheet)

> **Nguồn:** Google Sheet `TCsLine_Bill tiền_Improve2025` › tab **"Màn hình bill tiền"** (gid `412698763`), **rows 257–315** = **59 TC**.
> Fetch 2026-07-29 qua service account (`credentials/google-service-account.json`) — MCP google-sheets offline trong session này.
> Cột đánh dấu trong sheet **"Bug tự detect #38957"**: cả 59 case đều **OK**.
> ⚠️ **TC do người viết (read-only).** KHÔNG sửa title/expected. Format = **native master** (Main Function → Sub1 → Sub2), KHÔNG phải 16-col canonical (không có TC No. / Mã quan điểm / Loại case trong sheet gốc — không bịa thêm).
> Ô **Main Function** và **Sub1** là merged-cell trong sheet → đã **fill-down** để mỗi dòng tự đọc được. Ô **Expect Result** giữ verbatim (một số dòng thuộc case "không bill" để trống — kỳ vọng nằm ở dòng đầu group).

## Bảng TC (giữ nguyên cell từ sheet)

| Sheet row | Main Function | Sub1 | Sub2 (+ Sub3–5) | Kết quả mong đợi (Expect Result) | KQ #38957 |
|---|---|---|---|---|---|
| 257 | Check redirect khi mua mới hợp đồng | bot free |  | không redirect | OK |
| 258 | Check redirect khi mua mới hợp đồng | bot standard month | Bill card | Khi bill tiền success thì redirect sang url:<br>https://step.lme.jp/monthly/standard_success<br>Sau 3s redirect về màn step 完了 | OK |
| 259 | Check redirect khi mua mới hợp đồng | bot standard year | Bill card | Khi bill tiền thì redirect sang url:<br>https://step.lme.jp/yearly/standard_success<br><br>Sau 3s redirect về màn step 完了 | OK |
| 260 | Check redirect khi mua mới hợp đồng | Bot pro month | Bill card | Khi bill tiền  thì redirect sang url:<br>https://step.lme.jp/monthly/pro_success<br>Sau 3s redirect về màn step 完了 | OK |
| 261 | Check redirect khi mua mới hợp đồng | Bot pro year | Bill card | Khi bill tiền  thì redirect sang url:<br>https://step.lme.jp/yearly/pro_success<br>Sau 3s redirect về màn step 完了 | OK |
| 262 | Check redirect khi upgrade hợp đồng | Upgrade plan ở màn list bot (Khi user không có slot trống thì sẽ hiện nút upgrade) | Free -> standard month | Khi bill tiền success thì redirect sang url:<br>https://step.lme.jp/monthly/standard_success<br>Sau 3s redirect về màn step 完了 | OK |
| 263 | Check redirect khi upgrade hợp đồng | Upgrade plan ở màn list bot (Khi user không có slot trống thì sẽ hiện nút upgrade) | Free -> standard year | Khi bill tiền thì redirect sang url:<br>https://step.lme.jp/yearly/standard_success<br><br>Sau 3s redirect về màn step 完了 | OK |
| 264 | Check redirect khi upgrade hợp đồng | Upgrade plan ở màn list bot (Khi user không có slot trống thì sẽ hiện nút upgrade) | Free -> Pro month | Khi bill tiền  thì redirect sang url:<br>https://step.lme.jp/monthly/pro_success<br>Sau 3s redirect về màn step 完了 | OK |
| 265 | Check redirect khi upgrade hợp đồng | Upgrade plan ở màn list bot (Khi user không có slot trống thì sẽ hiện nút upgrade) | Free -> Pro year | Khi bill tiền  thì redirect sang url:<br>https://step.lme.jp/yearly/pro_success<br>Sau 3s redirect về màn step 完了 | OK |
| 266 | Check redirect khi upgrade hợp đồng | Upgrade plan ở màn list bot (Khi user không có slot trống thì sẽ hiện nút upgrade) | Upgrade standard month -> pro month | Khi bill tiền  thì redirect sang url:<br>https://step.lme.jp/monthly/pro_success<br>Sau 3s redirect về màn step 完了 | OK |
| 267 | Check redirect khi upgrade hợp đồng | Upgrade plan ở màn list bot (Khi user không có slot trống thì sẽ hiện nút upgrade) | Upgrade standard year -> pro year | Khi bill tiền  thì redirect sang url:<br>https://step.lme.jp/yearly/pro_success<br>Sau 3s redirect về màn step 完了 | OK |
| 268 | Check redirect khi upgrade hợp đồng | Upgrade plan ở màn list bot (Khi user không có slot trống thì sẽ hiện nút upgrade) | Upgrade standard year -> pro year có change phương thức bill từ transfer sang card | Khi bill tiền  thì redirect sang url:<br>https://step.lme.jp/yearly/pro_success<br>Sau 3s redirect về màn step 完了 | OK |
| 269 | Check redirect khi upgrade hợp đồng | Bot Free nhấn nút upgrade plan ở header (TH bot free và không được campaign) | Free -> standard month | Khi bill tiền success thì redirect sang url:<br>https://step.lme.jp/monthly/standard_success<br>Sau 3s redirect về màn step 完了 | OK |
| 270 | Check redirect khi upgrade hợp đồng | Bot Free nhấn nút upgrade plan ở header (TH bot free và không được campaign) | Free -> standard year | Khi bill tiền thì redirect sang url:<br>https://step.lme.jp/yearly/standard_success<br><br>Sau 3s redirect về màn step 完了 | OK |
| 271 | Check redirect khi upgrade hợp đồng | Bot Free nhấn nút upgrade plan ở header (TH bot free và không được campaign) | Free -> Pro month | Khi bill tiền  thì redirect sang url:<br>https://step.lme.jp/monthly/pro_success<br>Sau 3s redirect về màn step 完了 | OK |
| 272 | Check redirect khi upgrade hợp đồng | Bot Free nhấn nút upgrade plan ở header (TH bot free và không được campaign) | Free -> Pro year | Khi bill tiền  thì redirect sang url:<br>https://step.lme.jp/yearly/pro_success<br>Sau 3s redirect về màn step 完了 | OK |
| 273 | Check redirect khi Bill lại hợp đồng overdue card | Nhấn nút change card ở banner cảnh báo | bot standard month | Khi bill tiền success thì redirect sang url:<br>https://step.lme.jp/monthly/standard_success<br>Sau 3s redirect về màn step 完了 | OK |
| 274 | Check redirect khi Bill lại hợp đồng overdue card | Nhấn nút change card ở banner cảnh báo | bot standard year | Khi bill tiền thì redirect sang url:<br>https://step.lme.jp/yearly/standard_success<br><br>Sau 3s redirect về màn step 完了 | OK |
| 275 | Check redirect khi Bill lại hợp đồng overdue card | Nhấn nút change card ở banner cảnh báo | Bot pro month | Khi bill tiền  thì redirect sang url:<br>https://step.lme.jp/monthly/pro_success<br>Sau 3s redirect về màn step 完了 | OK |
| 276 | Check redirect khi Bill lại hợp đồng overdue card | Nhấn nút change card ở banner cảnh báo | Bot pro year | Khi bill tiền  thì redirect sang url:<br>https://step.lme.jp/yearly/pro_success<br>Sau 3s redirect về màn step 完了 | OK |
| 277 | Check redirect khi Bill lại hợp đồng overdue card | Nhấn change maincard | bot standard month | Khi bill tiền success thì redirect sang url:<br>https://step.lme.jp/monthly/standard_success<br>Sau 3s redirect về màn step 完了 | OK |
| 278 | Check redirect khi Bill lại hợp đồng overdue card | Nhấn change maincard | bot standard year | Khi bill tiền thì redirect sang url:<br>https://step.lme.jp/yearly/standard_success<br><br>Sau 3s redirect về màn step 完了 | OK |
| 279 | Check redirect khi Bill lại hợp đồng overdue card | Nhấn change maincard | Bot pro month | Khi bill tiền  thì redirect sang url:<br>https://step.lme.jp/monthly/pro_success<br>Sau 3s redirect về màn step 完了 | OK |
| 280 | Check redirect khi Bill lại hợp đồng overdue card | Nhấn change maincard | Bot pro year | Khi bill tiền  thì redirect sang url:<br>https://step.lme.jp/yearly//pro_success<br>Sau 3s redirect về màn step 完了 | OK |
| 281 | Check redirect khi Bill lại hợp đồng overdue card | Add sub card mới | bot standard month | Khi bill tiền success thì redirect sang url:<br>https://step.lme.jp/monthly/standard_success<br>Sau 3s redirect về màn step 完了 | OK |
| 282 | Check redirect khi Bill lại hợp đồng overdue card | Add sub card mới | bot standard year | Khi bill tiền thì redirect sang url:<br>https://step.lme.jp/yearly/standard_success<br><br>Sau 3s redirect về màn step 完了 | OK |
| 283 | Check redirect khi Bill lại hợp đồng overdue card | Add sub card mới | Bot pro month | Khi bill tiền  thì redirect sang url:<br>https://step.lme.jp/monthly/pro_success<br>Sau 3s redirect về màn step 完了 | OK |
| 284 | Check redirect khi Bill lại hợp đồng overdue card | Add sub card mới | Bot pro year | Khi bill tiền  thì redirect sang url:<br>https://step.lme.jp/yearly/pro_success<br>Sau 3s redirect về màn step 完了 | OK |
| 285 | Check redirect khi Bill lại hợp đồng overdue card | Change Sub card | bot standard month | Khi bill tiền success thì redirect sang url:<br>https://step.lme.jp/monthly/standard_success<br>Sau 3s redirect về màn step 完了 | OK |
| 286 | Check redirect khi Bill lại hợp đồng overdue card | Change Sub card | bot standard year | Khi bill tiền thì redirect sang url:<br>https://step.lme.jp/yearly/standard_success<br><br>Sau 3s redirect về màn step 完了 | OK |
| 287 | Check redirect khi Bill lại hợp đồng overdue card | Change Sub card | Bot pro month | Khi bill tiền  thì redirect sang url:<br>https://step.lme.jp/monthly/pro_success<br>Sau 3s redirect về màn step 完了 | OK |
| 288 | Check redirect khi Bill lại hợp đồng overdue card | Change Sub card | Bot pro year | Khi bill tiền  thì redirect sang url:<br>https://step.lme.jp/yearly/pro_success<br>Sau 3s redirect về màn step 完了 | OK |
| 289 | Check redirect khi Bill lại hợp đồng overdue transfer | Change type bill từ năm sang tháng => có nhập card mới bill success | bot standard year | Sau khi change sẽ bill hợp đồng standard month <br>=> redirect sang url https://step.lme.jp/monthly/standard_success<br>Sau 3s redirect về màn step 完了 | OK |
| 290 | Check redirect khi Bill lại hợp đồng overdue transfer | Change type bill từ năm sang tháng => có nhập card mới bill success | Bot pro year | Sau khi change sẽ bill hợp đồng promonth <br>=> redirect sang url https://step.lme.jp/monthly/pro_success<br>Sau 3s redirect về màn step 完了 | OK |
| 291 | Check redirect khi Bill lại hợp đồng overdue transfer | Change phương thúc bill từ transfer sang card có nhập card mới bill success | bot standard year | Sau khi change sẽ bill hợp đồng standard year<br>=> redirect sang url https://step.lme.jp/yearly/standard_success<br>Sau 3s redirect về màn step 完了 | OK |
| 292 | Check redirect khi Bill lại hợp đồng overdue transfer | Change phương thúc bill từ transfer sang card có nhập card mới bill success | Bot pro year | Sau khi change sẽ bill hợp đồng pro year<br>=> redirect sang url https://step.lme.jp/yearly/pro_success<br>Sau 3s redirect về màn step 完了 | OK |
| 293 | Check redirect khi Bill lại hợp đồng đã hủy | bot standard month |  | Khi bill tiền success thì redirect sang url:<br>https://step.lme.jp/monthly/standard_success<br>Sau 3s redirect về màn step 完了 | OK |
| 294 | Check redirect khi Bill lại hợp đồng đã hủy | bot standard year |  | Khi bill tiền thì redirect sang url:<br>https://step.lme.jp/yearly/standard_success<br><br>Sau 3s redirect về màn step 完了 | OK |
| 295 | Check redirect khi Bill lại hợp đồng đã hủy | Bot pro month |  | Khi bill tiền  thì redirect sang url:<br>https://step.lme.jp/monthly/pro_success<br>Sau 3s redirect về màn step 完了 | OK |
| 296 | Check redirect khi Bill lại hợp đồng đã hủy | Bot pro year |  | Khi bill tiền  thì redirect sang url:<br>https://step.lme.jp/yearly/pro_success<br>Sau 3s redirect về màn step 完了 | OK |
| 297 | Check redirect khi extend hợp đồng | bot standard month |  | Khi bill tiền success thì redirect sang url:<br>https://step.lme.jp/monthly/standard_success<br>Sau 3s redirect về màn step 完了 | OK |
| 298 | Check redirect khi extend hợp đồng | bot standard year |  | Khi bill tiền thì redirect sang url:<br>https://step.lme.jp/yearly/standard_success<br><br>Sau 3s redirect về màn step 完了 | OK |
| 299 | Check redirect khi extend hợp đồng | Bot pro month |  | Khi bill tiền  thì redirect sang url:<br>https://step.lme.jp/monthly/pro_success<br>Sau 3s redirect về màn step 完了 | OK |
| 300 | Check redirect khi extend hợp đồng | Bot pro year |  | Khi bill tiền  thì redirect sang url:<br>https://step.lme.jp/yearly/pro_success<br>Sau 3s redirect về màn step 完了 | OK |
| 301 | Check redirect khi thanh toán thẻ thanh công campaign | bot standard month |  | Khi bill tiền success thì redirect sang url:<br>https://step.lme.jp/monthly/standard_success<br>Sau 3s redirect về màn step 完了 | OK |
| 302 | Check redirect khi thanh toán thẻ thanh công campaign | bot standard year |  | Khi bill tiền thì redirect sang url:<br>https://step.lme.jp/yearly/standard_success<br><br>Sau 3s redirect về màn step 完了 | OK |
| 303 | Check redirect khi thanh toán thẻ thanh công campaign | Bot pro month |  | Khi bill tiền  thì redirect sang url:<br>https://step.lme.jp/monthly/pro_success<br>Sau 3s redirect về màn step 完了 | OK |
| 304 | Check redirect khi thanh toán thẻ thanh công campaign | Bot pro year |  | Khi bill tiền  thì redirect sang url:<br>https://step.lme.jp/yearly/pro_success<br>Sau 3s redirect về màn step 完了 | OK |
| 305 | Check các case không bill tiền => Không redirect router bill-success | Các case bill transfer | mua mới hợp đồng | Không redirect sang router bill success<br>mà sẽ redirect luôn sang màn 完了 | OK |
| 306 | Check các case không bill tiền => Không redirect router bill-success | Các case bill transfer | change phương thúc bill từ card sang transfer |  | OK |
| 307 | Check các case không bill tiền => Không redirect router bill-success | Các case bill transfer | hợp đồng lại |  | OK |
| 308 | Check các case không bill tiền => Không redirect router bill-success | Các case bill transfer | extend hợp đồng |  | OK |
| 309 | Check các case không bill tiền => Không redirect router bill-success | Các case bill transfer | thanh toán campaign chọn bill transfer |  | OK |
| 310 | Check các case không bill tiền => Không redirect router bill-success | Các case bill transfer | upgrade bot free chọn bill transfer |  | OK |
| 311 | Check các case không bill tiền => Không redirect router bill-success | Các case bill transfer | upgrade bot standard -> pro chọn bill transfer |  | OK |
| 312 | Check các case không bill tiền => Không redirect router bill-success | Các case thay đổi card nhưng hợp đồng còn hạn => không bill tiền | change main card |  | OK |
| 313 | Check các case không bill tiền => Không redirect router bill-success | Các case thay đổi card nhưng hợp đồng còn hạn => không bill tiền | change subcard |  | OK |
| 314 | Check các case không bill tiền => Không redirect router bill-success | Các case thay đổi card nhưng hợp đồng còn hạn => không bill tiền | change type bill từ năm (bill transfer) sang bill tháng (card) |  | OK |
| 315 | Check các case không bill tiền => Không redirect router bill-success | Các case thay đổi card nhưng hợp đồng còn hạn => không bill tiền | change phương thúc bill transfer sang card |  | OK |

<!-- Source: fetch từ Google Sheet 1p1tI1UUR3f9AEHKEqPZ6YpfInFEa-Us1a7x4oLvRoRk tab "Màn hình bill tiền" (gid 412698763) range A257:AF315, 2026-07-29. TC read-only — KHÔNG sửa nếu chưa confirm với Leader. -->
