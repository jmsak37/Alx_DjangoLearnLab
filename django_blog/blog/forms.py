# blog/forms.py
from django import forms
from .models import Comment
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import Post
User = get_user_model()

class PostForm(forms.ModelForm):
    """Form to create and edit Post objects."""
    class Meta:
        model = Post
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Post title'}),
            'content': forms.Textarea(attrs={'rows': 10}),
        }

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

class CommentForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={'rows': 4}), label='')

    class Meta:
        model = Comment
        fields = ['content']
