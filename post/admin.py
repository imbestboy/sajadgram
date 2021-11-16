from django.contrib import admin

from . import models


@admin.register(models.Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("user", "display_name", "created_time", "is_active")


@admin.register(models.SavedPost)
class SavePostAdmin(admin.ModelAdmin):
    list_display = ("username", "display_name", "created_time", "is_active")

    @admin.display()
    def username(self, obj):
        return obj.user.username

    @admin.display()
    def display_name(self, obj):
        return obj.post.display_name


@admin.register(models.LikedPost)
class SavePostAdmin(admin.ModelAdmin):
    list_display = ("username", "display_name", "created_time", "is_active")

    @admin.display()
    def username(self, obj):
        return obj.user.username

    @admin.display()
    def display_name(self, obj):
        return obj.post.display_name
