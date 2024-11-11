from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name="index"),
    path('signup/', views.SignupPage, name="signup"),
    path('login/', views.LoginPage, name="login"),
    path('logout/', views.LogoutPage, name="logout"),

   



    path("work/<int:work_id>/work_change_score/", views.work_increase_reset_decrease_score, name='work_increase_reset_decrease_score'),
    path('work/<int:id>/', views.work, name='work_detail'),

    path("book/<str:book_id>/book_change_score/", views.book_increase_decrease_score, name='book_increase_decrease_score'),
    path('book/<int:id>/', views.book, name='book_detail'),

    path("sport/<str:sport_id>/sport_change_score/", views.sport_increase_decrease_score, name='sport_increase_decrease_score'),
    path('sport/<int:id>/', views.sport, name='sport_detail'),

    path("evrika/<str:evrika_id>/evrika_change_score/", views.evrika_increase_decrease_score, name='evrika_increase_decrease_score'),
    path('evrika/<int:id>/', views.evrika, name='evrika_detail'),

    path('meeting/<str:meeting_id>/meeting_change_score/', views.meeting_increase_decrease_score, name='meeting_increase_decrease_score'),
    path('meeting/<int:id>/', views.meeting, name='meeting_detail'),


    path("all_works/", views.all_works, name='all_works'),
    path("all_books/", views.all_books, name='all_books'),
    path("all_evrika/", views.all_evrikas, name='all_evrika'),
    path("all_sports/", views.all_sports, name='all_sports'),
    path('all_meetings/', views.all_meetings, name='all_meetings'),

    
    path('reminder/', views.reminder),
    path('book_items/', views.bookItems, name='book_items'),

    path('test/', views.get_data, name='test'),

    path('kpi_create/', views.create_kpi, name='create_kpi'),
    path('kpi/', views.kpi_view, name='kpi_detail'),
    path('kpi/<int:kpi_id>/edit/', views.edit_kpi, name='edit_kpi'),
    path('kpi/<int:kpi_id>/delete/', views.delete_kpi, name='delete_kpi'),
    
    
    path('navbar/', views.Navbar, name='navbar')

]