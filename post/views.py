from django.contrib.auth import get_user_model
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin

from account.models import Block, Follow
from utilities.views import DoUndoWithAjaxView
from . import forms
from . import models


class CreatePostView(SuccessMessageMixin, generic.CreateView):
    success_url = reverse_lazy("account:timeline")
    template_name = "post/create.html"
    form_class = forms.CreatePostForm
    model = models.Post
    success_message = "your post has been created successfully"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class SavedPostListView(generic.ListView):
    paginate_by = 30
    template_name = "post/saved-list.html"
    context_object_name = "posts"
    model = models.Post

    def get_queryset(self):
        return models.SavedPost.objects.filter(user=self.request.user, is_active=True)


class LikedPostListView(generic.ListView):
    paginate_by = 30
    template_name = "post/liked-list.html"
    context_object_name = "posts"
    model = models.Post

    def get_queryset(self):
        return models.LikedPost.objects.filter(user=self.request.user, is_active=True)


class ShowPostView(SuccessMessageMixin, generic.DetailView, generic.CreateView):
    form_class = forms.CommentForm
    success_message = "Comment successfully sended"
    template_name = "post/show.html"
    model = models.Post
    context_object_name = "post"

    def get_success_url(self):
        return reverse_lazy(
            "post:show", kwargs={"display_name": self.kwargs.get("display_name")}
        )

    def get_object(self):
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
        context["comments"] = self.object.comments.filter(
            is_active=True, parent__isnull=True
        )
        return context

    def form_valid(self, form):
        parent_obj = None
        try:
            parent_id = int(self.request.POST.get("parent_id"))
            parent_obj = models.Comment.objects.get(id=parent_id)
            replay_comment = form.save(commit=False)
            replay_comment.parent = parent_obj
        except (TypeError, models.Comment.DoesNotExist):
            parent_id = None

        new_comment = form.save(commit=False)
        new_comment.post = self.get_object()
        new_comment.user = self.request.user
        new_comment.save()
        return super().form_valid(form)


class UserPostList(generic.ListView):
    template_name = "post/user-posts.html"
    context_object_name = "posts"
    model = models.Post

    def get_queryset(self):
        user = get_user_model().objects.get(username=self.kwargs.get("username"))
        all_posts = models.Post.objects.filter(user=user)
        if not user.is_private:
            return all_posts
        else:
            if Follow.objects.filter(
                from_user=self.request.user,
                to_user=user,
                is_active=True,
                status=2,
            ):
                return all_posts
        return []

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["current_username"] = self.kwargs.get("username")
        return context


class SaveUnsaveView(DoUndoWithAjaxView):
    model = models.SavedPost

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
        return (
            self.model.objects.all()
            .filter(user__is_private=False)
            .exclude(user__in=blocked_users)
            .order_by("?")
        )
