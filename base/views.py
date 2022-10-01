from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
from base.models import Article


def index(request):
    articles = Article.objects.order_by('publish_date')[:4]
    context = {'articles': articles}
    return render(request, 'index.html', context)


def new(request):
    return HttpResponse('new article')


def show(request):
    return render(request, 'show.html')


def edit(request):
    return HttpResponse('edit article')


def delete(request):
    return HttpResponse('delete article')
