# Salon Booking Tools

## 1. list_salons

**Description:** Tool trả về danh sách tất cả salon booking của bot kèm thống kê cơ bản — để AI nắm được các salon đang có, số dịch vụ, nhân viên và tổng booking trước khi gọi tool detail hoặc lịch sử.

**Tool:** `list_salons`

**Input:**
| Name | Type | Required | Description |
|----------------|-----------------|----------|-------------|
| bot_id | String | Yes | Bot ID hash string lấy từ tool list_bots |
| calendar_names | Array of String | No | Mảng pattern PARTIAL match (LIKE `%value%` trên admin `calendar_name`,
case-insensitive, trim). Multiple = OR. Ví dụ: `["ヘアサロン"]` — 管理用 calendar_name への部分一致 |

**Output:**
| Name | Type | Description |
|--------------------------|-----------------|-------------|
| salons | Json Array | Array Object Salon |
| not_found_calendar_names | Array of String | (Chỉ trả khi truyền `calendar_names`) Patterns không match salon nào —
`calendar_names` 指定時のみ返却 |

**Sub Object Salon:**
| Name | Type | Description |
|------|------|-------------|
| id | Int | ID salon |
| calendar_name | String | Tên quản lý nội bộ |
| manager_name | String | Tên người quản lý (null nếu chưa đặt) |
| enable_use_calendar | Boolean | true = đang bật |
| use_course | Boolean | true = có tính năng dịch vụ (course) |
| use_staff | Boolean | true = có tính năng nhân viên (staff) |
| stats | Object | Thống kê tổng — Sub Object SalonStats |
| created_at | String | Ngày tạo (format: yyyy-MM-dd HH:mm:ss) |

**Sub Object SalonStats:**
| Name | Type | Description |
|------|------|-------------|
| course_count | Int | Tổng số dịch vụ |
| staff_count | Int | Tổng số nhân viên |
| total_bookings | Int | Tổng lượt booking |

**Sample Output:**

```json
{
  "salons": [
    {
      "id": 1,
      "calendar_name": "Beauty Salon ABC",
      "manager_name": "Yamamoto",
      "enable_use_calendar": true,
      "use_course": true,
      "use_staff": true,
      "stats": {
        "course_count": 5,
        "staff_count": 3,
        "total_bookings": 240
      },
      "created_at": "2025-03-01 09:00:00"
    },
    {
      "id": 2,
      "calendar_name": "Nail Studio XYZ",
      "manager_name": null,
      "enable_use_calendar": true,
      "use_course": true,
      "use_staff": false,
      "stats": {
        "course_count": 8,
        "staff_count": 0,
        "total_bookings": 180
      },
      "created_at": "2025-08-10 14:00:00"
    }
  ]
}
```

---

## 2. get_salon_detail

**Description:** Tool trả về cấu hình đầy đủ của một salon, bao gồm menu dịch vụ, nhân viên, form câu hỏi khi booking, cài đặt approve + actions và buffer time — để AI phân tích cấu trúc và đề xuất cải thiện.

**Tool:** `get_salon_detail`

**Input:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| bot_id | String | Yes | Bot ID hash string lấy từ tool list_bots |
| salon_ids | String | Yes | Danh sách ID Salon cách nhau bằng dấu phẩy, tối đa 100. Trùng sẽ bị bỏ qua. Ví dụ: "1,2,3" |

**Output:** Json Array — mỗi phần tử ứng với 1 ID trong `salon_ids`, cấu trúc như sau:

| Name | Type | Description |
|------|------|-------------|
| id | Int | ID salon |
| calendar_name | String | Tên quản lý nội bộ |
| manager_name | String | Tên người quản lý (null nếu chưa đặt) |
| enable_use_calendar | Boolean | true = đang bật |
| use_course | Boolean | true = có tính năng dịch vụ |
| use_staff | Boolean | true = có tính năng nhân viên |
| setting_time_unit | Int | Đơn vị thời gian (phút) cho booking slot (VD: 30) |
| description_top | String | Mô tả hiển thị trong màn hình booking (null nếu chưa có) |
| image_top | String | URL ảnh hiển thị trong màn hình booking (null nếu chưa có) |
| menus | Json Array | Danh sách nhóm dịch vụ — Array Sub Object MenuGroup |
| staff | Json Array | Danh sách nhân viên — Array Sub Object StaffInfo |
| forms | Json Array | Form câu hỏi khi booking — Array Sub Object FormQuestion |
| booking_settings | Object | Cài đặt approve + actions — Sub Object SalonBookingSettings |
| time_free | Object | Cài đặt buffer time thông thường — Sub Object TimeBuffer |
| seasonal | Json Array | Cài đặt buffer time theo mùa — Array Sub Object SeasonalBuffer (empty array nếu không có) |
| created_at | String | Ngày tạo (format: yyyy-MM-dd HH:mm:ss) |
| updated_at | String | Ngày cập nhật (format: yyyy-MM-dd HH:mm:ss) |

