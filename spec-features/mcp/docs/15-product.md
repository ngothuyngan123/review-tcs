# Product Tools

## 1. list_products

**Description:** Tool trả về danh sách tất cả sản phẩm của bot kèm thông tin cơ bản và thống kê tổng — để AI nắm được
các sản phẩm đang có, giá và loại thanh toán trước khi gọi tool detail hoặc lịch sử. Hỗ trợ optional filter `names` (
EXACT match trên field `name` HOẶC `product_name`, case-insensitive, trim whitespace) để tìm product theo tên đầy đủ.
Khi truyền `names`, response có thêm `not_found_names` chứa các tên không match product nào.

**Tool:** `list_products`

**Input:**
| Name | Type | Required | Description |
|--------|-----------------|----------|-------------|
| bot_id | String | Yes | Bot ID hash string lấy từ tool list_bots |
| names | Array of String | No | Mảng tên product EXACT (match trên field `name` HOẶC `product_name` — sản phẩm khớp 1 trong 2 cột sẽ được trả; case-insensitive, trim). Multiple = OR. Partial KHÔNG match. Khuyến nghị dùng khi user chỉ định tên cụ thể thay vì paginate. |
| page | Integer | No | Số trang (default: 1) |
| limit | Integer | No | Số record mỗi trang (default: 100, max: 100) |

**Output:**
| Name | Type | Description |
|-----------------|-----------------|-------------|
| products | Json Array | Array Object Product |
| pagination | Json Object | Thông tin phân trang (`currentPage`, `limit`, `total`) |
| not_found_names | Array of String | (Chỉ trả khi truyền `names`) Các tên không match product nào — confirm với user trước khi tiếp tục |

**Sub Object Product:**
| Name | Type | Description |
|------|------|-------------|
| id | Long | ID sản phẩm |
| name | String | Tên sản phẩm quản lý trên hệ thống |
| item_code | String | Mã token của sản phẩm — dùng trong placeholder `[ITEM_<code>]` / `[CHANGE_<code>]` / `[CANCEL_<code>]` (nguồn: s_items.item_code) |
| product_name | String | Tên sản phẩm hiển thị với end user (null nếu chưa đặt) |
| image_product | Json Array<String> | Danh sách URL hình ảnh sản phẩm — mỗi phần tử là full URL (null nếu chưa có ảnh) |
| type_payment | String | Loại thanh toán: `one_time` = 1 lần / `weekly` = hàng tuần / `monthly` = hàng tháng / `every_3_months` = mỗi 3 tháng / `every_6_months` = mỗi 6 tháng / `yearly` = mỗi năm (`unknown` nếu giá trị khác) |
| amount | Long | Giá sản phẩm |
| tax_item | Int | Thuế (%) áp dụng cho sản phẩm |
| stats | Object | Thống kê tổng — Sub Object Stats |
| created_at | String | Ngày tạo (format: yyyy-MM-dd HH:mm:ss) |

**Sub Object Stats:**
| Name | Type | Description |
|------|------|-------------|
| number_register | Long | Tổng lượt mua / đăng ký |
| sum_sales | Long | Tổng doanh thu |
| number_cancel | Long | Tổng lượt hủy |

**Sample Output (no `names` filter):**

```json
{
  "products": [
    {
      "id": 10,
      "name": "Khóa học Python cơ bản",
      "item_code": "a1B2c3",
      "product_name": "Python入門コース",
      "image_product": ["https://example.com/img/python-1.jpg", "https://example.com/img/python-2.jpg"],
      "type_payment": "one_time",
      "amount": 9900,
      "tax_item": 10,
      "stats": {
        "number_register": 152,
        "sum_sales": 1504800,
        "number_cancel": 0
      },
      "created_at": "2025-06-01 10:00:00"
    },
    {
      "id": 11,
      "name": "Hội viên Premium",
      "item_code": "d4E5f6",
      "product_name": "プレミアム会員",
      "image_product": ["https://example.com/img/premium.jpg"],
      "type_payment": "monthly",
      "amount": 2980,
      "tax_item": 10,
      "stats": {
        "number_register": 88,
        "sum_sales": 786720,
        "number_cancel": 5
      },
      "created_at": "2025-09-01 09:00:00"
    }
  ],
  "pagination": { "currentPage": 1, "limit": 100, "total": 2 }
}
```

**Sample Output (with `names: ["Khóa học Python cơ bản", "Typo Name"]`):**

