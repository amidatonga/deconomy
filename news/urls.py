from django.urls import path
from . import views


urlpatterns = [
    path('api/news/more', views.api_get_news_more, name='api_news_more'),
    path('api/full_news/more', views.api_get_full_news_more, name='api_full_news_more'),

    path('', views.NewsList.as_view(), name='news_list'),
    path('news/drafts', views.DraftsList.as_view(), name='drafts_list'),
    path('news/hots', views.HotNews.as_view(), name='hot_news'),

    path('authors/<str:username>', views.UserNewsList.as_view(), name='user_news'),
    path('user/drafts/<str:username>', views.UserDraftList.as_view(), name='user_drafts'),

    path('news/new_publication', views.CreateNews.as_view(), name='new_post'),

    path('news/drafts/<slug:slug>', views.DraftPage.as_view(), name='draft_page'),
    path('news/publish/<slug:slug>', views.publish_post, name='publish_post'),
    path('news/<slug:slug>', views.NewsPage.as_view(), name='news_page'),


    path('news/<slug:slug>/edit', views.EditNews.as_view(), name='edit_post'),
    path('news/<slug:slug>/delete', views.DeleteNews.as_view(), name='delete_post'),
    path('category/<slug:slug>', views.CategoryView.as_view(), name='category_news'),
    path('tag/<slug:slug>', views.TagNewsList.as_view(), name='tag_news'),

]
