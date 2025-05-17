from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from .models import User



class RegisterUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['full_name','username','email','password1','password2']


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['avatar', 'full_name', 'username','bio']

    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar')
        if avatar and avatar.size > 20 * 1024 * 1024: 
            raise ValidationError('Avatar size must be less than 20MB.')
        return avatar
