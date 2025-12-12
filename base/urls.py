from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('subject/<str:pk>/', views.subject_page, name='subject'),
    
    # New Auth URLs
    path('login/', views.login_page, name='login'),
    path('register/', views.register_page, name='register'),
    path('logout/', views.logout_user, name='logout'),
    path('mark_complete/<int:subject_id>/<int:goal_id>/', views.mark_complete, name='mark_complete'),
    path('submit_quiz/<int:subject_id>/<int:goal_id>/', views.submit_quiz, name='submit_quiz'),
    path('journal/', views.journal_page, name='journal'),
    path('journal/edit/<int:pk>/', views.edit_journal, name='edit_journal'),
    path('profile/', views.profile_page, name='profile'),
]