from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.conf import settings
from useraccount.models import User

class UserRegisterForm(UserCreationForm):
    class Meta:
        model=User
        fields=["username","email","password1","password2"]