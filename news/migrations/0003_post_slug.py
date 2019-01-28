# Generated by Django 2.1.5 on 2019-01-27 15:41
from django.db import migrations, models

from news.models import Post


def fill_slugs(apps, schema_editor):
    for post in Post.objects.filter(slug='default'):
        post.slug = None
        post.save()


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0002_auto_20190126_1648'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='slug',
            field=models.SlugField(default='default', max_length=255, unique=False),
            preserve_default=False,
        ),

        migrations.RunPython(fill_slugs, reverse_code=lambda a, b: None),

        migrations.AlterField(
            model_name='post',
            name='slug',
            field=models.SlugField(max_length=255, unique=True),
        ),
    ]
