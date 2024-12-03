from django.urls import path
from django.shortcuts import render
from . import views

urlpatterns = [
    path('', views.sample, name='main'),
    path('detect/', views.upload_and_detect, name='upload_and_detect'),
]