from django.views import generic
from django.urls import reverse_lazy

from account.models import Block
from utilities.views import DoUndoWithAjaxView
from . import forms
from . import models


class CreatePostView(generic.CreateView):
    success_url = reverse_lazy("account:timeline")
    template_name = "post/create.html"
    form_class = forms.CreatePostForm
    model = models.Post

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class SavedPostListView(generic.ListView):
    paginate = 30
    template_name = "post/saved-list.html"
    context_object_name = "posts"
    model = models.Post

    def get_queryset(self):
        return models.SavedPost.objects.filter(user=self.request.user, is_active=True)


class LikedPostListView(generic.ListView):
    paginate = 30
    template_name = "post/liked-list.html"
    context_object_name = "posts"
    model = models.Post

    def get_queryset(self):
        return models.LikedPost.objects.filter(user=self.request.user, is_active=True)


class ShowPostView(generic.DetailView):
    template_name = "post/show.html"
    model = models.Post
    context_object_name = "post"

    def get_object(self, *args, **kwargs):
        return models.Post.objects.get(display_name=self.kwargs.get("display_name"))

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        display_name = self.kwargs.get("display_name")
        context["is_saved"] = models.SavedPost.objects.filter(
            post__display_name=display_name,
            user=self.request.user,
            is_active=True,
        ).exists()
        context["is_liked"] = models.LikedPost.objects.filter(
            post__display_name=display_name,
            user=self.request.user,
            is_active=True,
        ).exists()
        context["liked_count"] = models.LikedPost.objects.filter(
            post__display_name=display_name, is_active=True
        ).count()
        return context


class UserPostList(generic.ListView):
    template_name = "post/user-posts.html"
    context_object_name = "posts"
    model = models.Post

    def get_queryset(self):
        return models.Post.objects.filter(user__username=self.kwargs.get("username"))

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["current_username"] = self.kwargs.get("username")
        return context


class SaveUnsaveView(DoUndoWithAjaxView):
    model = models.SavedPost


class LikeUnlikeView(DoUndoWithAjaxView):
    model = models.LikedPost

    def get_check_dict(self):
        return {
            "post__display_name": self.request.POST.get("display_name"),
            "user": self.request.user,
        }

    def get_create_dict(self):
        return {
            "user": self.request.user,
            "post": models.Post.objects.get(
                display_name=self.request.POST.get("display_name")
            ),
        }


class ExploreView(generic.ListView):
    template_name = "post/explore.html"
    context_object_name = "posts"
    model = models.Post

    def get_queryset(self):
        blocked_users = (
            blocked_user.to_user
            for blocked_user in Block.objects.filter(
                from_user=self.request.user, is_active=True
            )
        )
        return self.model.objects.all().exclude(user__in=blocked_users).order_by("?")