```json
{
  "products": [
    {
      "id": 10,
      "name": "Khóa học Python cơ bản",
      "item_code": "a1B2c3",
      "product_name": "Python入門コース",
      "image_product": ["https://example.com/img/python-1.jpg", "https://example.com/img/python-2.jpg"],
      "type_payment": "one_time",
      "amount": 9900,
      "tax_item": 10,
      "stats": {
        "number_register": 152,
        "sum_sales": 1504800,
        "number_cancel": 0
      },
      "created_at": "2025-06-01 10:00:00"
    }
  ],
  "pagination": { "currentPage": 1, "limit": 100, "total": 1 },
  "not_found_names": ["Typo Name"]
}
```

---

## 2. get_product_detail

**Description:** Tool trả về cấu hình đầy đủ của nhiều sản phẩm, bao gồm cài đặt thanh toán, dùng thử, giới hạn tồn kho,
giới hạn mua per person, action tự động và thống kê chi tiết — để AI phân tích cấu hình và đề xuất cải thiện.

**Tool:** `get_product_detail`

**Input:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| product_ids | String | Yes | Danh sách ID Product cách nhau bằng dấu phẩy, tối đa 100. Trùng sẽ bị bỏ qua. Ví dụ: "1,2,3" |
| bot_id | String | Yes | Bot ID hash string lấy từ tool list_bots |

**Output** (Array — mỗi phần tử là một Product Detail):
| Name | Type | Description |
|------|------|-------------|
| id | Long | ID sản phẩm |
| name | String | Tên sản phẩm quản lý trên hệ thống |
| product_name | String | Tên sản phẩm hiển thị với end user (null nếu chưa đặt) |
| image_product | Json Array<String> | Danh sách URL hình ảnh — mỗi phần tử là full URL (null nếu chưa có ảnh) |
| page_start_simple | String | Mô tả sản phẩm (null nếu chưa có) |
| type_payment | String | `one_time` / `weekly` / `monthly` / `every_3_months` / `every_6_months` / `yearly` (`unknown` nếu giá trị khác) |
| amount | Long | Giá sản phẩm |
| tax_item | Int | Thuế (%) |
| charge_limit | Object | Giới hạn số lần charge — Sub Object ChargeLimit |
| trial | Object | Cài đặt dùng thử — Sub Object Trial |
| first_payment | Object | Cài đặt giá lần đầu — Sub Object FirstPayment |
| stock | Object | Cài đặt tồn kho — Sub Object Stock |
| per_person_limit | Object | Giới hạn mua theo người — Sub Object PerPersonLimit |
| actions | Object | Action tự động theo sự kiện — Sub Object Actions |
| stats | Object | Thống kê — Sub Object DetailStats |
| created_at | String | Ngày tạo (format: yyyy-MM-dd HH:mm:ss) |
| updated_at | String | Ngày cập nhật gần nhất (format: yyyy-MM-dd HH:mm:ss) |

**Sub Object ChargeLimit:**
| Name | Type | Description |
|------|------|-------------|
| limited | Boolean | true = có giới hạn số lần charge |
| max_charges | Int | Số lần charge tối đa (null nếu limited = false) |

**Sub Object Trial:**
| Name | Type | Description |
|------|------|-------------|
| enabled | Boolean | true = có giai đoạn dùng thử |
| days | Int | Số ngày dùng thử (null nếu enabled = false) |

**Sub Object FirstPayment:**
| Name | Type | Description |
|------|------|-------------|
| enabled | Boolean | true = giá lần đầu khác với giá thường |
| amount | Long | Giá lần đầu (null nếu enabled = false) |

**Sub Object Stock:**
| Name | Type | Description |
|------|------|-------------|
| limited | Boolean | true = có giới hạn số lượng tồn kho |
| quantity | Int | Số lượng tồn kho (null nếu limited = false) |
| show_stock | Boolean | true = hiển thị số lượng tồn kho cho user |

**Sub Object PerPersonLimit:**
| Name | Type | Description |
|------|------|-------------|
| limited | Boolean | true = có giới hạn số lượng mua cho 1 user |
| max | Int | Số lượng tối đa 1 user có thể mua (null nếu limited = false) |
| show_limit | Boolean | true = hiển thị giới hạn cho user |

