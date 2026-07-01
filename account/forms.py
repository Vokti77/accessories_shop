from django.forms import ModelForm
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from .models import MyUser
# User = get_user_model()

from account.models import Profile

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ('__all__')
        exclude = ('user', )


class RegistrationForm(UserCreationForm):
    class Meta:
        model = MyUser
        fields = ('email', 'user_name', 'password1', 'password2')