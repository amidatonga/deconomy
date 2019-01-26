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
from .models import Post, Category
from django.utils import timezone
from .forms import PublicationForm


class NewsList(ListView):
    model = Post
    template_name = 'news/news_list.html'
    context_object_name = 'news'
    ordering = ['-published_date']
    paginate_by = 3

    def get_context_data(self, **kwargs):
        ctx = super(NewsList, self).get_context_data(**kwargs)
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

    def get_context_data(self, **kwargs):
        ctx = super(UserNewsList, self).get_context_data(**kwargs)
        ctx['title'] = f"All articles by {self.kwargs.get('username')}"
        return ctx


class NewsPage(DetailView):
    model = Post
    template_name = 'news/news_page.html'

    def get_context_data(self, **kwargs):
        ctx = super(NewsPage, self).get_context_data(**kwargs)
        ctx['title'] = Post.objects.filter(pk=self.kwargs['pk']).first()
        return ctx


class CreateNews(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['category', 'title', 'text']

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.published_date = timezone.now()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(CreateNews, self).get_context_data(**kwargs)
        context['parent_categories'] = Category.objects.parents()
        return context


class EditNews(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'text', 'category']

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.published_date = timezone.now()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(EditNews, self).get_context_data(**kwargs)
        context['parent_categories'] = Category.objects.parents()
        return context

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


class CategoryView(ListView):
    model = Post
    template_name = 'news/category_news.html'
    context_object_name = 'news'
    paginate_by = 3

    def get_queryset(self):
        category = get_object_or_404(Category, slug=self.kwargs['slug'])
        return category.post_set.all()

    def get_context_data(self, **kwargs):
        ctx = super(CategoryView, self).get_context_data(**kwargs)
        category = get_object_or_404(Category, slug=self.kwargs['slug'])
        ctx['category'] = category
        ctx['title'] = f'Категория: {category.title}'
        return ctx


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
