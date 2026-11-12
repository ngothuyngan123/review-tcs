# Friend Stats Tools

## 1. get_friend_stats

**Description:** Tool trả về thống kê chi tiết friend của bot bao gồm tổng số friend, tổng số block, và danh sách thay
đổi hàng ngày trong 1 năm gần nhất

**Tool:** `get_friend_stats`

**Input:**
| Name | Type | Required | Description |
|--------|------|----------|-------------------------------|
| bot_id | String | Yes | Bot ID hash string lấy từ tool list_bots |

**Output:**
| Name | Type | Description |
|----------------------|------------|--------------------------------------------|
| bot_id | String | ID mã hóa (hash) của bot |
| total_friend | Int | Tổng số friend hiện tại của bot |
| total_follow_friend | Int | Tổng số friend đang follow (chưa block)    |
| total_blocked_friend | Int | Tổng số friend đã block bot |
| stats_from_date | String | Ngày bắt đầu thống kê (format: yyyy-MM-dd) |
| stats_to_date | String | Ngày kết thúc thống kê (format: yyyy-MM-dd)|
| friend_changes | Json Array | Array Object Friend Day Statistic |

**Sub Object Friend Day Statistic:**
| Name | Type | Description |
|--------------------|--------|---------------------------------------------------|
| statistic_date | String | Ngày của record (format: yyyy-MM-dd)              |
| count_user_followed | Int | Số lượng follow trong ngày |
| count_user_unfollowed| Int | Số lượng unfollow/block trong ngày |
| net_change | Int | Thay đổi net trong ngày (followed - unfollowed, dương = tăng) |
| total_friend | Long | Tổng số friend tích lũy tại cuối ngày đó |

**Sample Output:**

```json
{
  "bot_id": "abc123xyz",
  "total_friend": 15000,
  "total_follow_friend": 14200,
  "total_blocked_friend": 800,
  "stats_from_date": "2025-03-11",
  "stats_to_date": "2026-03-11",
  "friend_changes": [
    {
      "statistic_date": "2026-02-10",
      "count_user_followed": 120,
      "count_user_unfollowed": 23,
      "net_change": 97,
      "total_friend": 15000
    },
    {
      "statistic_date": "2026-02-09",
      "count_user_followed": 95,
      "count_user_unfollowed": 32,
      "net_change": 63,
      "total_friend": 14903
    },
    {
      "statistic_date": "2026-02-08",
      "count_user_followed": 150,
      "count_user_unfollowed": 15,
      "net_change": 135,
      "total_friend": 14840
    }
  ]
}
```
