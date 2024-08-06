from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home), 
    path('activity', views.GetDataActivity),
    path('lam/', views.Home), 
    path('data/', views.GetData),
    path('months/', views.GetMonths),
    path('test/', views.test, name = 'test'),
    path('languages/<str:username>', views.languages, name = 'languages'),
]
