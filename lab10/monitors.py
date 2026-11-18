"""★ FILE ĐỘI SỬA (2/3): chỉ số theo dõi (monitor). Thêm ÍT NHẤT MỘT chỉ số bắt được sự cố của bàn.

Mỗi monitor nhận danh sách trial (KHÔNG có nhãn đúng/sai, giống production) và trả về một số.
Một trial = {"ticket_id", "seed", "day", "status", "amount_vnd", "ticket", "events", "ledger", "faults", "outbound",
             "arrive_min", "warehouse", "cost_vnd", "review_kind", "queue_wait_min", "queue_stuck"}
"""


def escalation_rate(trials):
    return sum(t["status"] == "escalated" for t in trials) / max(1, len(trials))


def model_override_rate(trials):
    """Tỉ lệ ticket mà model đè số ngày khách tự khai lên DB tracking."""
    overrides = 0
    for t in trials:
        events = t.get("events") or []
        if any(e.get("type") == "model_override" for e in events):
            overrides += 1
    return overrides / max(1, len(trials))


def carrier_strike_rate(trials):
    """Tỉ lệ ticket có ghi lỗi phạt hãng vận chuyển."""
    faults = sum(len(t.get("faults") or []) for t in trials)
    return faults / max(1, len(trials))


def blocked_write_rate(trials):
    """Tỉ lệ ticket có lệnh ghi bị cổng guard chặn (deny) hoặc điều chỉnh (modify)."""
    blocked = 0
    for t in trials:
        events = t.get("events") or []
        if any(e.get("type") == "gate" and e.get("action") in ("deny", "modify") for e in events):
            blocked += 1
    return blocked / max(1, len(trials))


MONITORS = {
    "escalation_rate": escalation_rate,
    "model_override_rate": model_override_rate,
    "carrier_strike_rate": carrier_strike_rate,
    "blocked_write_rate": blocked_write_rate,
}
STARTER_MONITORS = ("escalation_rate",)
