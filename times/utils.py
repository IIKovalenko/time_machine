from datetime import datetime
from django.conf import settings
from django.utils.timezone import utc


def get_datetime_from_request(get_param_slug, request):
    raw_value = request.GET.get(get_param_slug, None)
    if raw_value:
        return datetime.strptime(raw_value, settings.TIME_FORMAT).replace(tzinfo=utc)
