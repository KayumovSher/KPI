from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name="index"),
    path('signup/', views.SignupPage, name="signup"),
    path('login/', views.LoginPage, name="login"),
    path('logout/', views.LogoutPage, name="logout"),
    path('book/<int:id>/', views.book, name="book_detail"),
   


    path('sport/<int:id>/', views.sport, name='sport_detail'),
    

    path('work_create/<int:kpi_id>/', views.create_work, name='create_work'),
    path('work/<int:id>/', views.work, name='work_detail'),
    path('work/<int:kpi_id>/edit/<int:work_id>/', views.edit_work, name='edit_work'),
    path('work/<int:kpi_id>/delete/<int:work_id>/', views.delete_work, name='delete_work'),

    path('book_create/<int:kpi_id>/', views.create_book, name='create_book'),
    path('book/<int:id>/', views.book, name='book_detail'),
    path('book/<int:kpi_id>/edit/<int:book_id>/', views.edit_book, name='edit_book'),
    path('book/<int:kpi_id>/delete/<int:book_id>/', views.delete_book, name='delete_book'),
       
    path('sport_create/<int:kpi_id>/', views.create_sport, name='create_sport'),
    path('sport/<int:id>/', views.sport, name='sport_detail'),
    path('sport/<int:kpi_id>/edit/<int:sport_id>/', views.edit_sport, name='edit_sport'),
    path('sport/<int:kpi_id>/delete/<int:sport_id>/', views.delete_sport, name='delete_sport'),
    

    path('evrika_create/<int:kpi_id>/', views.create_evrika, name='create_evrika'),
    path('evrika/<int:id>/', views.evrika, name='evrika_detail'),
    path('evrika/<int:kpi_id>/edit/<int:evrika_id>/', views.edit_evrika, name='edit_evrika'),
    path('evrika/<int:kpi_id>/delete/<int:evrika_id>/', views.delete_evrika, name='delete_evrika'),
    
    path("all_works/", views.all_works, name='all_works'),
    path("all_books/", views.all_books, name='all_books'),
    path("all_evrika/", views.all_evrikas, name='all_evrika'),
    path("all_sports/", views.all_sports, name='all_sports'),

    path('reminder/', views.reminder),
    path('book_items/', views.bookItems, name='book_items'),

    

    path('kpi_create/', views.create_kpi, name='create_kpi'),
    path('kpi/', views.kpi_view, name='kpi_detail'),
    path('kpi/<int:kpi_id>/edit/', views.edit_kpi, name='edit_kpi'),
    path('kpi/<int:kpi_id>/delete/', views.delete_kpi, name='delete_kpi'),
    
    
    path('navbar/', views.Navbar, name='navbar')

]