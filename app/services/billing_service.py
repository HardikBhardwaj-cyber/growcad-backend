from app.models.usage_log import UsageLog
from app.services.usage_service import get_peak_usage_last_30_days


def calculate_bill(db, tenant_id: str, slab: int, plan: str):

    peak_students = get_peak_usage_last_30_days(db, tenant_id)

    price_map = {
        "basic": 15,
        "academic": 25,
        "advanced": 99
    }

    price = price_map[plan]

    # 🔥 10% buffer
    buffer = int(slab * 0.1)
    allowed = slab + buffer

    # 🔥 extra calculation
    extra_students = max(0, peak_students - allowed)

    base_amount = slab * price
    extra_amount = extra_students * price
    total_amount = base_amount + extra_amount

    return {
        "slab": slab,
        "plan": plan,
        "price_per_student": price,
        "buffer": buffer,
        "allowed_students": allowed,
        "peak_students": peak_students,
        "extra_students": extra_students,
        "base_amount": base_amount,
        "extra_amount": extra_amount,
        "total_amount": total_amount
    }