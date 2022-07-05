from django.urls import path
from . import views

urlpatterns = [
    path('', views.GalleryView.as_view()),
    path('<str:nickname>/', views.UserGalleryView.as_view()),
    path('upload/makepainting/', views.PaintingView.as_view()),
]