from django.forms import ModelForm
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from .models import MyUser
import sys
# User = get_user_model()

from account.models import Profile

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ('__all__')
        exclude = ('user', )


class RegistrationForm(UserCreationForm):

    email = forms.EmailField(max_length=254, help_text='Required. Add a valid email address.')

    class Meta:
        model = MyUser
        fields = ('email', 'user_name', 'password1', 'password2', )

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        try:
            account = MyUser.objects.exclude(pk=self.instance.pk).get(email=email)
        except MyUser.DoesNotExist:
            return email
        raise forms.ValidationError('Email "%s" is already in use.' % account)

    def clean_username(self):
        user_name = self.cleaned_data['user_name']
        try:
            account = MyUser.objects.exclude(pk=self.instance.pk).get(user_name=user_name)
        except MyUser.DoesNotExist:
            return user_name
        raise forms.ValidationError('Username "%s" is already in use.' % user_name)

    # class Meta:
    #     model = MyUser
    #     fields = ('email', 'user_name', 'password1', 'password2')