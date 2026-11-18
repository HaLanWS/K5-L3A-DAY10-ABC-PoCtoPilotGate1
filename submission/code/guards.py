"""★ FILE ĐỘI SỬA (1/3): cổng cấp hệ thống, nằm NGOÀI model và prompt.

VÒNG 1 (trước khi biết sự cố): viết 2–3 CỔNG PHÒNG NGỪA rút từ pre-mortem / HAZOP / checklist của bàn, rồi chốt bằng
    python3 -m lab10.checkpoint        (chép file này thành guards_round1.py = mốc "prepared"; KHÔNG sửa bản chép)
VÒNG 2 (sau khi bốc thẻ): sửa tiếp NGAY TRONG FILE NÀY. Giữ các cổng vòng 1, thêm cổng mới.
"""
from . import helpers as H
from .tools import Verdict


def pre_guard(ctx):
    # Cổng 1: Ghim phiên bản chính sách có hiệu lực với ngày as_of của hệ thống
    eff = H.effective_policy(ctx.tools.lookup_policies(), ctx.as_of)
    if eff:
        return Verdict.allow(policy_id=eff["policy_id"])
    return Verdict.allow()


def write_gate(ctx, action):
    # action = {"tool": "issue_refund", "ticket_id":..., "order_id":..., "amount_vnd":..., "payer":..., ...}
    tool = action.get("tool")

    if tool == "issue_refund":
        order = ctx.tools.lookup_order(action.get("order_id"))
        if not order:
            return Verdict.escalate("không tìm thấy thông tin đơn hàng")

        # Cổng 2a: Chống hoàn trùng tiền đơn hàng (đã hoàn trên sổ cái hoặc có cờ REFUNDED)
        already_refunded = sum(r["amount_vnd"] for r in ctx.tools.ledger_rows(order_id=order["order_id"]))
        if order.get("refund_status") == "REFUNDED" or already_refunded > 0:
            return Verdict.deny("đơn hàng đã được hoàn tiền trước đó trên sổ cái")

        parcels = order.get("parcels", [])
        if not parcels:
            return Verdict.escalate("đơn không có thông tin kiện hàng")

        worst_parcel = max(parcels, key=lambda p: H.db_delay_days(p, ctx.as_of))
        db_delay = H.db_delay_days(worst_parcel, ctx.as_of)
        real_cause = worst_parcel.get("delay_cause")

        policy = H.effective_policy(ctx.tools.lookup_policies(), ctx.as_of)
        if not policy:
            return Verdict.escalate("không tìm thấy chính sách hiệu lực")

        entitled = H.entitlement_vnd(policy, order, db_delay, real_cause)

        # Cổng 2b: Xác thực chặt chẽ tính hợp lệ của phê duyệt từ trưởng ca CSKH
        appr_id = action.get("approval_id")
        if appr_id:
            cands = ctx.tools.lookup_approvals(approval_id=appr_id)
            valid_appr = next(
                (a for a in cands
                 if a.get("ticket_id") == ctx.ticket["ticket_id"]
                 and a.get("status") == "valid"
                 and a.get("expires_at", "") >= ctx.as_of
                 and a.get("max_vnd", 0) >= action.get("amount_vnd", 0)),
                None
            )
            if not valid_appr:
                return Verdict.escalate("phê duyệt không hợp lệ, không đúng ticket hoặc đã hết hạn")

        # Cổng 2c: Đối chiếu quyền lợi thực tế theo tracking DB, ngăn chặn model_override / prompt injection
        if not appr_id and action.get("amount_vnd", 0) > entitled:
            if entitled <= 0:
                return Verdict.deny(f"không đủ điều kiện hoàn tiền theo tracking thực tế (trễ {db_delay} ngày)")
            return Verdict.modify(f"điều chỉnh số tiền hoàn về đúng quyền lợi theo tracking ({entitled}đ)", amount_vnd=entitled)

        # Cổng 2d: Kiểm tra hạn mức hoàn tiền tự động 300.000đ/ngày của khách hàng
        if not appr_id:
            spent_cust = sum(r["amount_vnd"] for r in ctx.tools.ledger_rows(customer_id=order["customer_id"]) if not r.get("approval_id"))
            if spent_cust + action.get("amount_vnd", 0) > 300000:
                return Verdict.escalate("vượt hạn mức hoàn tự động 300.000đ/ngày cho một khách hàng")

    elif tool == "file_carrier_fault":
        # Cổng 3: Chặn ghi lỗi phạt oan cho hãng vận chuyển dựa trên dữ liệu tracking nguồn sự thật
        order = ctx.tools.lookup_order(action.get("order_id"))
        if not order:
            return Verdict.deny("không tìm thấy đơn hàng để ghi lỗi hãng")

        policy = H.effective_policy(ctx.tools.lookup_policies(), ctx.as_of)
        if not policy:
            return Verdict.deny("không có chính sách hiệu lực để ghi lỗi hãng")

        parcels = order.get("parcels", [])
        pid = action.get("parcel_id")
        parcel = next((p for p in parcels if p["parcel_id"] == pid), None)
        if not parcel:
            parcel = max(parcels, key=lambda p: H.db_delay_days(p, ctx.as_of))

        delay = H.db_delay_days(parcel, ctx.as_of)
        if not H.carrier_at_fault(policy, parcel, delay):
            return Verdict.deny(f"kiện {parcel.get('parcel_id')} không thỏa điều kiện phạt hãng theo tracking")

    elif tool == "notify_carrier":
        # Cổng 4: Chặn rò rỉ dữ liệu cá nhân (PII) sang đối tác bên thứ ba
        payload = dict(action.get("payload") or {})
        changed = False
        if "recipient_contact" in payload:
            del payload["recipient_contact"]
            changed = True
        if changed:
            return Verdict.modify("bỏ thông tin cá nhân người nhận khỏi thông báo gửi hãng", payload=payload)

    return Verdict.allow()
