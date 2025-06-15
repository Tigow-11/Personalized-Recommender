from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

# 🔷 Register Form
class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']


# 🔷 Setup Profile Form
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['level', 'interests', 'goals', 'learning_topics']
        widgets = {
            'interests': forms.Textarea(attrs={'rows': 2}),
            'goals': forms.Textarea(attrs={'rows': 2}),
            'learning_topics': forms.Textarea(attrs={'rows': 2}),
        }