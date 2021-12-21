from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.contrib.auth import get_user_model

from utilities.display_name import post_display_name_maker
from utilities.media import hash_media_name


def save_post_path(instance, file_name):
    file_extension = file_name.split(".")[-1]
    return f"user/post/{instance.user.id}/{hash_media_name(str(instance.id))}z{hash_media_name(str(timezone.now()))}.{file_extension}"


class Post(models.Model):
    user = models.ForeignKey(
        get_user_model(), verbose_name=_("user's post"), on_delete=models.CASCADE
    )
    caption = models.TextField(_("post caption"), max_length=1024, blank=True)
    media = models.ImageField(_("post's media"), upload_to=save_post_path)
    created_time = models.DateTimeField(
        _("post created time"), auto_now=False, auto_now_add=True
    )
    display_name = models.CharField(
        _("post name for urls"),
        max_length=10,
        unique=True,
        default=post_display_name_maker,
    )
    updated_time = models.DateTimeField(_("post updated time"), auto_now=True)
    is_active = models.BooleanField(_("is showable"), default=True)

    def __str__(self):
        return self.display_name


class SavedPost(models.Model):
    user = models.ForeignKey(
        get_user_model(), verbose_name=_("which user saved"), on_delete=models.CASCADE
    )
    post = models.ForeignKey(
        Post, verbose_name=_("saved post"), on_delete=models.CASCADE
    )
    is_active = models.BooleanField(_("is saved"), default=True)
    created_time = models.DateTimeField(
        _("save time"), auto_now=False, auto_now_add=True
    )

    def __str__(self):
        return self.post.display_name


class LikedPost(models.Model):
    user = models.ForeignKey(
        get_user_model(), verbose_name=_("liked user"), on_delete=models.CASCADE
    )
    post = models.ForeignKey(
        Post, verbose_name=_("liked post"), on_delete=models.CASCADE
    )
    is_active = models.BooleanField(_("is liked"), default=True)
    created_time = models.DateTimeField(
        _("when user liked"), auto_now=False, auto_now_add=True
    )

    def __str__(self):
        return f"{self.user.username} Liked {self.post.display_name} , {self.is_active}"


class Comment(models.Model):
    user = models.ForeignKey(
        get_user_model(), verbose_name=_("comment writer"), on_delete=models.CASCADE
    )
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    created_time = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    parent = models.ForeignKey(
        "self", null=True, blank=True, related_name="replies", on_delete=models.CASCADE
    )

    class Meta:
        ordering = ("-created_time",)

    def __str__(self):
        return "Comment by {}".format(self.name)
