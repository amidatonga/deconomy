from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.views.generic import (
        ListView,
        DetailView,
        CreateView,
        UpdateView,
        DeleteView,
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Post
from django.utils import timezone
from .forms import PublicationForm


class NewsList(ListView):
    model = Post
    template_name = 'news/news_list.html'
    context_object_name = 'news'
    ordering = ['-published_date']
    paginate_by = 3

    def get_context_data(self, **kwards):
        ctx = super(NewsList, self).get_context_data(**kwards)
        ctx['title'] = 'Main page'
        return ctx

class UserNewsList(ListView):
    model = Post
    template_name = 'news/user_news.html'
    context_object_name = 'news'
    paginate_by = 3

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-published_date')

    def get_context_data(self, **kwards):
        ctx = super(UserNewsList, self).get_context_data(**kwards)
        ctx['title'] = f"All articles by {self.kwargs.get('username')}"
        return ctx

class NewsPage(DetailView):
    model = Post
    template_name = 'news/news_page.html'

    def get_context_data(self, **kwords):
        ctx = super(NewsPage, self).get_context_data(**kwords)
        ctx['title'] = Post.objects.filter(pk=self.kwargs['pk']).first()
        return ctx

class CreateNews(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'text']

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.published_date = timezone.now()
        return super().form_valid(form)


class EditNews(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'text']

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.published_date = timezone.now()
        return super().form_valid(form)

    def test_func(self):
        news = self.get_object()
        if self.request.user == news.author:
            return True
        return False


class DeleteNews(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        news = self.get_object()
        if self.request.user == news.author:
            return True
        return False





# def new_post(request):
#     if request.method == "POST":
#         form = PublicationForm(request.POST)
#         if form.is_valid():
#             post = form.save(commit=False)
#             post.author = request.user
#             post.published_date = timezone.now()
#             post.save()
#             return redirect('news_page', pk=post.pk)
#     else:
#         form = PublicationForm()
#     return render(request, 'news/post_edit.html', {'form': form})
#
#
# def post_edit(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#     if request.method == "POST":
#         form = PublicationForm(request.POST, instance=post)
#         if form.is_valid():
#             post = form.save(commit=False)
#             post.author = request.user
#             post.published_date = timezone.now()
#             post.save()
#             return redirect('news_page', pk=post.pk)
#     else:
#         form = PublicationForm(instance=post)
#     return render(request, 'news/post_edit.html', {'form': form })







# def post_list(request):
#     posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
#     return render(request, 'news/post_list.html', {'posts': posts})


# def post_detail(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#     return render(request, 'news/post_detail.html', {'post': post})
