from django.contrib import admin
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'author', 'content', 'creation_date', 'updated_date']
    list_filter = ['author', 'creation_date']
    search_fields = ['author', 'content']
    ordering = ['-creation_date']