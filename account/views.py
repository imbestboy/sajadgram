from . import forms

from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.views import generic
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView as DjangoLoginView
from django.shortcuts import get_object_or_404

from post.models import Post


class SignupView(generic.CreateView):
    template_name = "account/signup.html"
    model = get_user_model()
    form_class = forms.SignupForm
    success_url = reverse_lazy(settings.LOGIN_URL)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(settings.LOGIN_REDIRECT_URL)
        return super().dispatch(request, *args, **kwargs)


class LoginView(DjangoLoginView):
    template_name = "account/login.html"
    form_class = forms.LoginForm
    redirect_authenticated_user = reverse_lazy(settings.LOGIN_REDIRECT_URL)


class TimeLineView(generic.TemplateView):  # ListView
    template_name = "account/timeline.html"


class ProfileView(generic.DetailView):
    template_name = "account/profile.html"
    context_object_name = "account"
    model = get_user_model()

    def get_object(self, queryset=None):
        return get_object_or_404(self.model, username=self.kwargs.get("username"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_username = self.kwargs.get("username")
        context["post_count"] = Post.objects.filter(
            user__username=current_username
        ).count()
        context["is_owner"] = current_username == self.request.user.username
        return context


class EditProfileView(generic.UpdateView):
    template_name = "account/edit-profile.html"
    form_class = forms.EditProfileForm

    def dispatch(self, *args, **kwargs):
        self.success_url = reverse_lazy(
            "account:profile", kwargs={"username": self.request.user.username}
        )
        return super().dispatch(*args, **kwargs)

    def get_object(self, queryset=None):
        return get_user_model().objects.get(username=self.request.user.username)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form(form_class=self.form_class, user=self.request.user)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_form(self, user=None, form_class=None):
        """Return an instance of the form to be used in this view."""
        if form_class is None:
            form_class = self.get_form_class()
        return form_class(**self.get_form_kwargs(), user=user)
