from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('book/', views.book),
    path('sport/', views.sport),
    path('work/', views.work),
    path('eureka/', views.eureka),
]
