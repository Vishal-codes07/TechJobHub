from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import CustomUser


class CustomCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    role = forms.ChoiceField(
        choices=CustomUser.ROLE_CHOICES,
        initial='seeker',
        label='I am a',
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'role']
