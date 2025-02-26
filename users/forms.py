from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import User


class RegisterUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name','username','email','password1','password2' ]