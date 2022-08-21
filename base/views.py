from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.

def index(request):
    return HttpResponse('homepage')


def new(request):
    return HttpResponse('new article')


def show(request):
    return HttpResponse('show article')


def edit(request):
    return HttpResponse('edit article')


def delete(request):
    return HttpResponse('delete article')
