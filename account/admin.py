from django.contrib import admin
from account.models import Profile, MyUser

admin.site.register(MyUser)
admin.site.register(Profile)

