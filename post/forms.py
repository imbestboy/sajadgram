from django import forms
from django.core.files.images import get_image_dimensions

from . import models


class CreatePostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.change_html_attribute(
            "caption",
            {
                "placeholder": "post caption ...",
                "class": "form-control",
                "rows": 4,
            },
            forms.Textarea,
        )
        self.change_html_attribute(
            "media",
            {
                "class": "custom-file-input",
            },
            forms.FileInput,
        )

    def change_html_attribute(
        self, field_name: str, information: dict, field_type
    ) -> None:
        self.fields[field_name].widget = field_type(attrs={**information})

    class Meta:
        model = models.Post
        fields = ("caption", "media")

    def clean_media(self):
        media = self.cleaned_data.get("media")
        width, height = get_image_dimensions(media)
        if width / height != 1.0:
            self.add_error("media", "Post photo should be square")
        elif width < 300 or height < 300:
            self.add_error(
                "media",
                "Post photo too small , width and height must be greater than 299",
            )
        return media


class CommentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["text"].widget = forms.TextInput(
            attrs={
                "placeholder": "write your comment and press enter ...",
                "class": "form-control form-control-sm",
            }
        )

    class Meta:
        model = models.Comment
        fields = ("text",)
