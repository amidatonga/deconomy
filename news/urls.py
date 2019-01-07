from django.urls import path
from django.conf.urls import url
from . import views


urlpatterns = [
    path('', views.NewsList.as_view(), name='news_list'),
    path('news/<int:pk>', views.NewsPage.as_view(), name='news_page'),

]
