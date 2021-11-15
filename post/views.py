from django.views import generic
from django.urls import reverse_lazy
from django.http import HttpResponse, Http404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ImproperlyConfigured

from . import forms
from . import models


@method_decorator(csrf_exempt, name="dispatch")
class DoUndoWithAjaxView(generic.View):
    model = None

    def post(self, request):
        if request.is_ajax():
            display_name = request.POST.get("display_name")
            model = self.get_model()
            try:
                do_post = model.objects.get(
                    post__display_name=display_name, user=request.user
                )
                do_post.is_active, is_do = (
                    (False, False) if do_post.is_active else (True, True)
                )
                do_post.save()
            except model.DoesNotExist:
                model.objects.create(
                    user=request.user,
                    post=models.Post.objects.get(display_name=display_name),
                )
                is_do = True

            return HttpResponse(str(is_do))
        else:
            raise Http404

    def get_model(self, model=None):
        if model:
            self.model = model
            return model
        elif self.model is None:
            raise ImproperlyConfigured(
                "%(cls)s is missing a model. Define "
                "%(cls)s.model, or override "
                "%(cls)s.get_model()." % {"cls": self.__class__.__name__}
            )
        return self.model


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


class ExploreView(generic.ListView):
    template_name = "post/explore.html"
    context_object_name = "posts"
    model = models.Post

    def get_queryset(self):
        return self.model.objects.all().order_by("?")
