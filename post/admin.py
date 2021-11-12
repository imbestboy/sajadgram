from django.contrib import admin

from . import models


@admin.register(models.Post)
class UserAdmin(admin.ModelAdmin):
    pass
