# Lesson Booking Tools

## 1. list_lesson_calendars

**Description:** Tool trả về danh sách tất cả calendar lesson booking của bot kèm thống kê cơ bản — để AI nắm được các lịch học đang có, trạng thái hoạt động và số lượng booking trước khi gọi tool detail hoặc lịch sử.

**Tool:** `list_lesson_calendars`

**Input:**
| Name | Type | Required | Description |
|----------------|-----------------|----------|-------------|
| bot_id | String | Yes | Bot ID hash string lấy từ tool list_bots |
| calendar_names | Array of String | No | Mảng pattern PARTIAL match (LIKE `%value%` trên admin `calendar_name`,
case-insensitive, trim). Multiple = OR. Ví dụ: `["英会話"]` — 管理用 calendar_name への部分一致 |

**Output:**
| Name | Type | Description |
|--------------------------|-----------------|-------------|
| calendars | Json Array | Array Object Calendar |
| not_found_calendar_names | Array of String | (Chỉ trả khi truyền `calendar_names`) Patterns không match calendar nào —
`calendar_names` 指定時のみ返却 |

**Sub Object Calendar:**
| Name | Type | Description |
|------|------|-------------|
| id | Int | ID calendar |
| calendar_name | String | Tên quản lý nội bộ |
| line_name | String | Tên hiển thị cho end user trong màn hình booking |
| enable_use_calendar | Boolean | true = đang bật |
| stats | Object | Thống kê tổng — Sub Object LessonStats |
| created_at | String | Ngày tạo (format: yyyy-MM-dd HH:mm:ss) |

**Sub Object LessonStats:**
| Name | Type | Description |
|------|------|-------------|
| course_count | Int | Tổng số khóa học |
| total_bookings | Int | Tổng lượt booking |
| total_cancels | Int | Tổng lượt hủy |

**Sample Output:**

```json
{
  "calendars": [
    {
      "id": 1,
      "calendar_name": "English Lesson Center",
      "line_name": "英会話スクール",
      "enable_use_calendar": true,
      "stats": {
        "course_count": 4,
        "total_bookings": 320,
        "total_cancels": 18
      },
      "created_at": "2025-04-01 09:00:00"
    },
    {
      "id": 2,
      "calendar_name": "Piano Studio",
      "line_name": "ピアノ教室",
      "enable_use_calendar": false,
      "stats": {
        "course_count": 2,
        "total_bookings": 55,
        "total_cancels": 3
      },
      "created_at": "2025-06-15 10:30:00"
    }
  ]
}
```

---

## 2. get_lesson_calendar_detail

**Description:** Tool trả về cấu hình đầy đủ của một calendar lesson booking, bao gồm danh sách khóa học, form câu hỏi khi booking và cài đặt approve + actions — để AI phân tích cấu trúc và đề xuất cải thiện.

**Tool:** `get_lesson_calendar_detail`

**Input:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| bot_id | String | Yes | Bot ID hash string lấy từ tool list_bots |
| calendar_ids | String | Yes | Danh sách ID Calendar cách nhau bằng dấu phẩy, tối đa 100. Trùng sẽ bị bỏ qua. Ví dụ: "1,2,3" |

**Output:** Json Array — mỗi phần tử ứng với 1 ID trong `calendar_ids`, cấu trúc như sau:

| Name | Type | Description |
|------|------|-------------|
| id | Int | ID calendar |
| calendar_name | String | Tên quản lý nội bộ |
| line_name | String | Tên hiển thị cho end user |
| description_top | String | Mô tả hiển thị trong màn hình booking (null nếu chưa có) |
| image_top | String | URL ảnh hiển thị trong màn hình booking (null nếu chưa có) |
| enable_use_calendar | Boolean | true = đang bật |
| courses | Json Array | Danh sách khóa học — Array Sub Object CourseInfo |
| forms | Json Array | Form câu hỏi khi booking — Array Sub Object FormQuestion |
| booking_settings | Object | Cài đặt approve + actions — Sub Object LessonBookingSettings |
| created_at | String | Ngày tạo (format: yyyy-MM-dd HH:mm:ss) |
| updated_at | String | Ngày cập nhật (format: yyyy-MM-dd HH:mm:ss) |

**Sub Object CourseInfo:**
| Name | Type | Description |
|------|------|-------------|
| id | Int | ID khóa học |
| course_name | String | Tên khóa học hiển thị cho end user |
| system_name | String | Tên quản lý nội bộ (null nếu chưa đặt) |
| duration_minutes | Int | Thời lượng (phút) |
| amount | Int | Học phí (null nếu miễn phí) |
| course_image | String | URL ảnh khóa học (null nếu chưa có) |
| course_description | String | Mô tả khóa học (null nếu chưa có) |
| visible | Boolean | true = hiển thị trong trang booking |
| actions | Object | Action tự động của khóa học — Sub Object ItemActions (null nếu chưa cài action nào) |
| messages | Object | Message text tự động của khóa học — Sub Object ItemMessages (null nếu chưa cài message nào) |

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

**Sub Object LessonBookingSettings:**
| Name | Type | Description |
|------|------|-------------|
| approve_type | String | Loại approve booking: `auto` = tự động approve / `admin` = cần admin duyệt (null nếu chưa có setting) |
| cancel_type | String | Loại cancel booking: `auto` = tự động cancel / `admin` = cần admin duyệt cancel / `no_cancel` = không cho phép hủy (null nếu chưa có setting) |
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

