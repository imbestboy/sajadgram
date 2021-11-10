from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import get_user_model
from django import forms
from django.utils.translation import gettext_lazy as _


class SignupForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.change_html_attribute(
            "username",
            {"placeholder": "Username", "class": "form-control"},
            forms.TextInput,
        )
        self.change_html_attribute(
            "password1",
            {"placeholder": "Your Password", "class": "form-control"},
            forms.PasswordInput,
        )
        self.change_html_attribute(
            "password2",
            {"placeholder": "Confirmation Password", "class": "form-control"},
            forms.PasswordInput,
        )

    def change_html_attribute(
        self, field_name: str, information: dict, field_type
    ) -> None:
        self.fields[field_name].widget = field_type(attrs={**information})

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if len(username) < 4:
            self.add_error("username", "username is too short")
        return username

    class Meta(UserCreationForm.Meta):
        model = get_user_model()


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget = forms.TextInput(
            attrs={"placeholder": "Username", "class": "form-control"}
        )
        self.fields["password"].widget = forms.PasswordInput(
            attrs={"placeholder": "Your Password", "class": "form-control"}
        )


class EditProfileForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self.fields["date_joined"].disabled = True
        self.fields["username"].disabled = True
        self.change_html_attribute(
            "username",
            {"class": "form-control"},
            forms.TextInput,
        )
        self.change_html_attribute(
            "email",
            {"placeholder": "sajadgram@gmail.com", "class": "form-control"},
            forms.TextInput,
        )
        self.change_html_attribute(
            "password",
            {"placeholder": "Password", "class": "form-control"},
            forms.PasswordInput,
        )

        self.change_html_attribute(
            "date_joined",
            {
                "class": "form-control datetimepicker-input",
                "data-target": "#reservationdate",
            },
            forms.DateInput,
        )
        self.change_html_attribute(
            "last_name",
            {"placeholder": "mohammadi", "class": "form-control"},
            forms.TextInput,
        )
        self.change_html_attribute(
            "first_name",
            {"placeholder": "mohammad", "class": "form-control"},
            forms.TextInput,
        )
        self.change_html_attribute(
            "bio",
            {
                "placeholder": "tell something about yourself ...",
                "class": "form-control",
                "rows": 3,
            },
            forms.Textarea,
        )
        self.change_html_attribute(
            "website",
            {"placeholder": "https://adminlte.io", "class": "form-control"},
            forms.TextInput,
        )
        self.change_html_attribute(
            "phone_number",
            {"placeholder": "+989127957054", "class": "form-control"},
            forms.TextInput,
        )
        self.change_html_attribute(
            "profile_photo",
            {
                "class": "custom-file-input",
                "class": "custom-file-input",
                "id": "exampleInputFile",
            },
            forms.FileInput,
        )
        self.change_html_attribute(
            "background_photo",
            {
                "class": "custom-file-input",
                "class": "custom-file-input",
                "id": "exampleInputFile",
            },
            forms.FileInput,
        )

        self.change_html_attribute(
            "is_private",
            {"class": "form-check-label"},
            forms.CheckboxInput,
        )
        self.change_html_attribute(
            "is_business",
            {"class": "form-check-label"},
            forms.CheckboxInput,
        )

    def change_html_attribute(
        self, field_name: str, information: dict, field_type
    ) -> None:
        if self.errors.get(field_name, False):
            information["class"] = (
                information["class"] + " is-invalid"
                if "class" in information
                else "is-invalid"
            )
        self.fields[field_name].widget = field_type(attrs={**information})

    class Meta:
        model = get_user_model()
        exclude = (
            "last_login",
            "is_superuser",
            "groups",
            "user_permissions",
            "is_staff",
            "is_active",
        )

    def clean(self):
        self.cleaned_data = super().clean()
        is_private = self.cleaned_data.get("is_private")
        is_business = self.cleaned_data.get("is_business")
        if is_private and is_business:
            self.add_error(
                None, "Your profile can't be private and business in same time"
            )

    def clean_password(self):
        password = self.cleaned_data.pop("password")
        if not self.user.check_password(password):
            self.add_error("password", "your password is incorrect")
        return password

    def save(self):
        instance = super().save(commit=False)
        dont_update_fields = ("password", "username", "date_joined")
        for dont_update_field in dont_update_fields:
            self.cleaned_data.pop(dont_update_field, None)
        instance.save(update_fields=self.cleaned_data.keys())
        return instance
