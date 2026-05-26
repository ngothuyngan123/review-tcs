# 02 — Spec Reference

## Nguồn spec

| Trường | Giá trị |
|---|---|
| Tên spec | LME Broadcast Spec v2.3 |
| Link spec | https://confluence.internal/lme/broadcast-spec-v2.3 |
| Version / Last updated | v2.3 — 2026-01-15 |
| Section liên quan | 3.2 Scheduled broadcast, 3.5 Recipient resolution |

## Trích nội dung spec liên quan

### Section 3.2 — Scheduled broadcast

> A scheduled broadcast is a broadcast that is configured now but sent at a future time.
> When creating a scheduled broadcast, the user selects:
> - Target filter (tag, segment, custom query)
> - Scheduled send time (in the bot's timezone)
>
> The system **stores the filter definition**, not the resolved recipient list.
> At the scheduled time, the system **re-resolves** the filter to determine actual recipients.

### Section 3.5 — Recipient resolution

> Recipients are resolved by the following rules:
> 1. Friend must be **active** (not blocked, not unfollowed).
> 2. Friend must match **current** filter criteria (tag, segment,...).
> 3. Friend must not have opted out of the broadcast category.
>
> **The preview count at creation time is an estimate** based on current data.
> The actual recipient count at send time may differ.

## Business rules liên quan

- **BR-01**: Filter được lưu dưới dạng definition, **KHÔNG phải snapshot list friend**.
- **BR-02**: Recipient được resolve lại **tại thời điểm send**, không phải tại thời điểm create.
- **BR-03**: Friend active bao gồm: chưa block bot, chưa unfollow, chưa opt-out category.
- **BR-04**: Preview count tại create chỉ là estimate, có note "Preview only — actual count may vary".
- **BR-05**: Tag mapping table cần đồng bộ giữa `friends_tags` và `broadcast_recipients` tại thời điểm send.

## Mâu thuẫn spec ↔ bug (nếu có)

- [x] Spec đã cover case này (bug là do code sai)
- [ ] Spec CHƯA cover case này → cần update spec
- [ ] Spec cũ đang SAI → cần update spec

**Ghi chú**: Theo BR-02, broadcast phải gửi 200 friends (resolve tại send time). Bug là do code snapshot sai — đang dùng cache tag list từ lúc create, không refresh tại send.
