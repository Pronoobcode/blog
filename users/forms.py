from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import User


class RegisterUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['full_name','username','email','password1','password2']


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['avatar', 'full_name', 'username', 'email', 'bio']