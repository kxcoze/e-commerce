from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import User


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ('email', 'is_staff', 'is_active')
    list_filter = ('email', 'is_staff', 'is_active')
    fieldsets = (
        ('Credentials', {
            'fields': ('email', 'password')
        }),
        ('Personal Info', {
            'fields': ('username',)
        }),
        ('Permissions', {
            'fields': ('is_staff', 'is_active', 'groups', 'user_permissions')
        }),
        ('Products Preferences', {
            'classes': ('collapse',),
            'fields': ('favorites',)
        }),
    )
    add_fieldsets = (
        ('Credentials', {
            'fields': ('email', 'password1', 'password2')
        }),
        ('Personal Info', {
            'fields': ('username',)
        }),
        ('Permissions', {
            'fields': ('is_staff', 'is_active', 'groups', 'user_permissions')
        }),
        ('Products Preferences', {
            'classes': ('collapse',),
            'fields': ('favorites',)
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)


admin.site.register(User, CustomUserAdmin)