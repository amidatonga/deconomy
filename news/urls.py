from django.urls import path
from . import views


urlpatterns = [
    path('api/news/more', views.api_get_news_more, name='api_news_more'),

    path('', views.NewsList.as_view(), name='news_list'),
    path('user/<str:username>', views.UserNewsList.as_view(), name='user_news'),
    path('news/new_publication', views.CreateNews.as_view(), name='new_post'),
    path('news/<slug:slug>', views.NewsPage.as_view(), name='news_page'),
    path('news/<slug:slug>/edit', views.EditNews.as_view(), name='edit_post'),
    path('news/<slug:slug>/delete', views.DeleteNews.as_view(), name='delete_post'),
    path('category/<slug:slug>', views.CategoryView.as_view(), name='category_news'),

]