**Sub Object Actions:**
| Name | Type | Description |
|------|------|-------------|
| show_page | Json Array | Action khi user mở trang sản phẩm — Array Sub Object ActionItem (null nếu chưa cài) |
| contract_trial | Json Array | Action khi user đăng ký dùng thử — Array Sub Object ActionItem (null nếu chưa cài) |
| contract | Json Array | Action khi user ký hợp đồng/subscribe — Array Sub Object ActionItem (null nếu chưa cài) |
| cancel_payment | Json Array | Action khi user hủy thanh toán — Array Sub Object ActionItem (null nếu chưa cài) |
| purchase_1st | Json Array | Action khi user mua lần đầu — Array Sub Object ActionItem (null nếu chưa cài) |
| purchase_2nd | Json Array | Action khi user mua lần 2 trở đi — Array Sub Object ActionItem (null nếu chưa cài) |
| buy_error | Json Array | Action khi mua bị lỗi — Array Sub Object ActionItem (null nếu chưa cài) |

**Sub Object ActionItem:**
| Name | Type | Description |
|-----------|-------------|-------------|
| id | Long | ID của action detail |
| action_id | Long | ID nhóm action chứa action detail này |
| type | String | Loại action: `template` / `text` / `richmenu` / `scenario` / `tag` / `bookmark` / `friend_info` / `handling_status` / `block` / `remind` / ... (giá trị khác được trả nguyên gốc) |
| content | String | Mô tả action dạng human-readable (tiếng Nhật), ví dụ: `タグ「VIP」をつける`, `テンプレート「Welcome」を送信` |
| data | Json Object | Raw data JSON của action (chỉ trả khi parse được — có thể vắng; cấu trúc phụ thuộc loại action) |

**Sub Object DetailStats:**
| Name | Type | Description |
|------|------|-------------|
| number_register | Long | Tổng lượt mua / đăng ký |
| number_trial | Long | Tổng lượt dùng thử |
| number_cancel | Long | Tổng lượt hủy |
| number_refund | Long | Tổng lượt hoàn tiền |
| current_month_sales | Long | Doanh thu tháng hiện tại |
| sum_sales | Long | Tổng doanh thu tích lũy |

**Sample Output:**

```json
[
  {
  "id": 11,
  "name": "Hội viên Premium",
  "product_name": "プレミアム会員",
  "image_product": ["https://example.com/img/premium-1.jpg", "https://example.com/img/premium-2.jpg"],
  "page_start_simple": "Gói hội viên cao cấp với đầy đủ quyền lợi VIP...",
  "type_payment": "monthly",
  "amount": 2980,
  "tax_item": 10,
  "charge_limit": { "limited": false, "max_charges": null },
  "trial": { "enabled": true, "days": 7 },
  "first_payment": { "enabled": true, "amount": 980 },
  "stock": { "limited": false, "quantity": null, "show_stock": false },
  "per_person_limit": { "limited": true, "max": 1, "show_limit": false },
  "actions": {
    "show_page": [
      { "id": 901, "action_id": 70, "type": "tag", "content": "タグ「Đã xem trang Premium」をつける" }
    ],
    "contract_trial": [
      { "id": 902, "action_id": 71, "type": "tag", "content": "タグ「Đang dùng thử」をつける" }
    ],
    "contract": [
      { "id": 903, "action_id": 72, "type": "scenario", "content": "ステップ「Premium Onboarding」を開始" }
    ],
    "cancel_payment": [
      { "id": 904, "action_id": 73, "type": "tag", "content": "タグ「Hội viên Premium」をはずす" },
      { "id": 905, "action_id": 73, "type": "tag", "content": "タグ「Đã hủy」をつける" }
    ],
    "purchase_1st": [
      { "id": 906, "action_id": 74, "type": "tag", "content": "タグ「Đã mua lần đầu」をつける" }
    ],
    "purchase_2nd": null,
    "buy_error": null
  },
  "stats": {
    "number_register": 88,
    "number_trial": 30,
    "number_cancel": 5,
    "number_refund": 1,
    "current_month_sales": 89400,
    "sum_sales": 786720
  },
  "created_at": "2025-09-01 09:00:00",
  "updated_at": "2026-02-15 14:30:00"
  }
]
```

---

## 3. get_product_order_history

**Description:** Tool trả về lịch sử đặt hàng của một sản phẩm, có phân trang và lọc theo thời gian — bao gồm cả đơn mua
1 lần và từng lần thanh toán của subscription — để AI phân tích doanh thu, tần suất và hành vi mua hàng.