**Sub Object MenuGroup:**
| Name | Type | Description |
|------|------|-------------|
| menu_name | String | Tên nhóm dịch vụ (null = nhóm gom các dịch vụ chưa thuộc menu nào) |
| menu_image | String | URL ảnh nhóm dịch vụ (null nếu chưa có) |
| courses | Json Array | Danh sách dịch vụ trong nhóm — Array Sub Object CourseItem |

**Sub Object CourseItem:**
| Name | Type | Description |
|------|------|-------------|
| id | Int | ID dịch vụ |
| course_name | String | Tên dịch vụ |
| system_name | String | Tên quản lý nội bộ (null nếu chưa đặt) |
| duration_minutes | Int | Thời lượng (phút) |
| amount | Int | Giá dịch vụ (null nếu miễn phí) |
| course_image | String | URL ảnh dịch vụ (null nếu chưa có) |
| course_description | String | Mô tả dịch vụ (null nếu chưa có) |
| visible | Boolean | true = hiển thị trong trang booking |
| actions | Object | Action tự động của dịch vụ — Sub Object ItemActions (null nếu chưa cài action nào) |
| messages | Object | Message text tự động của dịch vụ — Sub Object ItemMessages (null nếu chưa cài message nào) |

**Sub Object StaffInfo:**
| Name | Type | Description |
|------|------|-------------|
| id | Int | ID nhân viên |
| staff_name | String | Tên nhân viên |
| staff_image | String | URL ảnh nhân viên (null nếu chưa có) |
| staff_description | String | Mô tả nhân viên (null nếu chưa có) |
| staff_bill | Int | Phụ thu của nhân viên (0 = không phụ thu) |
| is_all_course | Boolean | true = phụ trách tất cả dịch vụ |
| course_ids | String | IDs dịch vụ phụ trách, comma-separated (null nếu is_all_course = true) |
| actions | Object | Action tự động của nhân viên — Sub Object ItemActions (null nếu chưa cài action nào) |
| messages | Object | Message text tự động của nhân viên — Sub Object ItemMessages (null nếu chưa cài message nào) |

**Sub Object ItemActions:** (field nào null sẽ bị omit khỏi JSON)
| Name | Type | Description |
|------|------|-------------|
| after_booking | Json Array | Action chạy sau khi booking — Array Sub Object ActionItem (omit nếu chưa cài) |
| on_approve | Json Array | Action chạy khi booking được duyệt — Array Sub Object ActionItem (omit nếu chưa cài) |

**Sub Object ItemMessages:** (field nào null sẽ bị omit khỏi JSON)
| Name | Type | Description |
|------|------|-------------|
| after_booking | String | Message text gửi sau khi booking (omit nếu không dùng chế độ message) |
| on_approve | String | Message text gửi khi booking được duyệt (omit nếu không dùng chế độ message) |

**Sub Object FormQuestion:**
| Name | Type | Description |
|------|------|-------------|
| id | Int | ID form question |
| form_type | String | Loại câu hỏi: `text` / `textarea` / `radio` / `checkbox` / `datetime` |
| question | String | Nội dung câu hỏi |
| sub_question | String | Câu hỏi phụ (null nếu không có) |
| required | Boolean | true = bắt buộc điền |
| options | String | Các lựa chọn (null nếu form_type là text / textarea / datetime) |

**Sub Object SalonBookingSettings:**
| Name | Type | Description |
|------|------|-------------|
| approve_type | String | Loại approve booking: `auto` = tự động approve / `admin` = cần admin duyệt (null nếu chưa có setting) |
| cancel_type | String | Loại cancel booking: `auto` = tự động cancel / `admin` = cần admin duyệt cancel / `no_cancel` = không cho phép hủy (null nếu chưa có setting) |
| limit_per_customer | Int | Giới hạn booking mỗi customer (0 = không giới hạn) |
| actions | Object | Action tự động theo sự kiện — Sub Object BookingActions |
| messages | Object | Message text gửi theo sự kiện — Sub Object BookingMessages |

