import socket

from django.conf import settings

if settings.DEBUG:

    hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
    INTERNAL_IPS = [ip[: ip.rfind('.')] + '.1' for ip in ips] + ['127.0.0.1', '10.0.2.2']  # noqa: WPS336, WPS221
