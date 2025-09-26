# middlewares.py
from django.conf import settings


class AdminSessionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith("/admin/"):
            settings.SESSION_COOKIE_NAME = getattr(settings, "ADMIN_SESSION_COOKIE_NAME", "addmin_sessionid")
        else:
            settings.SESSION_COOKIE_NAME = "sessionid"
        return self.get_response(request)