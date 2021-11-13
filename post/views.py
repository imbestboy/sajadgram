from django.views import generic
from django.urls import reverse_lazy

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
    template_name = "post/saved-list.html"
    context_object_name = "posts"
    model = models.Post

    # TODO: implement save post model and modify get_queryset
    def get_queryset(self):
        pass


class LikedPostListView(generic.ListView):
    template_name = "post/liked-list.html"
    context_object_name = "posts"
    model = models.Post

    # TODO: implement like post model and modify get_queryset
    def get_queryset(self):
        pass


class ShowPostView(generic.DetailView):
    template_name = "post/show.html"
    model = models.Post
    context_object_name = "post"

    def get_object(self, *args, **kwargs):
        return models.Post.objects.get(display_name=self.kwargs.get("display_name"))


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
