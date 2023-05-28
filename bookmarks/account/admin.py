from django.contrib import admin
from .models import Profile


class ProfileAdmin(admin.ModelAdmin):
    class Meta:
        model = Profile
    list_display = ['username', 'email', 'is_active', 'is_staff']


admin.site.register(Profile, ProfileAdmin)
