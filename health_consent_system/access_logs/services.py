from datetime import datetime

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR')


def build_access_log_data(
    user,
    patient,
    record,
    request,
    access_type="READ",
    is_emergency=False
):
    return {
        "user": user,
        "patient": patient,
        "record": record,
        "access_type": access_type,
        "ip_address": get_client_ip(request),
        "timestamp": datetime.now(),
        "is_emergency": is_emergency
    }
