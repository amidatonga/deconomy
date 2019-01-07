from django.shortcuts import render, get_object_or_404
from django.views.generic import (
        ListView,
        DetailView
)
from .models import Post
from django.utils import timezone


# def post_list(request):
#     posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
#     return render(request, 'news/post_list.html', {'posts': posts})

class NewsList(ListView):
    model = Post
    template_name = 'news/news_list.html'
    context_object_name = 'news'
    ordering = ['-published_date']

    def get_context_data(self, **kwards):
        ctx = super(NewsList, self).get_context_data(**kwards)
        ctx['title'] = 'Main page'
        return ctx


class NewsPage(DetailView):
    model = Post
    template_name = 'news/news_page.html'

    def get_context_data(self, **kwords):
        ctx = super(NewsPage, self).get_context_data(**kwords)
        ctx['title'] = Post.objects.filter(pk=self.kwargs['pk']).first()
        return ctx



# def post_detail(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#     return render(request, 'news/post_detail.html', {'post': post})
