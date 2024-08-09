from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home), 
    path('activity/<str:username>', views.GetDataActivity),
    path('data/<str:username>', views.GetData),
    path('months/<str:username>', views.GetMonths),
    path('languages/<str:username>', views.languages, name = 'languages'),
]
