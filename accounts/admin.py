from django.contrib import admin
from .models import MyUser

@admin.register(MyUser)
class MyUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'first_name', 'last_name', 'email', 'gender', 'is_verified']
    list_display_links = ['username', 'email']
    search_fields = ['username', 'email']
    list_filter = ['gender', 'birth_date']