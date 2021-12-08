import re
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.core import validators

from utilities.media import hash_media_name

from functools import partial


class UsernameValidator(validators.RegexValidator):
    regex = r"^(?=.{4,24}$)(?![_.])(?!.*[_.]{2})[a-zA-Z0-9._]+(?<![_.])$"
    message = _(
        "Enter a valid username. This value may contain only English letters, "
        "numbers, and . and _ characters."
        "NOTE : . and _ shouldn't at the beginning or end"
        "NOTE 2 : between _ and . should be characters"
        "NOTE 3 : username should be 5 to 24 characters"
    )
    flags = re.ASCII


class PhoneNumberValidator(validators.RegexValidator):
    regex = r"^(\+98|0).?9\d{9}$"
    message = _(
        "Enter a valid phone number. This value may contain only numbers or maybe +, "
        "please enter like +989127957054 or 09127957054"
    )
    flags = re.ASCII


def save_image_path(instance, file_name, is_background):
    file_name_extension = file_name.split(".")[-1]
    prefix = "background" if is_background else "profile"
    return f"{prefix}/{instance.id}/{hash_media_name(str(timezone.now()))}.{file_name_extension}"


class User(AbstractUser):
    class Gender(models.TextChoices):
        MALE = "M", "Male"
        FEMALE = "F", "Female"
        UNSET = "U", "Unset"

    email = models.EmailField(_("email address"))
    username_validator = UsernameValidator()
    username = models.CharField(
        _("username"),
        max_length=25,
        unique=True,
        help_text=_("Required. 4 - 24 characters. Letters, digits and . and _ only."),
        validators=[username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
            "invalid": _(
                "NOTE : . or _ shouldn't at the beginning or end"
                "NOTE 2 : between _ and . should be characters"
                "NOTE 3 : username should be 5 to 24 characters"
            ),
        },
    )
    last_name = models.CharField(_("last name"), max_length=15, blank=True)
    first_name = models.CharField(_("first name"), max_length=15)
    bio = models.CharField(_("biography"), max_length=150, blank=True)
    is_private = models.BooleanField(_("private account"), default=False)
    website = models.URLField(_("website"), max_length=30, blank=True)
    phone_number_validator = PhoneNumberValidator()
    phone_number = models.CharField(
        _("phone number"),
        max_length=13,
        blank=True,
        validators=[phone_number_validator],
        help_text="write your phone number like : +989127957054 or 09127957054",
    )
    is_business = models.BooleanField(_("business account"), default=False)
    is_new_google_user = models.BooleanField(_("is new google user"), default=True)
    gender = models.CharField(
        _("gender"), max_length=1, choices=Gender.choices, default=Gender.UNSET
    )
    profile_photo = models.ImageField(
        upload_to=partial(save_image_path, is_background=False),
        default="profile/default.jpeg",
    )
    background_photo = models.ImageField(
        upload_to=partial(save_image_path, is_background=True),
        default="background/default.jpeg",
    )

    @property
    def get_full_name(self):
        return super().get_full_name()


class Follow(models.Model):
    to_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="to user",
        related_name="to_user",
    )
    from_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="from user",
        related_name="from_user",
    )
    is_requested = models.BooleanField(_("is request to follow"))
    is_active = models.BooleanField(_("is followed"), default=True)
    created_time = models.DateTimeField(
        _("follow time"), auto_now=False, auto_now_add=True
    )

    def __str__(self):
        return f"{self.to_user.username} Followed by {self.from_user.username} , {self.is_active}"


class Block(models.Model):
    to_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="to user",
        related_name="to_user_block",
    )
    from_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="from user",
        related_name="from_user_block",
    )
    is_active = models.BooleanField(_("is blocked"), default=True)
    created_time = models.DateTimeField(
        _("block time"), auto_now=False, auto_now_add=True
    )

    def __str__(self):
        return f"{self.to_user.username} Blocked by {self.from_user.username} , {self.is_active}"
