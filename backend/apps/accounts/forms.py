from django.contrib.auth.forms import AdminUserCreationForm
from django.contrib.auth.forms import UserChangeForm as BaseUserChangeForm

from .models import User


class UserCreationForm(AdminUserCreationForm):
    class Meta:
        model = User
        fields = ("email", "role")


class UserChangeForm(BaseUserChangeForm):
    class Meta:
        model = User
        fields = "__all__"
