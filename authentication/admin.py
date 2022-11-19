from django.contrib import admin

from authentication.profile import UserProfile


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'username')


admin.site.register(UserProfile, UserProfileAdmin)
