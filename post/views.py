from django.views import generic
from django.urls import reverse_lazy
from django.http import HttpResponse, Http404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

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

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["is_saved"] = models.SavedPost.objects.filter(
            post__display_name=self.kwargs.get("display_name"),
            user=self.request.user,
            is_active=True,
        ).exists()
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


@method_decorator(csrf_exempt, name="dispatch")
class SaveUnsaveView(generic.View):
    def post(self, request):
        if request.is_ajax():
            display_name = request.POST.get("display_name")
            try:
                saved_post = models.SavedPost.objects.get(
                    post__display_name=display_name, user=request.user
                )
                saved_post.is_active, is_saved = (
                    (False, False) if saved_post.is_active else (True, True)
                )
                saved_post.save()
            except models.SavedPost.DoesNotExist:
                models.SavedPost.objects.create(
                    user=request.user,
                    post=models.Post.objects.get(display_name=display_name),
                )
                is_saved = True

            return HttpResponse(str(is_saved))
        else:
            raise Http404
