from django.contrib import admin
from .models import Post, Category
from users import models


class PostAdmin(admin.ModelAdmin):
    model = models.Profile
    list_display = ('author', 'title', 'category')
    list_filter = ('author',)
    search_fields = ['title', 'text']


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
