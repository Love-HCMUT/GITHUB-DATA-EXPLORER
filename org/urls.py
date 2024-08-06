
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.LoadTemplate),
    path('infor/', views.LoadDataOrg),
    path('top10/', views.Home), 
    path('data/', views.GetData)
]
