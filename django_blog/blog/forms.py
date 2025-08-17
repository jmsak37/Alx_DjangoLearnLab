# blog/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class UserRegisterForm(UserCreationForm):
    """Extend Django's UserCreationForm to include an email field."""
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        # include any fields your custom user model requires (for default User use 'username')
        fields = ("username", "email", "password1", "password2")

class ProfileForm(forms.ModelForm):
    """Simple form to edit a user's profile fields (email here; extend as needed)."""
    class Meta:
        model = User
        fields = ("email",)  # add other editable fields if present (e.g. first_name)
