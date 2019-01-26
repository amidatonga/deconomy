from django.contrib import admin
from .models import Post
from users import models



class PostAdmin(admin.ModelAdmin):
    model = models.Profile
    list_display = ('author', 'title')
    list_filter = ('author',)
    search_fields = ['title', 'text']


admin.site.register(Post, PostAdmin)