**Sample Output:**

```json
[
  {
  "id": 1,
  "calendar_name": "English Lesson Center",
  "line_name": "英会話スクール",
  "description_top": "初心者から上級者まで対応した英会話スクールです",
  "image_top": "https://example.com/img/english.jpg",
  "enable_use_calendar": true,
  "courses": [
    {
      "id": 10,
      "course_name": "Morning English",
      "system_name": "eng_am",
      "duration_minutes": 60,
      "amount": 3000,
      "course_image": "https://example.com/img/morning.jpg",
      "course_description": "朝の英会話レッスン（初心者向け）",
      "visible": true,
      "actions": {
        "after_booking": [
          { "id": 501, "action_id": 88, "type": "tag", "content": "タグ「Morning受講」をつける", "data": { "action": 1, "ids": ["45"] } }
        ]
      },
      "messages": {
        "after_booking": "レッスンのご予約ありがとうございます"
      }
    },
    {
      "id": 11,
      "course_name": "Business English",
      "system_name": "eng_biz",
      "duration_minutes": 90,
      "amount": 5000,
      "course_image": null,
      "course_description": "ビジネスシーンで使える英語",
      "visible": true,
      "actions": null,
      "messages": null
    },
    {
      "id": 12,
      "course_name": "試験対策コース",
      "system_name": null,
      "duration_minutes": 60,
      "amount": 4000,
      "course_image": null,
      "course_description": null,
      "visible": false,
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
      "question": "英語レベルを選んでください",
      "sub_question": null,
      "required": true,
      "options": "初心者,中級者,上級者"
    }
  ],
  "booking_settings": {
    "approve_type": "auto",
    "cancel_type": "admin",
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
  "created_at": "2025-04-01 09:00:00",
  "updated_at": "2026-01-15 14:30:00"
  }
]
```

---

## 3. get_lesson_calendar_bookings

**Description:** Tool trả về lịch sử booking của một calendar lesson, có phân trang và lọc theo thời gian — để AI phân tích xu hướng đặt lịch, tỷ lệ hủy và câu trả lời form của user.

**Tool:** `get_lesson_calendar_bookings`

**Input:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| bot_id | String | Yes | Bot ID hash string lấy từ tool list_bots |
| calendar_id | Int | Yes | ID calendar lấy từ tool list_lesson_calendars |
| from_date | String | No | Ngày bắt đầu lọc theo booking_date (format: yyyy-MM-dd) |
| to_date | String | No | Ngày kết thúc lọc theo booking_date (format: yyyy-MM-dd) |
| page | Int | No | Số trang (default: 1) |
| limit | Int | No | Số record mỗi trang (default: 100, max: 100) |

**Output:**
| Name | Type | Description |
|------|------|-------------|
| total | Int | Tổng số record |
| page | Int | Trang hiện tại |
| limit | Int | Số record mỗi trang |
| total_pages | Int | Tổng số trang |
| bookings | Json Array | Array Object LessonBooking |

**Sub Object LessonBooking:**
| Name | Type | Description |
|------|------|-------------|
| id | Int | ID booking |
| reception_id | Int | ID khung giờ (calendar_course_receptions.id) |
| course_id | Int | ID khóa học (null nếu không chọn) |
| course_name | String | Tên khóa học snapshot tại thời điểm booking; nếu không có snapshot thì join theo course_id; `指定なし` nếu không chọn khóa học |
| booking_date | String | Ngày giờ đặt lịch từ khung giờ tiếp nhận (format: yyyy-MM-dd HH:mm ~ HH:mm; null nếu khung giờ đã bị xóa) |
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
  "total": 320,
  "page": 1,
  "limit": 100,
  "total_pages": 7,
  "bookings": [
    {
      "id": 1001,
      "reception_id": 55,
      "course_id": 10,
      "course_name": "Morning English",
      "booking_date": "2026-02-20 09:00 ~ 10:00",
      "lmessage_friend_id": 12345,
      "line_friend_id": "U4d5e6f708192a3b0c1d2e3f405162738",
      "user_name": "Nguyen Van A",
      "status": "approved",
      "payment_status": "paid",
      "payment_amount": 3000,
      "form_answers": [
        { "question": "お名前を入力してください", "answer": "Nguyen Van A" },
        { "question": "英語レベルを選んでください", "answer": "初心者" }
      ],
      "created_at": "2026-02-18 10:30:00"
    },
    {
      "id": 1002,
      "reception_id": 60,
      "course_id": 11,
      "course_name": "Business English",
      "booking_date": "2026-02-21 14:00 ~ 15:00",
      "lmessage_friend_id": 67890,
      "line_friend_id": "U5e6f708192a3b4c0d1e2f30415263748",
      "user_name": "Tran Thi B",
      "status": "cancelled",
      "payment_status": "refunded",
      "payment_amount": 5000,
      "form_answers": [
        { "question": "お名前を入力してください", "answer": "Tran Thi B" },
        { "question": "英語レベルを選んでください", "answer": "中級者" }
      ],
      "created_at": "2026-02-19 09:15:00"
    }
  ]
}
```
