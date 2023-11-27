from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import password_validation

from .models import Comment


class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email')
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'email': forms.TextInput(attrs={
                'class': 'form-control',
            }),
        }

    password1 = forms.CharField(
        label='Password',
        help_text=password_validation.password_validators_help_text_html(),
        widget=forms.PasswordInput(attrs={
            'class': 'form-control'
        })
    )
    password2 = forms.CharField(
        label='Password confirmation',
        help_text="Enter the same password as before, for verification.",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control'
        })
    )


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'autofocus': True,
            'class': 'form-control'
        })
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'autocomplete': 'current-password'
        })
    )


class CommentCreationForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['book', 'text', 'date']
        widgets = {
            'book': forms.TextInput(attrs={
                'class': 'form-control',
                'readonly': '',
            }),
            'text': forms.Textarea(attrs={
                'class': 'form-control',
            }),
            'date': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'readonly': '',
            }),
        }
