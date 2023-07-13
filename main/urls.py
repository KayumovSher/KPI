from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="home"),
    path('signup/', views.SignupPage),
    path('login/', views.LoginPage),

    path('book/<int:id>/', views.book, name="book_detail"),


    path('sport/<int:id>/', views.sport, name='sport_detail'),
    path('evrika/<int:id>/', views.eureka, name='evrika_detail'),
    path('work/<int:id>/', views.work, name="work_detail"),
    path('edit_work/<int:kpi_id>/<int:work_id>/', edit_work, name='edit_work'),


    path('reminder/', views.reminder),
    
]
