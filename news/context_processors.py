# -*- coding: utf-8 -*-
from news.models import Category


def categories(request):
    return {
        'parents': Category.objects.parents()
    }
