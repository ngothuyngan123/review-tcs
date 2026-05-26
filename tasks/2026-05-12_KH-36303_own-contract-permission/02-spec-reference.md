# 02 — Spec Reference

> **Spec reference**: Không có spec riêng cho task này. Fallback tham chiếu [LME-SYSTEM-SPEC.md](../../templates/LME-SYSTEM-SPEC.md) — phần **Quản lý hợp đồng / Phân quyền staff**.

## Điểm liên quan trong LME-SYSTEM-SPEC

- **Permission model**: LME có 2 cấp quyền — Owner (chủ bot/contract) vs Staff (được mời, có role giới hạn). Quyền được check theo **bot đang select**.
- **Contract types**: Free / Standard / Pro / Enterprise. Mỗi contract gắn với 1 bot HOẶC chưa connect bot (slot trống).
- **Bot context**: User có thể là owner của nhiều bot + staff của nhiều bot khác. UI có dropdown chuyển bot → permission được resolve theo bot đang select.

## Spec gap / mâu thuẫn

- **Spec hiện không nói rõ** logic permission khi user vào contract **của chính mình** (ownership) từ context của bot khác mà user đang làm staff. Đây là root cause của bug 36303.
- Fix (mục 2 của dev impact) introduce rule mới: **nếu contract là của chính user đang login (ownership check) → bỏ qua check quyền bot**. → Cần spec update.

## Spec update needed

- [ ] **Cần update spec** — section "Quản lý hợp đồng → Phân quyền access detail contract":
  - Thêm rule: "Khi user vào màn detail contract, ưu tiên check **ownership** trước. Nếu user là **owner của contract** → bỏ qua check quyền bot (role-based). Chỉ check quyền bot nếu user KHÔNG phải owner."
  - Ghi rõ scope rule này áp dụng cho các thao tác: view detail / change card / change payment method / change bill type / update-delete sub card / hủy contract.
