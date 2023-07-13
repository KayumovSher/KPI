from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name="home"),
    path('signup/', views.SignupPage),
    path('login/', views.LoginPage),



    path('sport/<int:id>/', views.sport, name='sport_detail'),
    



    path('evrika/<int:id>/', views.eureka, name='evrika_detail'),

    path('work_create/<int:kpi_id>/', views.create_work, name='create_work'),
    path('work/<int:id>/', views.work, name='work_detail'),
    path('work/<int:kpi_id>/edit/<int:work_id>/', views.edit_work, name='edit_work'),
    path('work/<int:kpi_id>/delete/<int:work_id>/', views.delete_work, name='delete_work'),
    

    path('book_create/<int:kpi_id>/', views.create_book, name='create_book'),
    path('book/<int:id>/', views.book, name='books'),
    path('book/<int:kpi_id>/edit/<int:book_id>/', views.edit_book, name='edit_book'),
    path('book/<int:kpi_id>/delete/<int:book_id>/', views.delete_book, name='delete_book'),
    

    path('reminder/', views.reminder),
    
]
