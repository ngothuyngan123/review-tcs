# Friend Tools

## 1. list_friends

**Description:** Tool trả về danh sách friend của bot kèm trạng thái follow. Hỗ trợ optional filter `line_names` (
PARTIAL substring match LIKE %% trên **cả** tên LINE (`line_user.name`) **và** tên hiển thị hệ thống
(`line_user.view_name`) — khớp 1 trong 2 là được, case-insensitive — cùng spec với `list_conversations`). KHÁC với
các tool list khác — đây là partial match, "田中" sẽ khớp "田中太郎".

**Tool:** `list_friends`

**Input:**
| Name | Type | Required | Description |
|------------|-----------------|----------|------------------------------------------|
| bot_id | String | Yes | Bot ID hash string lấy từ tool list_bots |
| line_names | Array of String | No | Mảng pattern PARTIAL match (LIKE `%value%`, case-insensitive, trim) trên **cả**
tên LINE (`line_user.name`) **và** tên hiển thị hệ thống (`line_user.view_name`) — khớp 1 trong 2 là được. Multiple =
OR. "田中" match "田中太郎", "田中花子"... Khi truyền, response có thêm `not_found_line_names` |
| page | Int | No | Số trang (default: 1)                    |
| limit | Int | No | Số lượng record mỗi trang (default: 100, max: 100) |

**Output:**
| Name | Type | Description |
|---------------------|-----------------|--------------------------------|
| total | Int | Tổng số friend |
| page | Int | Trang hiện tại |
| limit | Int | Số lượng record mỗi trang |
| total_pages | Int | Tổng số trang |
| friends | Json Array | Array Object Friend |
| not_found_line_names| Array of String | (Chỉ trả khi truyền `line_names`) Các pattern không match friend nào |

**Sub Object Friend:**
| Name | Type | Description |
|--------------|--------|--------------------------------------------------------|
| lmessage_friend_id | Long | ID nội bộ DB của friend (`line_user.id`) |
| line_friend_id | String | LINE UID thật (`"Uxxx"`) |
| line_name | String | Tên hiển thị trên LINE |
| system_name | String | Tên hiển thị hệ thống (`line_user.view_name`) — field riêng, null nếu chưa đặt |
| is_blocked | Boolean | Trạng thái block (true: đã block, false: đang follow) |
| followed_at | String | Ngày follow (format: yyyy-MM-dd HH:mm:ss)              |
| blocked_at | String | Ngày block (format: yyyy-MM-dd HH:mm:ss, lấy từ `updated_at` khi đã block; null nếu chưa block) |

**Sample Output:**

```json
{
  "total": 15000,
  "page": 1,
  "limit": 100,
  "total_pages": 150,
  "friends": [
    {
      "lmessage_friend_id": 50001,
      "line_friend_id": "U1a2b3c4d5e6f7081920a1b2c3d4e5f60",
      "line_name": "Nguyen Van A",
      "system_name": null,
      "is_blocked": false,
      "followed_at": "2025-06-15 10:30:00",
      "blocked_at": null
    },
    {
      "lmessage_friend_id": 50002,
      "line_friend_id": "U2b3c4d5e6f708192a03b1c2d3e4f5061",
      "line_name": "Tran Thi B",
      "system_name": "Anh B VIP",
      "is_blocked": false,
      "followed_at": "2025-08-20 14:00:00",
      "blocked_at": null
    },
    {
      "lmessage_friend_id": 50003,
      "line_friend_id": "U3c4d5e6f708192a0b1c2d3e4f5061728",
      "line_name": "Le Van C",
      "system_name": null,
      "is_blocked": true,
      "followed_at": "2025-03-10 09:00:00",
      "blocked_at": "2026-01-15 16:30:00"
    }
  ]
}
```

---

## 2. get_friend_detail

**Description:** Tool trả về chi tiết thông tin đầy đủ của nhiều friend bao gồm tags, friend info fields (cơ bản +
custom),
scenarios, lịch sử mua hàng, lịch sử đặt chỗ và ghi chú. Top-level có `system_name` (tên hiển thị hệ thống
`view_name`, null nếu chưa đặt) bên cạnh `line_name`. Danh sách `friend_info` bắt đầu với các built-in basic fields
có ID âm (khi có giá trị: -1 system_display, -2 phone_number, -3 email, -4 birthday, -6 province, -7 zip_code, -8
district, -9 township, -10 building), tiếp theo là custom fields (ID dương).

**Tool:** `get_friend_detail`

**Input:**
| Name | Type | Required | Description |
|--------------|------|----------|---------------------------------|
| lmessage_friend_ids | String | Yes | Danh sách internal DB id (`line_user.id`) cách nhau bằng dấu phẩy, tối đa 100. Trùng sẽ bị bỏ qua. Ví dụ: "1,2,3" |
| bot_id | String | Yes | Bot ID hash string lấy từ tool list_bots |

