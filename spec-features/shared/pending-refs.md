# Tham chiếu đang chờ (Pending References)

> Khi scan tính năng gặp shared component chưa scan → ghi vào đây.
> Khi shared component được scan xong → backfill tất cả features tham chiếu → xoá entry.

## Pending

| Shared Component | Mã SC | Features chờ cập nhật | Ưu tiên | Ghi chú |
|-----------------|------|--------------------|---------|---------|
| Template Message | SC-001 | FA-008, FA-009, FA-007, FA-001, FA-010, FA-012 | Cao | Dùng rất phổ biến — nên scan sớm. FA-012: dùng trong action settings khi gán tag. FA-001: xác nhận dùng trong toolbar「テンプレート送信」 |
| Tag Selector | SC-002 | FA-001, FA-012, FA-013, FA-008, FA-009 | Cao | Dùng trong lọc và phân nhóm. FA-001: xác nhận dùng trong tab「タグ管理クイック操作」. FA-013: xác nhận dùng trong filter「タグ」và tab「タグ」trên chi tiết bạn bè |
| Friend Filter/Segment | SC-003 | FA-002, FA-003, FA-008, FA-009, FA-013, FA-024 | Cao | Lọc đối tượng gửi tin. FA-002: xác nhận dùng biến thể trong modal「絞り込み設定」— bổ sung「表示設定」và「メッセージ確認状況」. FA-003: xác nhận dùng trong modal「絞り込み」với 11 filter types, AND/OR conditions. FA-013: xác nhận dùng trong modal「絞り込み」với 11 filter types (タグ, 友だち名, 友だち追加日, ステップ購読状況, QRコードアクション, コンバージョン, 確認状況, 友だち情報, 対応ステータス, アフィリエイター, 新規・既存 友だち), AND/OR logic, API post-advance-filter-v2 |
| Action Settings | SC-004 | FA-001, FA-003, FA-004, FA-007, FA-008, FA-009, FA-010, FA-011, FA-012, FA-013, FA-015, FA-016, FA-017 | Cao | Cấu hình hành động tự động. FA-012: xác nhận dùng trong edit tag. FA-001: xác nhận dùng trong toolbar「アクション」. FA-003: xác nhận dùng trong modal「アクション」với 10 action types (ステップ, テンプレート, テキスト, リマインド, タグ, リッチメニュー, ブックマーク, 友だち情報, 対応ステータス, ブロック). FA-010: xác nhận dùng trong Panel/Button editor — nút「アクション登録・編集」cho button action + overflow action (tab 詳細設定). FA-013: có thể dùng trong「友だち一括アクション」→「アクション選択」(cần xác nhận). FA-015: xác nhận dùng trong dialog「アクション」cho 選択肢/年月日/ポイント — cùng 10 action types |
| Rich Text / Message Editor | SC-005 | FA-008, FA-009, FA-007, FA-010, FA-001 | Cao | Soạn thảo nội dung tin nhắn. FA-001: xác nhận dùng trong toolbar「メディア送信」+ khung nhập tin nhắn. FA-010: xác nhận dùng trong editor テキスト — tools「情報自動挿入」「PDFアップロード」「絵文字」+ checkbox URL gốc |
| Delivery Target Selector | SC-006 | FA-008, FA-009, FA-022 | Trung bình | Chọn đối tượng nhận tin |
| Schedule/Timer Settings | SC-007 | FA-001, FA-008, FA-009, FA-016, FA-022 | Trung bình | Cài đặt thời gian gửi. FA-001: xác nhận dùng trong toolbar「送信予約」 |

_Danh sách trên được suy luận từ phân tích menu — sẽ được xác nhận và cập nhật khi chạy `/spec` cho từng tính năng._
_FA-012 (Quản lý thẻ) đã xác nhận sử dụng: SC-001 (Template Message trong action), SC-002 (Tag Selector trong action), SC-004 (Action Settings editor)._
_FA-001 (Chat 1:1) đã xác nhận sử dụng: SC-001 (Template Message qua toolbar), SC-002 (Tag Selector qua tab 3), SC-004 (Action Settings qua toolbar), SC-005 (Message Editor qua toolbar + input), SC-007 (Schedule qua toolbar「送信予約」)._
_FA-002 (Quản lý chat) đã xác nhận sử dụng: SC-003 (Friend Filter/Segment biến thể trong modal「絞り込み設定」)._
_FA-003 (Tự động trả lời) đã xác nhận sử dụng: SC-003 (Friend Filter/Segment trong modal「絞り込み」— 11 filter types, AND/OR logic), SC-004 (Action Settings trong modal「アクション」— 10 action types)._
_FA-013 (Danh sách bạn bè) đã xác nhận sử dụng: SC-002 (Tag Selector trong filter + tab chi tiết), SC-003 (Friend Filter/Segment trong modal「絞り込み」— 11 filter types, AND/OR logic, API post-advance-filter-v2), SC-004 (Action Settings trong「友だち一括アクション」— cần xác nhận chi tiết)._
_FA-004 (Rich Menu) đã xác nhận sử dụng: SC-004 (Action Settings trong tab「友だちアクション」trên Step 3 — タップ時アクション). SC-003 (Friend Filter/Segment) suy luận dùng trong SCR-RCM-07「個別に選択する」— cần xác nhận._
_FA-010 (Mẫu tin nhắn) đã xác nhận sử dụng: SC-004 (Action Settings trong Panel/Button editor — button action + overflow action), SC-005 (Message Editor trong tab テキスト — 情報自動挿入, PDFアップロード, 絵文字). FA-010 chính là trang quản lý SC-001 (Template Message) — các tính năng khác tham chiếu template từ đây._

## Đã backfill (lịch sử)

| Shared Component | Mã SC | Ngày scan | Features đã cập nhật |
|-----------------|------|----------|---------------------|
