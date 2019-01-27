from django.contrib import admin
from .models import Post, Category
from users import models


class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'title', 'category')
    list_filter = ('author',)
    search_fields = ['title', 'text', 'author__username']
    prepopulated_fields = {'slug': ('title',)}

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            kwargs['queryset'] = Category.objects.filter(parent__isnull=False)
        return super(PostAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'parent')
    prepopulated_fields = {'slug': ('title',)}

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'parent':
            kwargs['queryset'] = Category.objects.parents()
        return super(CategoryAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
