from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.views import generic
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView as DjangoLoginView
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.contrib.auth import login

from . import forms
from . import models
from post.models import Post
from utilities.views import DoUndoWithAjaxView


class SignupView(generic.CreateView):
    template_name = "account/signup.html"
    model = get_user_model()
    form_class = forms.SignupForm
    success_url = reverse_lazy(settings.LOGIN_URL)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(settings.LOGIN_REDIRECT_URL)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.is_new_google_user = False
        return super().form_valid(form)


class LoginView(DjangoLoginView):
    template_name = "account/login.html"
    form_class = forms.LoginForm
    redirect_authenticated_user = reverse_lazy(settings.LOGIN_REDIRECT_URL)


class TimeLineView(generic.ListView):
    template_name = "account/timeline.html"
    context_object_name = "posts"
    model = Post

    def queryset(self):
        followed_users = (
            followed_user.to_user
            for followed_user in models.Follow.objects.filter(
                from_user=self.request.user, is_active=True
            )
        )
        return Post.objects.filter(user__in=followed_users).order_by("created_time")


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
        context["following_count"] = models.Follow.objects.filter(
            from_user__username=current_username, is_active=True
        ).count()
        context["follower_count"] = models.Follow.objects.filter(
            to_user__username=current_username, is_active=True
        ).count()
        context["is_block"] = models.Block.objects.filter(
            from_user=self.request.user,
            to_user__username=current_username,
            is_active=True,
        ).exists()
        if current_username != self.request.user.username:
            context["is_followed"] = models.Follow.objects.filter(
                to_user__username=current_username,
                from_user=self.request.user,
                is_active=True,
            ).exists()
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


class FollowUnfollowView(DoUndoWithAjaxView):
    model = models.Follow
    permission_denied_message = "You cant follow your self !"

    def get_check_dict(self):
        current_username = self.request.POST.get("username")
        if self.request.user.username == current_username:
            raise PermissionDenied(self.permission_denied_message)
        return {"from_user": self.request.user, "to_user__username": current_username}

    def get_create_dict(self):
        return {
            "from_user": self.request.user,
            "to_user": get_user_model().objects.get(
                username=self.request.POST.get("username")
            ),
        }


class BlockUnblockView(FollowUnfollowView):
    model = models.Block
    permission_denied_message = "You cant block your self !"

    def post(self, *args, **kwargs):
        super_post = super().post(*args, **kwargs)
        self.unfollow_when_block(super_post.content.decode("utf-8"))
        return super_post

    def unfollow_when_block(self, is_blocked):
        if is_blocked == "True":
            try:
                followed = models.Follow.objects.get(
                    from_user=self.request.user,
                    to_user__username=self.request.POST.get("username"),
                    is_active=True,
                )
                followed.is_active = False
                followed.save()
                followed = models.Follow.objects.get(
                    from_user__username=self.request.POST.get("username"),
                    to_user=self.request.user,
                    is_active=True,
                )
                followed.is_active = False
                followed.save()
            except models.Follow.DoesNotExist:
                pass


class SearchView(generic.ListView):
    paginate_by = 15
    template_name = "account/search.html"
    model = get_user_model()
    context_object_name = "accounts"

    def get_queryset(self):
        search = self.request.GET.get("q", None)
        blocked_users_username = (
            blocked_user.to_user.username
            for blocked_user in models.Block.objects.filter(
                from_user=self.request.user, is_active=True
            )
        )
        return (
            (
                get_user_model()
                .objects.filter(
                    Q(username__contains=search)
                    | Q(first_name__contains=search)
                    | Q(last_name__contains=search)
                )
                .exclude(username__in=blocked_users_username)
            )
            if search
            else []
        )


class FollowersListView(generic.ListView):
    template_name = "account/following-follower-list.html"
    paginate_by = 15
    context_object_name = "accounts"
    model = models.Follow

    def get_queryset(self):
        return self.model.objects.filter(
            to_user__username=self.kwargs.get("username"), is_active=True
        )

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["follower_or_following"] = "Followers"
        context["current_username"] = self.kwargs.get("username")
        return context


class FollowingsListView(generic.ListView):
    template_name = "account/following-follower-list.html"
    paginate_by = 15
    context_object_name = "accounts"
    model = models.Follow

    def get_queryset(self):
        return self.model.objects.filter(
            from_user__username=self.kwargs.get("username"), is_active=True
        )

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["follower_or_following"] = "Followings"
        context["current_username"] = self.kwargs.get("username")
        return context


class FinalizeSignupView(generic.UpdateView):
    success_url = reverse_lazy("account:timeline")
    form_class = forms.SignupForm
    template_name = "account/finalize-signup.html"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_new_google_user:
            return redirect("account:timeline")
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        form.instance.is_new_google_user = False
        valid_form = super().form_valid(form)
        self.request.user.backend = "django.contrib.auth.backends.ModelBackend"
        login(self.request, self.request.user)
        return valid_form
