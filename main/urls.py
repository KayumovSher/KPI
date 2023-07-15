from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name="home"),
    path('signup/', views.SignupPage),
    path('login/', views.LoginPage),



    path('sport/<int:id>/', views.sport, name='sport_detail'),
    


    path('evrika_create/<int:kpi_id>/', views.create_evrika, name='create_evrika'),
    path('evrika/<int:id>/', views.evrika, name='evrika_detail'),
    path('evrika/<int:kpi_id>/edit/<int:evrika_id>/', views.edit_evrika, name='edit_evrika'),
    path('evrika/<int:kpi_id>/delete/<int:evrika_id>/', views.delete_evrika, name='delete_evrika'),
    
    path('work_create/<int:kpi_id>/', views.create_work, name='create_work'),
    path('work/<int:id>/', views.work, name='work_detail'),
    path('work/<int:kpi_id>/edit/<int:work_id>/', views.edit_work, name='edit_work'),
    path('work/<int:kpi_id>/delete/<int:work_id>/', views.delete_work, name='delete_work'),
    

    path('book_create/<int:kpi_id>/', views.create_book, name='create_book'),
    path('book/<int:id>/', views.book, name='book_detail'),
    path('book/<int:kpi_id>/edit/<int:book_id>/', views.edit_book, name='edit_book'),
    path('book/<int:kpi_id>/delete/<int:book_id>/', views.delete_book, name='delete_book'),
    

    path('reminder/', views.reminder),
    
]
