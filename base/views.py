from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import ArticleForm, NewUserForm
from django.contrib import messages

# Create your views here.
from base.models import Article, Category
from .decorators import unauthenticated_user, allowed_users, authenticated_user

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


@allowed_users(allowed_roles=['admin'])
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


@allowed_users(allowed_roles=['admin'])
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


@allowed_users(allowed_roles=['admin'])
def delete(request, pk):
    chosen_article = Article.objects.get(pk=pk)
    if request.method == 'POST':
        chosen_article.delete()
        return redirect("index")
    context = {"obj": chosen_article}
    return render(request, 'delete.html', context)


@unauthenticated_user
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


@unauthenticated_user
def register(request):
    form = NewUserForm()
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.username = user.username.lower()
            group = Group.objects.get(name='guest')
            user.groups.add(group)
            auth_login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Возникли проблемы с регистрацией')
    return render(request, 'registration/register.html', {'form': form})


def logout(request):
    auth_logout(request)
    return redirect('index')


@authenticated_user
def profile(request):
    return render(request, 'profile.html')


def newsletter(request):
    return render(request, 'newsletter.html')
