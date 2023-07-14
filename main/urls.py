from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('signup/', views.SignupPage, name="signup"),
    path('login/', views.LoginPage, name="login"),
    path('book/<int:id>/', views.book, name="book_detail"),
    path('sport/<int:id>/', views.sport, name='sport_detail'),
    path('evrika/<int:id>/', views.eureka, name='evrika_detail'),
    path('work/<int:id>/', views.work, name="work_detail"),
    path('reminder/', views.reminder),
    
]
