from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('new/', views.new, name='new'),
    path('show/', views.show, name='show'),
    path('edit/', views.edit, name='edit'),
    path('delete/', views.delete, name='delete'),
    path('category/<str:pk>/', views.category, name='category')
]