**Sub Object BookingActions:**
| Name | Type | Description |
|------|------|-------------|
| on_auto_approve | Json Array | Action khi auto-approve booking (approve_type=auto) — Array Sub Object ActionItem (null nếu chưa cài) |
| on_request | Json Array | Action khi user gửi yêu cầu booking (approve_type=admin) — Array Sub Object ActionItem (null nếu chưa cài) |
| on_approve | Json Array | Action khi admin approve booking (approve_type=admin) — Array Sub Object ActionItem (null nếu chưa cài) |
| on_reject | Json Array | Action khi admin từ chối booking (approve_type=admin) — Array Sub Object ActionItem (null nếu chưa cài) |
| on_auto_cancel | Json Array | Action khi auto-cancel (cancel_type=auto) — Array Sub Object ActionItem (null nếu chưa cài) |
| on_request_cancel | Json Array | Action khi user gửi yêu cầu cancel (cancel_type=admin) — Array Sub Object ActionItem (null nếu chưa cài) |
| on_approve_cancel | Json Array | Action khi admin approve cancel (cancel_type=admin) — Array Sub Object ActionItem (null nếu chưa cài) |
| on_reject_cancel | Json Array | Action khi admin từ chối cancel (cancel_type=admin) — Array Sub Object ActionItem (null nếu chưa cài) |

**Sub Object BookingMessages:**
| Name | Type | Description |
|------|------|-------------|
| on_auto_approve | String | Message text gửi khi auto-approve booking (null nếu chưa cài) |
| on_request | String | Message text gửi khi user gửi yêu cầu booking (null nếu chưa cài) |
| on_approve | String | Message text gửi khi admin approve booking (null nếu chưa cài) |
| on_reject | String | Message text gửi khi admin từ chối booking (null nếu chưa cài) |
| on_auto_cancel | String | Message text gửi khi auto-cancel (null nếu chưa cài) |
| on_request_cancel | String | Message text gửi khi user gửi yêu cầu cancel (null nếu chưa cài) |
| on_approve_cancel | String | Message text gửi khi admin approve cancel (null nếu chưa cài) |
| on_reject_cancel | String | Message text gửi khi admin từ chối cancel (null nếu chưa cài) |

**Sub Object ActionItem:**
| Name | Type | Description |
|------|------|-------------|
| id | Int | ID record action detail |
| action_id | Int | ID nhóm action (các action detail cùng nhóm dùng chung action_id) |
| type | String | Loại action: `tag` / `scenario` / `richmenu` / `text` / `template` / `bookmark` / `friend_info` / `handling_status` / `block` / `remind` |
| content | String | Mô tả action dạng text tiếng Nhật (VD: `タグ「VIP」をつける`, `テンプレート「Welcome」を送信`) |
| data | Object | Raw data cài đặt của action (key thay đổi theo loại action; omit nếu không parse được) |

**Sub Object TimeBuffer:**
| Name | Type | Description |
|------|------|-------------|
| before_minutes | Int | Buffer time trước booking (phút) — null nếu tắt buffer trước |
| after_minutes | Int | Buffer time sau booking (phút) — null nếu tắt buffer sau |

**Sub Object SeasonalBuffer:**
| Name | Type | Description |
|------|------|-------------|
| date_start | String | Ngày bắt đầu mùa (format: yyyy-MM-dd) |
| date_end | String | Ngày kết thúc mùa (format: yyyy-MM-dd) |

**Sample Output:**