**Tool:** `get_product_order_history`

**Input:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| bot_id | String | Yes | Bot ID hash string lấy từ tool list_bots |
| product_id | Long | Yes | ID sản phẩm lấy từ tool list_products |
| from_date | String | No | Ngày bắt đầu lọc theo payment_date (format: yyyy-MM-dd) |
| to_date | String | No | Ngày kết thúc lọc theo payment_date (format: yyyy-MM-dd) |
| page | Int | No | Số trang (default: 1) |
| limit | Int | No | Số record mỗi trang (default: 100, max: 100) |

**Output:**
| Name | Type | Description |
|------|------|-------------|
| total | Long | Tổng số record |
| page | Int | Trang hiện tại |
| limit | Int | Số record mỗi trang |
| total_pages | Int | Tổng số trang |
| orders | Json Array | Array Object Order |

**Sub Object Order:**
| Name | Type | Description |
|------|------|-------------|
| id | Long | ID đơn hàng |
| item_id | Long | ID sản phẩm |
| name_item | String | Tên sản phẩm tại thời điểm mua |
| lmessage_friend_id | Long | ID nội bộ DB của friend (`line_user.id`) |
| line_friend_id | String | LINE UID thật (`"Uxxx"`) |
| name_friend | String | Tên hiển thị của friend (null nếu chưa có) |
| amount_order | Long | Số tiền thanh toán |
| quantity_purchased | Int | Số lượng mua |
| status_order | String | Trạng thái đơn: `success` = thành công / `cancelled` = đã hủy / `bill_error` = lỗi thanh toán (`unknown` nếu giá trị khác) |
| is_trial | String | `normal` = đơn mua thường / `trial` = đơn dùng thử |
| cycle_order_id | Long | ID subscription tương ứng trong s_cycle_order_history (null nếu là đơn mua 1 lần) |
| payment_date | String | Thời điểm thanh toán (format: yyyy-MM-dd HH:mm:ss, null nếu chưa thanh toán) |
| register_date | String | Thời điểm đăng ký (format: yyyy-MM-dd HH:mm:ss, null nếu chưa có) |
| cancel_date | String | Thời điểm hủy (format: yyyy-MM-dd HH:mm:ss, null nếu chưa hủy) |
| created_at | String | Thời điểm tạo record (format: yyyy-MM-dd HH:mm:ss) |

**Sample Output:**

```json
{
  "total": 88,
  "page": 1,
  "limit": 100,
  "total_pages": 2,
  "orders": [
    {
      "id": 5001,
      "item_id": 11,
      "name_item": "Hội viên Premium",
      "lmessage_friend_id": 12345,
      "line_friend_id": "U4d5e6f708192a3b0c1d2e3f405162738",
      "name_friend": "Nguyen Van A",
      "amount_order": 980,
      "quantity_purchased": 1,
      "status_order": "success",
      "is_trial": "normal",
      "cycle_order_id": 800,
      "payment_date": "2025-09-01 10:30:00",
      "register_date": "2025-09-01 09:00:00",
      "cancel_date": null,
      "created_at": "2025-09-01 10:31:00"
    },
    {
      "id": 5002,
      "item_id": 11,
      "name_item": "Hội viên Premium",
      "lmessage_friend_id": 12345,
      "line_friend_id": "U4d5e6f708192a3b0c1d2e3f405162738",
      "name_friend": "Nguyen Van A",
      "amount_order": 2980,
      "quantity_purchased": 1,
      "status_order": "success",
      "is_trial": "normal",
      "cycle_order_id": 800,
      "payment_date": "2025-10-01 10:30:00",
      "register_date": "2025-09-01 09:00:00",
      "cancel_date": null,
      "created_at": "2025-10-01 10:31:00"
    },
    {
      "id": 5050,
      "item_id": 11,
      "name_item": "Hội viên Premium",
      "lmessage_friend_id": 67890,
      "line_friend_id": "U5e6f708192a3b4c0d1e2f30415263748",
      "name_friend": "Tran Thi B",
      "amount_order": 2980,
      "quantity_purchased": 1,
      "status_order": "cancelled",
      "is_trial": "trial",
      "cycle_order_id": 901,
      "payment_date": null,
      "register_date": "2025-11-10 08:00:00",
      "cancel_date": "2025-11-17 12:00:00",
      "created_at": "2025-11-10 08:01:00"
    }
  ]
}
```
