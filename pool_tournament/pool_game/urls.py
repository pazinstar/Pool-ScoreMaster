from django.urls import path
from . import views

urlpatterns = [
     path('', views.home, name='home'),  # URL pattern for the homepage
    path('create/', views.create_tournament, name='create_tournament'),
    path('join/<int:tournament_id>/', views.join_tournament, name='join_tournament'),
    path('tournament/<int:pk>/', views.tournament_detail, name='tournament_detail'),
    path('tournament_list/', views.tournament_list, name='tournament_list'),  # URL pattern for the tournament list
    path('login/', views.user_login, name='login'),
    path('register/', views.user_registration, name='register'),
    path('logout/', views.logout_view, name='logout'),
]