```json
[
  {
  "id": 1,
  "calendar_name": "Beauty Salon ABC",
  "manager_name": "Yamamoto",
  "enable_use_calendar": true,
  "use_course": true,
  "use_staff": true,
  "setting_time_unit": 30,
  "description_top": "トータルビューティーサロンです。お気軽にご予約ください。",
  "image_top": "https://example.com/img/salon-top.jpg",
  "menus": [
    {
      "menu_name": "ヘアケア",
      "menu_image": "https://example.com/img/hair.jpg",
      "courses": [
        {
          "id": 10,
          "course_name": "カット",
          "system_name": "cut_basic",
          "duration_minutes": 60,
          "amount": 5000,
          "course_image": "https://example.com/img/cut.jpg",
          "course_description": "シャンプー・ブロー込み",
          "visible": true,
          "actions": {
            "after_booking": [
              { "id": 501, "action_id": 88, "type": "tag", "content": "タグ「カット予約」をつける", "data": { "action": 1, "ids": ["45"] } }
            ]
          },
          "messages": {
            "after_booking": "ご予約ありがとうございます"
          }
        },
        {
          "id": 11,
          "course_name": "カラー",
          "system_name": null,
          "duration_minutes": 120,
          "amount": 8000,
          "course_image": null,
          "course_description": "全体カラー",
          "visible": true,
          "actions": null,
          "messages": null
        }
      ]
    },
    {
      "menu_name": "トリートメント",
      "menu_image": null,
      "courses": [
        {
          "id": 12,
          "course_name": "ヘアトリートメント",
          "system_name": null,
          "duration_minutes": 30,
          "amount": 2000,
          "course_image": null,
          "course_description": null,
          "visible": true,
          "actions": null,
          "messages": null
        }
      ]
    }
  ],
  "staff": [
    {
      "id": 3,
      "staff_name": "田中",
      "staff_image": "https://example.com/img/tanaka.jpg",
      "staff_description": "10年の経験を持つスタイリスト",
      "staff_bill": 1000,
      "is_all_course": true,
      "course_ids": null,
      "actions": {
        "after_booking": [
          { "id": 502, "action_id": 89, "type": "tag", "content": "タグ「指名:田中」をつける", "data": { "action": 1, "ids": ["46"] } }
        ]
      },
      "messages": {
        "after_booking": "田中が担当いたします"
      }
    },
    {
      "id": 4,
      "staff_name": "鈴木",
      "staff_image": "https://example.com/img/suzuki.jpg",
      "staff_description": null,
      "staff_bill": 0,
      "is_all_course": false,
      "course_ids": "10,11",
      "actions": null,
      "messages": null
    }
  ],
  "forms": [
    {
      "id": 5,
      "form_type": "text",
      "question": "お名前を入力してください",
      "sub_question": null,
      "required": true,
      "options": null
    },
    {
      "id": 6,
      "form_type": "radio",
      "question": "初めてのご来店ですか？",
      "sub_question": null,
      "required": true,
      "options": "はい,いいえ"
    }
  ],
  "booking_settings": {
    "approve_type": "auto",
    "cancel_type": "admin",
    "limit_per_customer": 0,
    "actions": {
      "on_auto_approve": [
        { "id": 601, "action_id": 90, "type": "tag", "content": "タグ「予約確定」をつける", "data": { "action": 1, "ids": ["51"] } }
      ],
      "on_request": [
        { "id": 602, "action_id": 91, "type": "tag", "content": "タグ「予約申請中」をつける", "data": { "action": 1, "ids": ["52"] } }
      ],
      "on_approve": null,
      "on_reject": null,
      "on_auto_cancel": [
        { "id": 603, "action_id": 92, "type": "tag", "content": "タグ「予約確定」をはずす", "data": { "action": 2, "ids": ["51"] } },
        { "id": 604, "action_id": 92, "type": "tag", "content": "タグ「キャンセル済み」をつける", "data": { "action": 1, "ids": ["53"] } }
      ],
      "on_request_cancel": null,
      "on_approve_cancel": null,
      "on_reject_cancel": null
    },
    "messages": {
      "on_auto_approve": "ご予約が確定しました。当日お待ちしております。",
      "on_request": "予約リクエストを受け付けました。確認後ご連絡いたします。",
      "on_approve": null,
      "on_reject": null,
      "on_auto_cancel": "キャンセルを受け付けました。",
      "on_request_cancel": null,
      "on_approve_cancel": null,
      "on_reject_cancel": null
    }
  },
  "time_free": {
    "before_minutes": 10,
    "after_minutes": 10
  },
  "seasonal": [
    {
      "date_start": "2026-07-01",
      "date_end": "2026-08-31"
    }
  ],
  "created_at": "2025-03-01 09:00:00",
  "updated_at": "2026-02-20 11:00:00"
  }
]
```

---

## 3. get_salon_bookings

**Description:** Tool trả về lịch sử booking của một salon, có phân trang và lọc theo thời gian — bao gồm thông tin dịch vụ, nhân viên, câu trả lời form và trạng thái thanh toán — để AI phân tích xu hướng booking và hành vi user.

