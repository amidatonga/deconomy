from django.contrib import admin
from django.db import models
from .models import Profile
from .models import *


class UserProfile(admin.ModelAdmin):
    list_display=('user_id', 'user', 'fullname', 'moderator')
    search_fields=['user']
    list_filter = ('user','age',)


admin.site.register(Profile, UserProfile)
