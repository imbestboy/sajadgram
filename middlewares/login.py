from django.conf import settings
from django.contrib.auth.views import redirect_to_login
from django.urls import reverse


class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_view(self, request, *args, **kwargs):
        if not request.user.is_authenticated and request.path not in map(
            reverse, settings.LOGIN_EXEMPT_URLS
        ):
            return redirect_to_login(request.path)
