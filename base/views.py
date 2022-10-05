from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import ArticleForm
from django.contrib import messages

# Create your views here.
from base.models import Article, Category

categories = Category.objects.all()


def index(request):
    query = request.GET.get('query') if request.GET.get('query') is not None else ''

    articles = Article.objects.filter(headline__contains=query).order_by('-publish_date')[:6]
    context = {
        'articles': articles,
        'categories': categories
    }
    return render(request, 'index.html', context)


def category(request, pk):
    query = request.GET.get('query') if request.GET.get('query') is not None else ''
    chosen_category = Category.objects.get(pk=pk)
    category_articles = Article.objects.filter(category=chosen_category)
    articles = category_articles.filter(headline__contains=query).order_by('-publish_date')[:6]
    context = {
        'articles': articles,
        'chosen_category': chosen_category,
        'categories': categories
    }
    return render(request, 'index.html', context)


def new(request):
    form = ArticleForm()
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    context = {"form": form}
    return render(request, 'new.html', context)


def show(request, pk):
    chosen_article = Article.objects.get(pk=pk)
    context = {
        'article': chosen_article,
        'categories': categories
    }
    return render(request, 'show.html', context)


def edit(request, pk):
    chosen_article = Article.objects.get(pk=pk)
    form = ArticleForm(instance=chosen_article)
    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=chosen_article)
        if form.is_valid():
            form.save()
            return redirect('show', pk=pk)
    context = {"form": form}
    return render(request, 'new.html', context)


def delete(request, pk):
    chosen_article = Article.objects.get(pk=pk)
    if request.method == 'POST':
        chosen_article.delete()
        return redirect("index")
    context = {"obj": chosen_article}
    return render(request, 'delete.html', context)


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'Пользователь не найден')
            return render(request, 'registration/login.html')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Неверный пароль')
            return render(request, 'registration/login.html')

    return render(request, 'registration/login.html')


def logout(request):
    auth_logout(request)
    return redirect('index')
