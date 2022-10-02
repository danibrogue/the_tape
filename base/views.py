from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
from base.models import Article, Category

categories = Category.objects.all()


def index(request):
    articles = Article.objects.order_by('-publish_date')[:6]
    context = {
        'articles': articles,
        'categories': categories
    }
    return render(request, 'index.html', context)


def category(request, pk):
    chosen_category = Category.objects.get(pk=pk)
    articles = Article.objects.filter(category=chosen_category)
    context = {
        'articles': articles,
        'chosen_category': chosen_category
    }
    return render(request, 'index.html', context)


def new(request):
    return HttpResponse('new article')


def show(request, pk):
    chosen_article = Article.objects.get(pk=pk)
    context = {
        'article': chosen_article,
        'categories': categories
    }
    return render(request, 'show.html', context)


def edit(request):
    return HttpResponse('edit article')


def delete(request):
    return HttpResponse('delete article')
