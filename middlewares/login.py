from django.conf import settings
from django.contrib.auth.views import redirect_to_login
from django.urls import reverse
from django.urls.exceptions import NoReverseMatch
from django.shortcuts import redirect


class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def get_exempt_urls(self, view_kwargs):
        urls = []
        for url in settings.LOGIN_EXEMPT_URLS:
            try:
                if view_kwargs:
                    urls += [reverse(url, kwargs=view_kwargs)]
                else:
                    urls += [reverse(url)]
            except NoReverseMatch:
                pass
        return urls

    def process_view(self, request, _, __, view_kwargs=None):
        if (
            not request.user.is_authenticated
            and request.path not in self.get_exempt_urls(view_kwargs)
        ):
            return redirect_to_login(request.path)
        elif (
            request.user.is_authenticated
            and request.user.is_new_google_user
            and request.path != "/finalize-signup/"
        ):
            return redirect("account:finalize-signup")
