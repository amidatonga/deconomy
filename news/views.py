from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.conf import settings
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.views.generic import (
        ListView,
        DetailView,
        CreateView,
        UpdateView,
        DeleteView,
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Post, Category, Tag
from django.utils import timezone
from .forms import PublicationForm
from users.models import Profile


def update_news_ctx(ctx, request, news, hot=None):
    query = request.GET.get('query')
    if query is not None:
        qs = Q(title__icontains=query) | Q(text__icontains=query)
        news = news.filter(qs)
    ctx.update({
        'news_count': len(news),
        'one_more': len(news) > Post.POSTS_ON_PAGE,
        'query': query,
    })
    ctx['news'] = news[:Post.POSTS_ON_PAGE]
    if hot is not None:
        ctx['hotnews'] = Post.get_hot_news(count=hot)
    return ctx

def view_post(request, post):
    if 'post__viewed' not in request.session:
        request.session['post__viewed'] = []
    if post.id not in request.session['post__viewed']:
        request.session['post__viewed'].append(post.id)
        request.session.save()
        post.view()

def publish_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    post.publish()
    return redirect('news_page', slug=post.slug)



class NewsList(ListView):
    model = Post
    template_name = 'news/news_list.html'

    def get_context_data(self, **kwargs):
        ctx = super(NewsList, self).get_context_data(**kwargs)
        news = Post.objects.filter(published_date__isnull=False)
        update_news_ctx(ctx, self.request, news, hot=settings.SIDEBAR_POST_COUNT)
        ctx.update({
            'title': 'Deconomy - Digital Economy and Cryptocurrencies',
        })
        return ctx

class HotNews(ListView):
    model = Post
    template_name = 'news/includes/main_sidebar.html'

    def get_context_data(self, **kwargs):
        ctx = super(HotNews, self).get_context_data(**kwargs)
        hotnews = Post.get_hot_news(count=6)
        ctx.update({
            'title': 'Deconomy - Digital Economy and Cryptocurrencies',
            'hotnews': hotnews,
        })
        return ctx

class DraftsList(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'news/news_list_drafts.html'

    def get_context_data(self, **kwargs):
        ctx = super(DraftsList, self).get_context_data(**kwargs)
        news = Post.objects.filter(published_date__isnull=True).order_by('-created_date')
        update_news_ctx(ctx, self.request, news)
        ctx.update({
            'title': 'Drafts',
        })
        return ctx

class UserNewsList(ListView):
    model = Post
    template_name = 'news/news_list_sorted.html'

    def get_context_data(self, **kwargs):
        ctx = super(UserNewsList, self).get_context_data(**kwargs)
        user = get_object_or_404(User, username=self.kwargs['username'])
        news = user.post_set.filter(published_date__isnull=False)
        update_news_ctx(ctx, self.request, news, hot=settings.SIDEBAR_POST_COUNT)
        ctx.update({
            'title': f'All articles by {self.kwargs["username"]}',
            'author_username': user.profile.fullname,
        })
        return ctx

class UserDraftList(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'news/news_list_drafts.html'

    def get_context_data(self, **kwargs):
        ctx = super(UserDraftList, self).get_context_data(**kwargs)
        user = get_object_or_404(User, username=self.kwargs['username'])
        news = user.post_set.filter(published_date__isnull=True).order_by('-created_date')
        update_news_ctx(ctx, self.request, news)
        ctx.update({
            'title': f'All drafts by {self.kwargs["username"]}',
            'author_username': self.kwargs['username'],
        })
        return ctx


class NewsPage(DetailView):
    model = Post
    template_name = 'news/news_page.html'

    def get_context_data(self, **kwargs):
        ctx = super(NewsPage, self).get_context_data(**kwargs)
        post = get_object_or_404(Post, slug=self.kwargs['slug'], published_date__isnull=False)
        view_post(self.request, post)
        news = Post.objects.filter(category=post.category, published_date__isnull=False).exclude(id=post.id)
        update_news_ctx(ctx, self.request, news, hot=settings.SIDEBAR_POST_COUNT)
        ctx.update({
            'title': post,
            'category': post.category,
            'page_absolute_url': self.request.build_absolute_uri(post.get_absolute_url())
        })
        return ctx

class DraftPage(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'news/draft_page.html'



    def get_context_data(self, **kwargs):
        ctx = super(DraftPage, self).get_context_data(**kwargs)
        post = get_object_or_404(Post, slug=self.kwargs['slug'], published_date__isnull=True)
        view_post(self.request, post)
        news = Post.objects.filter(category=post.category, published_date__isnull=True).exclude(id=post.id)
        update_news_ctx(ctx, self.request, news)
        ctx.update({
            'title': post,
            'category': post.category,
            'page_absolute_url': self.request.build_absolute_uri(post.get_absolute_url())
        })
        return ctx


class CreateNews(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['category', 'tags', 'title', 'text']


    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(CreateNews, self).get_context_data(**kwargs)
        context['parent_categories'] = Category.objects.parents()
        context['tags'] = Tag.objects.all()
        return context
    # def get_success_url(self):
    #     return reverse('draft_page', kwargs={'slug': self.slug})


class EditNews(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['category', 'tags', 'title', 'text']

    def form_valid(self, form):
        # form.instance.author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(EditNews, self).get_context_data(**kwargs)
        context['parent_categories'] = Category.objects.parents()
        context['tags'] = Tag.objects.all()
        return context

    def test_func(self):
        news = self.get_object()
        if self.request.user == news.author or self.request.user.profile.moderator:
            return True
        return False


class DeleteNews(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        news = self.get_object()
        if self.request.user == news.author or self.request.user.profile.moderator:
            return True
        return False


class CategoryView(DetailView):
    model = Category
    template_name = 'news/news_list_sorted.html'

    def get_context_data(self, **kwargs):
        ctx = super(CategoryView, self).get_context_data(**kwargs)
        category = get_object_or_404(Category, slug=self.kwargs['slug'])
        news = category.post_set.filter(published_date__isnull=False)
        update_news_ctx(ctx, self.request, news, hot=settings.SIDEBAR_POST_COUNT)
        ctx.update({
            'title': f'Категория: {category.title}',
            'category': category,
        })
        return ctx


class TagNewsList(ListView):
    model = Post
    template_name = 'news/news_list_sorted.html'

    def get_context_data(self, **kwargs):
        ctx = super(TagNewsList, self).get_context_data(**kwargs)
        tag = get_object_or_404(Tag, slug=self.kwargs['slug'])
        news = Post.objects.filter(tags__id=tag.id)
        update_news_ctx(ctx, self.request, news, hot=settings.SIDEBAR_POST_COUNT)
        ctx.update({
            'title': f'Tag: {tag.name}',
            'tag': tag,
        })
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
