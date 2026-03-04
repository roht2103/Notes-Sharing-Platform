"""
URL configuration for notes app
"""
from django.urls import path
from . import views
from .views_setup import initial_setup

urlpatterns = [
    # Initial setup (one-time admin creation)
    path('setup/', initial_setup, name='initial_setup'),

    # Home/Note List
    path('', views.note_list_view, name='note_list'),

    # Authentication URLs
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Note URLs
    path('upload/', views.upload_note_view, name='upload_note'),
    path('note/<int:pk>/', views.note_detail_view, name='note_detail'),
    path('download/<int:pk>/', views.download_note_view, name='download_note'),

    # Comment URLs
    path('comment/delete/<int:pk>/', views.delete_comment_view, name='delete_comment'),
]
