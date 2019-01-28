from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.views.decorators.http import require_http_methods
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

    def get_context_data(self, **kwargs):
        ctx = super(NewsList, self).get_context_data(**kwargs)
        news = Post.objects.filter(published_date__isnull=False)
        ctx.update({
            'title': 'Main page',
            'news_count': len(news),
            'one_more': len(news) > Post.POSTS_ON_PAGE,
        })
        ctx['news'] = news[:Post.POSTS_ON_PAGE]
        return ctx


class UserNewsList(ListView):
    model = Post
    template_name = 'news/news_list.html'

    def get_context_data(self, **kwargs):
        ctx = super(UserNewsList, self).get_context_data(**kwargs)
        user = get_object_or_404(User, username=self.kwargs['username'])
        news = user.post_set.filter(published_date__isnull=False)
        ctx.update({
            'title': f'All articles by {self.kwargs["username"]}',
            'news_count': len(news),
            'one_more': len(news) > Post.POSTS_ON_PAGE,
            'author_username': self.kwargs['username'],
        })
        ctx['news'] = news[:Post.POSTS_ON_PAGE]
        return ctx


class NewsPage(DetailView):
    model = Post
    template_name = 'news/news_page.html'

    def get_context_data(self, **kwargs):
        ctx = super(NewsPage, self).get_context_data(**kwargs)
        post = get_object_or_404(Post, slug=self.kwargs['slug'])
        news = Post.objects.filter(category=post.category, published_date__isnull=False).exclude(id=post.id)
        ctx.update({
            'title': post,
            'news_count': len(news),
            'one_more': len(news) > Post.POSTS_ON_PAGE,
            'category': post.category,
        })
        ctx['news'] = news[:Post.POSTS_ON_PAGE]
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


class CategoryView(DetailView):
    model = Category
    template_name = 'news/news_list.html'

    def get_context_data(self, **kwargs):
        ctx = super(CategoryView, self).get_context_data(**kwargs)
        category = get_object_or_404(Category, slug=self.kwargs['slug'])
        news = category.post_set.filter(published_date__isnull=False)
        ctx.update({
            'title': f'Категория: {category.title}',
            'news_count': len(news),
            'one_more': len(news) > Post.POSTS_ON_PAGE,
            'category': category,
        })
        ctx['news'] = news[:Post.POSTS_ON_PAGE]
        return ctx


@require_http_methods(['POST', ])
def api_get_news_more(request, template_name='news/includes/posts.html'):

    post = get_object_or_404(Post, id=request.POST.get('current_news'))

    def add_query(params, q, k):
        value = request.POST.get(k)
        if value is not None:
            params[q] = value

    filter_params = {}
    add_query(filter_params, 'category__slug', 'category')
    add_query(filter_params, 'author__username', 'author')
    filter_params['published_date__lt'] = post.published_date

    news = Post.objects.filter(**filter_params)
    one_more = len(news) > Post.POSTS_ON_PAGE

    context = {
        'news': news[:Post.POSTS_ON_PAGE],
        'category': request.POST.get('category'),
        'author_username': request.POST.get('author'),
    }
    html = render_to_string(template_name, context=context)
    return JsonResponse({'html': html, 'one_more': one_more})



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
