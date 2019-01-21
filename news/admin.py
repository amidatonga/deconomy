from django.contrib import admin
from .models import Post


class PostAdmin(admin.ModelAdmin):
    list_display=('author', 'title', 'created_date', 'published_date')
    list_filter = ('author',)
    search_fields=['Post__author', 'post__title']


admin.site.register(Post, PostAdmin)
