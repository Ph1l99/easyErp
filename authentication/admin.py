from django.contrib import admin

from authentication.profile import UserProfile
from authentication.user import User


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'username', 'is_approved')


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'is_active', 'is_superuser', 'last_login')


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(User, UserAdmin)
