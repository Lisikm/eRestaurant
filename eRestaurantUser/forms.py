import string

import django.forms as forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class LoginForm(forms.Form):
    login = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)


def login_validator(login):
    users = User.objects.all().values_list("username", flat=True)
    if login in users:
        raise ValidationError("Login already exists")


def password_validator(password):
    num = False
    ss = False
    for dig in password:
        if dig in string.digits:
            num = True
        elif dig in string.punctuation:
            ss = True
    if len(password) < 8:
        raise ValidationError("Password must be at least 8 characters long.")
    if password.islower():
        raise ValidationError("Password must contain at least 1 lowercase letter")
    if password.isupper():
        raise ValidationError("Password must contain at least 1 uppercase letter")
    if num == False:
        raise ValidationError("Password must contain at least 1 number")
    if ss == False:
        raise ValidationError("Password must contain at least 1 special character")


class AddUserForm(forms.Form):
    login = forms.CharField(validators=[login_validator], label="login")
    password = forms.CharField(widget=forms.PasswordInput, label="password")
    password2 = forms.CharField(widget=forms.PasswordInput, label="repeat password")
    name = forms.CharField(label="name")
    surname = forms.CharField(label="surname")
    email = forms.EmailField(label="email")

    def clean(self):
        cleaned_data = super().clean()
        password_validator(cleaned_data["password"])
        if cleaned_data["password"] != cleaned_data["password2"]:
            raise ValidationError("Passwords do not match.")
