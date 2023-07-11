from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('book/', views.book),
    path('sport/', views.sport, name='sport'),
    path('work/', views.work, name='work'),
    path('evrika/', views.eureka),
]
