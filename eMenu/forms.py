import django.forms as forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import validate_email


class LoginForm(forms.Form):
    login = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)


def login_validator(login):
    users = User.objects.all().values_list("username", flat=True)
    if login in users:
        raise ValidationError(f"{login} jest juz zajete")


class AddUserForm(forms.Form):
    login = forms.CharField(validators=[login_validator], label="login")
    password = forms.CharField(widget=forms.PasswordInput, label="password")
    password2 = forms.CharField(widget=forms.PasswordInput, label="repeat password")
    name = forms.CharField(label="name")
    surname = forms.CharField(label="surname")
    email = forms.EmailField(label="email")

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data["password"] != cleaned_data["password2"]:
            raise ValidationError("hasla nie sa takie same")