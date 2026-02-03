from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import SignUpForm, ProfileUpdateForm
from .models import User


class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = "accounts/signup.html"
    success_url = reverse_lazy("login")


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileUpdateForm
    template_name = "accounts/profile_edit.html"
    success_url = reverse_lazy("expenses:list")

    def get_object(self):
        return self.request.user