**Output:**
| Name | Type | Description |
|------------------|------------|----------------------------------------------------|
| lmessage_friend_id | Long | ID nội bộ DB của friend (`line_user.id`) |
| line_friend_id | String | LINE UID thật (`"Uxxx"`) |
| line_name | String | Tên hiển thị trên LINE |
| system_name | String | Tên hiển thị hệ thống (`line_user.view_name`). null nếu chưa đặt. Giá trị này cũng xuất hiện trong `friend_info` field -1 (giữ cả hai) |
| is_old_friend | Boolean | Friend cũ (true: cũ, false: mới) |
| is_blocked | Boolean | Trạng thái block (true: đã block, false: đang follow) |
| followed_at | String | Ngày follow (format: yyyy-MM-dd HH:mm:ss)          |
| blocked_at | String | Ngày block (null nếu chưa block)                   |
| memo | Json Array | Danh sách ghi chú (lấy từ bảng `memos`, sắp xếp theo position tăng dần) |
| tags | Json Array | Danh sách tag của friend |
| friend_info | Json Array | Danh sách thông tin của friend: built-in basic fields (ID âm, chỉ khi có giá trị — tên hệ thống/view_name nằm ở field -1) trước, rồi custom fields (ID dương). Value là đường dẫn media sẽ được prepend host |
| scenarios | Json Array | Danh sách scenario đang/đã follow |
| purchase_history | Json Array | Lịch sử mua hàng |
| booking_history | Json Object | Lịch sử đặt chỗ `{ salon: [...], lesson: [...] }` |

**Sub Object Memo:**
| Name | Type | Description |
|------------|--------|--------------------------------------------|
| title | String | Tiêu đề ghi chú (nullable) |
| content | String | Nội dung ghi chú (nullable) |
| position | Int | Thứ tự hiển thị |
| created_at | String | Ngày tạo (format: yyyy-MM-dd HH:mm:ss) |

**Sub Object Tag:**
| Name | Type | Description |
|----------|--------|--------------------------------------------|
| tag_id | Int | ID của tag |
| tag_name | String | Tên tag |
| added_at | String | Ngày gắn tag (format: yyyy-MM-dd HH:mm:ss) |

**Sub Object Friend Info:**
| Name | Type | Description |
|----------|--------|-----------------------|
| field_id | Long | ID của trường thông tin (âm = built-in basic field, dương = custom field) |
| title | String | Tên trường thông tin (built-in field dùng title cố định tiếng Nhật: -1 システム表示名, -2 携帯電話, -3 メールアドレス, -4 生年月日, -6 都道府県名, -7 郵便番号, -8 市区町村名, -9 町名/番地, -10 建物名・部屋番号) |
| value | String | Giá trị |

**Sub Object Scenario:**
| Name | Type | Description |
|---------------|--------|------------------------------------------------|
| scenario_id | Int | ID của scenario |
| scenario_name | String | Tên scenario |
| status | String | Trạng thái (following/completed/stopped)       |
| started_at | String | Ngày bắt đầu (format: yyyy-MM-dd HH:mm:ss)     |
| ended_at | String | Ngày kết thúc (null nếu đang follow)           |

**Sub Object Purchase:**
| Name | Type | Description |
|---------------|--------|------------------------------------------------|
| id | Long | ID của order |
| product_name | String | Tên sản phẩm |
| quantity | Int | Số lượng (default 1 nếu null) |
| price | Long | Giá tiền (0 nếu null) |
| purchased_at | String | Ngày mua (format: yyyy-MM-dd HH:mm:ss)         |

**Sub Object Booking History:**

`booking_history` là object gồm 2 mảng: `salon` (salon bookings) và `lesson` (lesson calendar bookings). Cap 200 booking mới nhất mỗi loại, sort theo ngày đặt DESC.

**Sub Object Salon Booking:**
| Name | Type | Description |
|-----------------|---------|---------------------------------------------------------------------|
| id | Int | ID của booking |
| salon_id | Int | ID của salon |
| salon_name | String | Tên salon |
| course_name | String | Tên course (`指定なし` nếu không chọn) |
| staff_name | String | Tên staff (`指定なし` nếu không chọn) |
| date_booking | String | Ngày giờ booking (format: `yyyy-MM-dd HH:mm ~ HH:mm`) |
| status | String | `request` / `approved` / `admin_booked` / `full_slot` / `cancelled` / `request_cancel` / `denied` / `admin_cancelled` |
| payment_status | String | `unpaid` / `paid` / `no_bill` / `refunded` |
| payment_amount | Int | Số tiền thanh toán (nullable) |
| form_answers | Array | Câu trả lời form lúc đặt lịch — `[{question, answer}]`, `[]` nếu không có |
| created_at | String | Ngày tạo booking (format: yyyy-MM-dd HH:mm:ss) |

