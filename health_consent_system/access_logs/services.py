from django.utils import timezone

def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        return x_forwarded_for.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR")


def build_access_log_data(
    user,
    record,
    request,
    action="READ",
    is_emergency=False
):
    return {
        "user": user,
        "record": record,
        "action": action,
        "ip_address": get_client_ip(request),
        "is_emergency": is_emergency,
        "created_at": timezone.now()
    }
