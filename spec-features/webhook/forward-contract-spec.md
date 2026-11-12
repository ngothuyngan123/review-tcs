# FA-047 — Webhook転送: Hợp đồng chuyển tiếp ra ngoài — Contract Spec

> **Loại spec**: **Contract-first** (hợp đồng nhà cung cấp phát cho bên tích hợp nhận dữ liệu), **BỔ SUNG** cho [feature-spec.md](../admin/webhook-relay/feature-spec.md) code-first (1413 dòng, reverse-engineer từ web #40044 + job #40475).
> **Nguồn**: "Chuyển tiếp dữ liệu từ LME sang hệ thống bên ngoài — Webhook転送" — **bản 1.0.0 / 16-09-2026 19:35 JST**, WSSJ, Phase 1. Bản HTML gốc: [docs/webhook_v1_1104.html](docs/webhook_v1_1104.html).
> **Thêm vào spec-features**: 2026-11-04 (human dán trực tiếp).
> **Góc nhìn**: dữ liệu LME **gửi ra** + yêu cầu với endpoint **bên nhận**. feature-spec.md mô tả **cơ chế bên trong LME** (web config + job gửi). Dùng kèm nhau.

---

## 0. ⚠️ Đối chiếu với feature-spec.md code-first (flag cho Leader)

Doc hợp đồng này (16/09, **sau** mốc chốt "Phương án A" 10/09) ở nhiều điểm **khớp hành vi job thật** và ở điểm chữ ký còn **đúng hơn** wording UI/web cũ. Bảng dưới để Leader chốt expected khi review TC — **không tự chọn bên** ngoài phần đã ✅ khớp code.

| # | Hạng mục | Doc hợp đồng (file này) | feature-spec.md (code-first) | Kết luận |
|---|---|---|---|---|
| 1 | **`X-Lme-Signature`** | "Giá trị **secret thô** `whsec_…`, **so sánh chuỗi là đủ**" | Job gửi **secret thô** `whsec_…` ("Phương án A" chốt 2026-09-10). UI/hợp đồng web cũ ghi `hex(HMAC-SHA256(body))` → **SAI** (V-02) | ✅ **Doc này ĐÚNG, khớp job**. Expected TC: verify = so sánh chuỗi, **KHÔNG** HMAC |
| 2 | Retry | Tối đa **3 lần** (1 đầu + 2 lại), cách **1 phút**, **chỉ** khi timeout/5xx | `MAX_ATTEMPT=3`, `RETRY_DELAY_MINUTES=1`, `TIMEOUT_SECONDS=10`; lỗi khác ghi **ngay sau lần 1** (BR-31, BR-47) | ✅ Khớp |
| 3 | Batch `events[]` (kênh LME) | Tối đa **1.000** phần tử/request | `MAX_EVENTS_PER_REQUEST=1000` **nhưng thực tế ≤500** (BR-45) | ⚠️ Doc ghi 1000; code cắt thực tế ≤500 — TC boundary dùng số nào phải hỏi Leader |
| 4 | Lỗi timeout → mã hiển thị | timeout = "—, 408, 504" → 「タイムアウト（10秒）」 | Job ghi **NULL** (UI 「—」) cho timeout; "hợp đồng web 408" là wording lệch (V-11, V-13) | ⚠️ Chuỗi 「タイムアウト（10秒）」 cho 408/504 gây nhầm (doc tự thừa nhận) |
| 5 | Tái tạo secret | Admin: cũ hết hiệu lực ngay; **nhưng job còn gửi secret CŨ tới ~1 phút** (chu kỳ config). Khuyến nghị bên nhận **chấp nhận cả cũ+mới trong ~2 phút** | Job: cache config **60s** → gửi secret cũ ≤60s; nếu bên nhận trả 401 → `UNAUTHORIZED` **không retry** → mất lô (§7.9) | ✅ Khớp; doc nêu đúng rủi ro + cách né |
| 6 | **Flag bật trên production** | Doc không đề cập | Job có flag riêng `ENABLE_FORWARD_WEBHOOK_CALLBACK` / `_LME` **mặc định = 0 (TẮT)**; bật ≤60s đầu event bị **bỏ qua vĩnh viễn** (G-01, R-06, V-12) | ⚠️ **TC phải xác nhận flag đã bật**; UI hiện 「転送中」 vẫn có thể không gửi gì |
| 7 | **Lỗ hổng bảo mật** | Doc không đề cập | (a) webhook LINE **không kiểm `X-Line-Signature`** → event giả vẫn forward nguyên văn; (b) job **không chống SSRF** + OkHttp **follow redirect mang theo secret** (#2, #3, V-04) | ⚠️ TC bảo mật cần cover; "chưa nên bật trên production" |
| 8 | Built-in field ID | Liệt kê -1,-2,-3,-4,-6,-7,-8,-9,-10 (thiếu -5) | Khớp (feature-spec.md §3.8.x) | ✅ Khớp |

➡️ Tham chiếu chéo thêm: memory [[forward-webhook-unhandled-event-rule]] (kênh LINE forward cả event LME không xử lý: accountLink status 9…).

---

## 1. Tổng quan — 2 kênh độc lập

Bên nhận có thể dùng 1 hoặc cả 2 kênh với 2 URL khác nhau; bật kênh này không ảnh hưởng kênh kia.

| Kênh | Nội dung gửi | Thời điểm | Xác thực |
|---|---|---|---|
| **LINE公式アカウントデータ転送** | **Nguyên trạng** event LINE Platform gửi tới LME (message, follow, unfollow, postback…) | Ngay sau khi LME tiếp nhận (vài giây) | **Không chữ ký** |
| **L Messageデータ転送** | Thao tác tag / friend info phát sinh trong LME, đóng gói `events[]` | Ngay sau khi thao tác hoàn tất | Header `X-Lme-Signature` |

**Phạm vi Phase 1**: Kênh LINE = **toàn bộ event** LINE gửi tới (không lọc, không phụ thuộc LME xử lý được hay không). Kênh LME = **đúng 2 loại**: `tag` và `friend_info`. Event nội bộ khác (form, scenario…) **ngoài** Phase 1.

**Lưu ý vận hành**:
- Bật kênh **chỉ** chuyển tiếp event phát sinh **từ lúc bật trở đi** — không gửi lại dữ liệu lịch sử (muốn lịch sử → lấy qua API riêng).
- **Thay đổi cấu hình có độ trễ tới ~1 phút** (LME đọc config theo chu kỳ 1 phút). Sau khi 「保存する」, chưa hiệu lực ngay:
  - Vừa **bật kênh**: event trong khoảng chờ có thể **không được chuyển tiếp** và **không** vào danh sách lỗi (hệ thống coi kênh vẫn tắt). → Bật trước, chờ ~1 phút rồi mới thao tác thử.
  - Vừa **tắt / đổi URL**: đích cũ còn có thể nhận request trong khoảng chờ → chỉ đóng endpoint cũ sau ~1 phút.
  - Vừa **tái tạo secret**: xem §5.

## 2. Quy định chung (cả 2 kênh trừ khi ghi khác)

| Hạng mục | Quy định |
|---|---|
| Method | `POST` tới URL đích cấu hình ở màn 「Webhook転送」 |
| Content-Type | `application/json; charset=utf-8` |
| Thành công | **HTTP 2xx** (LME **không đọc** body response) |
| Timeout | **10 giây** (cả kết nối lẫn chờ phản hồi); quá = thất bại |
| Gửi lại | **Tối đa 3 lần, cách nhau 1 phút**. **Chỉ** gửi lại khi **timeout (kể cả 408, 504) hoặc HTTP 5xx**. Lần 1 ngay, 2 lần sau cách 1 phút (vòng đời ~2 phút). Lỗi khác → ghi lỗi ngay. Chỉ khi **cả 3 lần thất bại** mới ghi **1 bản ghi lỗi**. 1 sự cố = 1 dòng lỗi |
| Thứ tự event | **Không đảm bảo** (LME ưu tiên tốc độ, không xếp hàng theo friend) — bên nhận tự xử lý |
| Gửi trùng | **Có thể xảy ra** (request tới nơi nhưng phản hồi mất → vẫn tính thất bại + gửi lại). Mọi lần gửi lại mang **cùng `X-Lme-Delivery-Id`** → bên nhận dùng để dedupe |

## 3. Kênh LINE公式アカウントデータ転送

- **Nội dung**: nguyên văn request body LINE Platform gửi tới LME, giữ nguyên không thêm bớt.
- **Event media**: ảnh/video/audio **có** forward nhưng payload chỉ chứa **ID nội dung**, không chứa file → bên nhận tự gọi LINE Content API bằng token của chính mình.
- **Tài khoản hết hạn**: LINE OA đã xoá hoặc hết hạn **> 7 ngày** → ngừng chuyển tiếp; cấu hình giữ nguyên, khôi phục tài khoản là dùng lại.
- **Xác thực**: ⚠️ **Không kèm chữ ký** → bên nhận **không có cách xác thực** request đến từ LME; ai biết URL đều gửi giả được. Khuyến nghị bên nhận tự bảo vệ (giới hạn IP, URL khó đoán, thêm tham số bí mật trên path).

**Sample Input**
```json
{
  "destination": "Uxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
  "events": [
    {"type": "message", "replyToken": "xxxx", "source": {"type": "user", "userId": "Uxxxxxxxx"},
     "timestamp": 1789000000000, "message": {"id": "987654321", "type": "text", "text": "こんにちは"}}
  ]
}
```
**Sample Output**: `HTTP/1.1 200 OK` (body không được đọc tới).

## 4. Kênh L Messageデータ転送 — tag / friend_info

LME gửi 1 request chứa mảng `events[]`; mỗi item là 1 thao tác đã phát sinh + 2 field định danh friend.

**Input `events[]`**:

| Field | Type | Bắt buộc | Áp dụng | Mô tả |
|---|---|---|---|---|
| `events[]` | array\<object\> | Có | Chung | Mảng event notify ra ngoài |
| `events[].lmessage_friend_id` | integer | Có | Chung | L Message Friend ID |
| `events[].line_friend_id` | string | Có | Chung | LINE Friend ID. Hiếm: friend đã bị xoá trước khi gửi → có thể là **chuỗi rỗng**, khi đó đối chiếu bằng `lmessage_friend_id` |
| `events[].type` | string | Có | Chung | Phase 1: `tag`, `friend_info` |
| `events[].action` | string | Có | Chung | tag: `add`/`remove` · friend_info: `set`/`clear` |
| `events[].tag_id` | integer | Có điều kiện | tag | Tag ID được thao tác |
| `events[].field_id` | integer | Có điều kiện | friend_info | Field ID (built-in âm, custom dương) |
| `events[].value` | string | Có điều kiện | friend_info | Giá trị mới sau thao tác. **Không có mặt** khi `action = clear` |

**Built-in field (ID âm)**: -1 システム表示名 · -2 携帯電話 · -3 メールアドレス · -4 生年月日 · -6 都道府県 · -7 郵便番号 · -8 市区町村名 · -9 町名/番地 · -10 建物名・部屋番号 (không có -5).

**Sample Input**
```json
{
  "events": [
    {"lmessage_friend_id": 12345, "line_friend_id": "Uxxxxxxxx", "type": "tag", "action": "add", "tag_id": 101},
    {"lmessage_friend_id": 12345, "line_friend_id": "Uxxxxxxxx", "type": "friend_info", "action": "set", "field_id": -1, "value": "山田太郎"},
    {"lmessage_friend_id": 12345, "line_friend_id": "Uxxxxxxxx", "type": "friend_info", "action": "clear", "field_id": 5001}
  ]
}
```

**Gom lô**: tối đa **1.000** phần tử `events[]`/request (vượt → chia nhiều request; ⚠️ code thực tế ≤500 — xem §0 #3). Một request luôn thuộc **một LINE OA duy nhất** (không trộn nhiều tài khoản). Có thể chỉ chứa 1 phần tử.

## 5. Xác thực request (chỉ kênh LME)

| Header | Kênh | Nội dung |
|---|---|---|
| `X-Lme-Signature` | Chỉ LME | **Secret thô** của LINE OA đó, dạng `whsec_…`. **So sánh chuỗi là đủ** (KHÔNG HMAC — xem §0 #1) |
| `X-Lme-Delivery-Id` | Cả 2 | UUID định danh **một request** (vd `3f2a8c10-9d4b-4e21-8a77-1c5e9b0d6f34`). **Giữ nguyên qua cả 3 lần gửi** cùng nội dung; khác nhau giữa nội dung khác → khóa để dedupe |
| `X-Lme-Timestamp` | Cả 2 | Thời điểm gửi, **epoch mili giây** (vd `1789000000000`, cùng đơn vị `timestamp` webhook LINE). Mỗi lần gửi lại là giá trị mới |
| `Content-Type` | Cả 2 | `application/json; charset=utf-8` |

**Vòng đời secret**: là 「署名シークレット」 của LINE OA (xem/sao chép/tái tạo trên màn 「Webhook転送」), tiền tố `whsec_`. Khi **tái tạo**: admin cho secret cũ **hết hiệu lực ngay**, nhưng job đọc config theo chu kỳ 1 phút nên **tới ~1 phút sau vẫn gửi secret CŨ**. → **Khuyến nghị bên nhận chấp nhận cả secret cũ lẫn mới trong ~2 phút** rồi mới bỏ cũ; nếu đổi sang mới ngay, request trong khoảng chờ bị từ chối và rơi vào danh sách lỗi dù không ai làm sai.

## 6. Khi gửi thất bại

**Luồng**: LẦN 1 (gửi ngay; timeout/5xx → chờ 1 phút gửi lại; lỗi khác → ghi lỗi ngay) → LẦN 2–3 (tối đa 2 lần nữa, mỗi lần cách 1 phút, cùng nội dung + cùng `X-Lme-Delivery-Id`; thành công bất kỳ lần nào thì dừng) → SAU 3 LẦN (cả 3 timeout/5xx, ~2 phút → ghi **1 bản ghi lỗi**).

**Chuỗi hiển thị lỗi cho người dùng** (tách riêng theo kênh):

| Tình huống | Mã | Hiển thị trên LME |
|---|---|---|
| Không mở được kết nối / DNS lỗi | — | 接続できませんでした |
| Quá thời gian chờ (LME chờ > 10s **hoặc** endpoint trả mã hết giờ) | —, 408, 504 | タイムアウト（10秒） |
| Endpoint từ chối xác thực | 401, 403 | 認証エラー |
| Không tìm thấy đường dẫn | 404 | 転送先が見つかりません |
| Endpoint tạm thời không phục vụ | 503 | 転送先が一時的に応答できません |
| Lỗi phía endpoint | 5xx khác | 転送先でエラーが発生しました |
| Mã khác | mã thật | ⚠️ Chưa chốt chuỗi hiển thị |

> Doc tự lưu ý: 「タイムアウト（10秒）」 cho 408/504 không phản ánh đúng (chính endpoint mới báo hết giờ) — có thể tách 2 chuỗi tuỳ cột mã lỗi có giá trị hay không (xem §0 #4).

## 7. Yêu cầu với endpoint bên nhận

- Trả **HTTP 2xx trong vòng 10 giây** (quá = thất bại).
- **Xử lý được nhận trùng** — dùng `X-Lme-Delivery-Id`.
- **Không phụ thuộc thứ tự nhận** — dùng `X-Lme-Timestamp` nếu cần.

## 8. Lịch sử cập nhật (từ doc gốc)

| Bản | Thời điểm (JST) | Thay đổi |
|---|---|---|
| **1.0.0** | 16/09/2026 19:35 | Bản đầu tiên |
