from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.LoadTemplate),
    path('infor/<str:orgname>', views.LoadDataOrg),
    path('data/<str:orgname>', views.GetData),
    path('languages/<str:orgname>', views.languages, name = 'languages'),
    path('contributions/<str:orgname>', views.contributions, name = 'contributions'),
]
