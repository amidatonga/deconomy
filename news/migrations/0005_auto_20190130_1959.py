# Generated by Django 2.1.3 on 2019-01-30 16:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0004_auto_20190130_1606'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ('parent__title',)},
        ),
    ]