**Tool:** `get_salon_bookings`

**Input:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| bot_id | String | Yes | Bot ID hash string lấy từ tool list_bots |
| salon_id | Int | Yes | ID salon lấy từ tool list_salons |
| from_date | String | No | Ngày bắt đầu lọc theo date_booking (format: yyyy-MM-dd) |
| to_date | String | No | Ngày kết thúc lọc theo date_booking (format: yyyy-MM-dd) |
| page | Int | No | Số trang (default: 1) |
| limit | Int | No | Số record mỗi trang (default: 100, max: 100) |

**Output:**
| Name | Type | Description |
|------|------|-------------|
| total | Int | Tổng số record |
| page | Int | Trang hiện tại |
| limit | Int | Số record mỗi trang |
| total_pages | Int | Tổng số trang |
| bookings | Json Array | Array Object SalonBooking |

**Sub Object SalonBooking:**
| Name | Type | Description |
|------|------|-------------|
| id | Int | ID booking |
| course_id | Int | ID dịch vụ (null hoặc 0 nếu không chọn dịch vụ) |
| course_name | String | Tên dịch vụ join theo course_id (`指定なし` nếu không chọn dịch vụ; null nếu dịch vụ đã bị xóa) |
| staff_id | Int | ID nhân viên (null hoặc 0 nếu không chọn) |
| staff_name | String | Tên nhân viên join theo staff_id (`指定なし` nếu không chọn; null nếu nhân viên đã bị xóa) |
| date_booking | String | Ngày giờ booking (format: yyyy-MM-dd HH:mm ~ HH:mm) |
| lmessage_friend_id | Long | ID nội bộ DB của friend (`line_user.id`) |
| line_friend_id | String | LINE UID thật (`"Uxxx"`) |
| user_name | String | Tên user (null nếu chưa có) |
| status | String | Trạng thái: `request` = chờ duyệt / `approved` = đã duyệt / `admin_booked` = admin tự book / `full_slot` = hết slot / `cancelled` = đã hủy / `request_cancel` = yêu cầu hủy / `denied` = bị từ chối / `admin_cancelled` = admin hủy |
| payment_status | String | Trạng thái thanh toán: `unpaid` = chưa thanh toán / `paid` = đã thanh toán / `no_bill` = không tính tiền / `refunded` = đã hoàn tiền |
| payment_amount | Int | Số tiền thanh toán (null nếu chưa thanh toán) |
| form_answers | Json Array | Câu trả lời form — Array Sub Object FormAnswer |
| created_at | String | Thời điểm tạo record (format: yyyy-MM-dd HH:mm:ss) |

**Sub Object FormAnswer:**
| Name | Type | Description |
|------|------|-------------|
| question | String | Nội dung câu hỏi |
| answer | String | Câu trả lời của user (null nếu chưa điền) |

**Sample Output:**

```json
{
  "total": 240,
  "page": 1,
  "limit": 100,
  "total_pages": 5,
  "bookings": [
    {
      "id": 301,
      "course_id": 10,
      "course_name": "カット",
      "staff_id": 3,
      "staff_name": "田中",
      "date_booking": "2026-03-10 10:00 ~ 11:00",
      "lmessage_friend_id": 12345,
      "line_friend_id": "U4d5e6f708192a3b0c1d2e3f405162738",
      "user_name": "Nguyen Van A",
      "status": "approved",
      "payment_status": "paid",
      "payment_amount": 6000,
      "form_answers": [
        { "question": "お名前を入力してください", "answer": "Nguyen Van A" },
        { "question": "初めてのご来店ですか？", "answer": "はい" }
      ],
      "created_at": "2026-03-05 15:30:00"
    },
    {
      "id": 302,
      "course_id": 11,
      "course_name": "カラー",
      "staff_id": null,
      "staff_name": "指定なし",
      "date_booking": "2026-03-10 13:00 ~ 15:00",
      "lmessage_friend_id": 67890,
      "line_friend_id": "U5e6f708192a3b4c0d1e2f30415263748",
      "user_name": "Tran Thi B",
      "status": "request",
      "payment_status": "unpaid",
      "payment_amount": null,
      "form_answers": [
        { "question": "お名前を入力してください", "answer": "Tran Thi B" },
        { "question": "初めてのご来店ですか？", "answer": "いいえ" }
      ],
      "created_at": "2026-03-08 09:00:00"
    }
  ]
}
```
