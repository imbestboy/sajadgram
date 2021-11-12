from django import forms

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
