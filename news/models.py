from django.db import models
from django.utils import timezone
from django.urls import reverse


class Post(models.Model):

    class Meta:
        ordering = ('-published_date', )

    POSTS_ON_PAGE = 3

    author = models.ForeignKey('auth.User', on_delete=models.PROTECT)
    category = models.ForeignKey(to='news.Category', on_delete=models.PROTECT, blank=True, null=True)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=255, db_index=True, unique=True)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('news_page', kwargs={'slug': self.slug})




class CategoryQueryset(models.QuerySet):

    def parents(self):
        return self.filter(parent__isnull=True)


class Category(models.Model):

    class Meta:
        ordering = ('title', )

    parent = models.ForeignKey(to='self', on_delete=models.SET_NULL, blank=True, null=True)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=255, db_index=True, unique=True)

    objects = CategoryQueryset.as_manager()

    def __str__(self):
        return self.title

    def children(self):
        return self.category_set.all()

    def get_absolute_url(self):
        return reverse('category_news', kwargs={'slug': self.slug})
