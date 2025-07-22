from django.contrib import admin
from .models import MyUser, AuthToken


@admin.register(MyUser)
class MyUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'first_name', 'last_name', 'email', 'gender', 'is_verified']
    list_display_links = ['username', 'email']
    search_fields = ['username', 'email']
    list_filter = ['gender', 'birth_date']
    readonly_fields = ['password']

@admin.register(AuthToken)
class AuthTokenAdmin(admin.ModelAdmin):
    list_display = ['key', 'user']
    search_fields = ['user']
    list_filter = ['user']
    readonly_fields = ['key']
