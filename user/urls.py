from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home), 
    path('activity/<str:username>/<str:TOKEN>', views.GetDataActivity),
    path('data/<str:username>/<str:TOKEN>', views.GetData),
    path('months/<str:username>/<str:TOKEN>', views.GetMonths),
    path('languages/<str:username>/<str:TOKEN>', views.languages, name = 'languages'),
]
