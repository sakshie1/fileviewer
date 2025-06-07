from django.urls import path
from app import views

urlpatterns = [
    path('', views.index),
    path('view-file/', views.view_file),
    path('download-file/', views.download_file),
]