**Sub Object Lesson Booking:**
| Name | Type | Description |
|-----------------|---------|---------------------------------------------------------------------|
| id | Int | ID của booking |
| calendar_id | Int | ID của lesson calendar |
| calendar_name | String | Tên lesson calendar |
| course_name | String | Tên course (snapshot tại thời điểm booking, hoặc `指定なし`) |
| booking_date | String | Ngày giờ booking (format: `yyyy-MM-dd HH:mm ~ HH:mm`) |
| status | String | Giống salon booking |
| payment_status | String | Giống salon booking |
| payment_amount | Int | Số tiền thanh toán (nullable) |
| form_answers | Array | Câu trả lời form lúc đặt lịch — `[{question, answer}]`, `[]` nếu không có |
| created_at | String | Ngày tạo booking (format: yyyy-MM-dd HH:mm:ss) |

**Sample Output:**

```json
[
  {
  "lmessage_friend_id": 50001,
  "line_friend_id": "U1a2b3c4d5e6f7081920a1b2c3d4e5f60",
  "line_name": "Nguyen Van A",
  "system_name": "Anh A VIP",
  "is_old_friend": true,
  "is_blocked": false,
  "followed_at": "2025-06-15 10:30:00",
  "blocked_at": null,
  "memo": [
    {
      "title": "Khách VIP",
      "content": "Cần chăm sóc đặc biệt",
      "position": 1,
      "created_at": "2025-08-01 14:00:00"
    },
    {
      "title": "Đơn hàng #12345",
      "content": "Đã giải quyết khiếu nại",
      "position": 2,
      "created_at": "2026-01-15 09:30:00"
    }
  ],
  "tags": [
    {
      "tag_id": 101,
      "tag_name": "VIP Member",
      "added_at": "2025-08-01 14:00:00"
    },
    {
      "tag_id": 102,
      "tag_name": "Summer 2026",
      "added_at": "2026-01-20 10:00:00"
    },
    {
      "tag_id": 103,
      "tag_name": "Promotion Interest",
      "added_at": "2026-02-05 09:30:00"
    }
  ],
  "friend_info": [
    {
      "field_id": -1,
      "title": "システム表示名",
      "value": "Anh A VIP"
    },
    {
      "field_id": -2,
      "title": "携帯電話",
      "value": "0901234567"
    },
    {
      "field_id": -3,
      "title": "メールアドレス",
      "value": "nguyenvana@email.com"
    },
    {
      "field_id": -4,
      "title": "生年月日",
      "value": "1990-05-15"
    },
    {
      "field_id": 204,
      "title": "Giới tính",
      "value": "Nam"
    },
    {
      "field_id": 205,
      "title": "Điểm tích lũy",
      "value": "2500"
    }
  ],
  "scenarios": [
    {
      "scenario_id": 3001,
      "scenario_name": "Welcome New Member",
      "status": "completed",
      "started_at": "2025-06-15 10:30:00",
      "ended_at": "2025-06-18 10:00:00"
    },
    {
      "scenario_id": 3002,
      "scenario_name": "VIP Member Benefits",
      "status": "following",
      "started_at": "2025-08-01 14:00:00",
      "ended_at": null
    }
  ],
  "purchase_history": [
    {
      "id": 8001,
      "product_name": "Premium Subscription",
      "quantity": 1,
      "price": 299000,
      "purchased_at": "2026-01-10 15:30:00"
    },
    {
      "id": 8002,
      "product_name": "Gift Box Set A",
      "quantity": 2,
      "price": 150000,
      "purchased_at": "2025-12-20 10:00:00"
    },
    {
      "id": 8003,
      "product_name": "Monthly Package",
      "quantity": 1,
      "price": 99000,
      "purchased_at": "2025-11-01 09:00:00"
    }
  ],
  "booking_history": {
    "salon": [
      {
        "id": 9001,
        "salon_id": 10,
        "salon_name": "Main Salon",
        "course_name": "Hair Cut",
        "staff_name": "Tanaka",
        "date_booking": "2026-04-20 10:00 ~ 11:00",
        "status": "approved",
        "payment_status": "paid",
        "payment_amount": 3000,
        "form_answers": [
          {"question": "Họ tên?", "answer": "Nguyen Van A"},
          {"question": "Ghi chú?", "answer": "Khách yêu cầu phòng yên tĩnh"}
        ],
        "created_at": "2026-04-15 14:22:01"
      }
    ],
    "lesson": [
      {
        "id": 7001,
        "calendar_id": 5,
        "calendar_name": "Yoga Studio",
        "course_name": "Beginner Yoga",
        "booking_date": "2026-04-22 09:00 ~ 10:00",
        "status": "approved",
        "payment_status": "paid",
        "payment_amount": 2000,
        "form_answers": [
          {"question": "Trình độ yoga?", "answer": "Beginner"}
        ],
        "created_at": "2026-04-10 08:30:11"
      }
    ]
  }
  }
]
```
