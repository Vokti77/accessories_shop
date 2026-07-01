from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import MyUser, Profile


class MyUserAdmin(UserAdmin):
    model = MyUser

    list_display = ('email', 'user_name', 'is_staff', 'is_active')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('user_name',)}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
    )

    # THIS IS THE MAIN FIX
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'user_name', 'password1', 'password2'),
        }),
    )

    search_fields = ('email',)
    ordering = ('email',)


admin.site.register(MyUser, MyUserAdmin)
admin.site.register(Profile)

