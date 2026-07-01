

from django.contrib.auth import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import MyUser, Profile


# Profile Form 
class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        exclude = ('user',)


# 🔹 Registration Form (IMPORTANT FIX)
class RegistrationForm(UserCreationForm):
    class Meta:
        model = MyUser
        fields = ('email', 'user_name', 'password1', 'password2')

    # optional: email unique validation
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if MyUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists")
        return email