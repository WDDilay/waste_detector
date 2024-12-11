from django.urls import path
from django.shortcuts import render
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.main, name='main'),
    path('analyze', views.analyze, name='analyze'),
    path('detect/', views.upload_and_detect, name='upload_and_detect'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)