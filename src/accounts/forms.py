from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "phone_number",
            "city",
            "monthly_budget",
            "profile_avatar",
            "password1",
            "password2",
        )


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("city", "monthly_budget", "profile_avatar")
