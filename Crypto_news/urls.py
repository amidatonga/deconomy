
from django.contrib import admin
from django.urls import path, include
from users import views as userViews


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('news.urls')),
    path('reg/', userViews.register, name='reg' )
]
