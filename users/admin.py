from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User,UserOtp

class CustomUserAdmin(UserAdmin):
    list_display = ('mobile_number', 'email', 'is_active', 'is_staff')
    list_filter = ('is_active', 'is_staff')
    fieldsets = (
        (None, {'fields': ('mobile_number', 'password')}),
        ('Personal Info', {'fields': ('email',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('mobile_number', 'password1', 'password2'),
        }),
    )
    ordering = ('mobile_number',)
    search_fields = ('mobile_number', 'email')
    filter_horizontal = ()

# Register the custom User model with the custom admin class
admin.site.register(User, CustomUserAdmin)


@admin.register(UserOtp)
class UserOtpAdmin(admin.ModelAdmin):
    list_display = ('user', 'otp', 'is_verified', 'created_at')
    list_filter = ('is_verified', 'created_at')
    search_fields = ('user__mobile_number', 'otp')
