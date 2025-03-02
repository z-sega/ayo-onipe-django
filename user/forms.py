"""User forms."""

from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import User


class UserCreationForm(UserCreationForm):
    """Create User Form."""

    class Meta:
        """Metadata about User Creation Form."""

        model = User
        fields = ("email",)


class UserChangeForm(UserChangeForm):
    """Change User Form."""

    class Meta:
        """Metadata about User Change Form."""

        model = User
        fields = ("email",)
