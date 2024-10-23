from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('username', 'tel', 'role', 'doctor_license', 'doctor_name')
    search_fields = ('username', 'tel', 'role')
