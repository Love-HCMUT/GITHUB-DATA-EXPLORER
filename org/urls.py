from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.LoadTemplate),
    path('infor/<str:orgname>/<str:TOKEN>', views.LoadDataOrg),
    path('data/<str:orgname>/<str:TOKEN>', views.GetData),
    path('languages/<str:orgname>/<str:TOKEN>', views.languages, name = 'languages'),
    path('contributions/<str:orgname>/<str:TOKEN>', views.contributions, name = 'contributions'),
]
