from django.urls import path
from django.conf.urls import url
from . import views


urlpatterns = [
    path('', views.NewsList.as_view(), name='news_list'),
    path('news/<int:pk>', views.NewsPage.as_view(), name='news_page'),
    path('news/new_publication', views.CreateNews.as_view(), name='new_post'),
    path('news/<int:pk>/edit', views.EditNews.as_view(), name='edit_post'),
    path('news/<int:pk>/delete', views.DeleteNews.as_view(), name='delete_post'),

]
