from django.urls import path
from . import views
from .views import NoteListCreateAPI, NoteRetrieveUpdateDestroyAPI

urlpatterns = [
    path('', views.home, name='home'),

    path('accounts/register/', views.register, name='register'),
    path('accounts/login/', views.user_login, name='login'),
    path('accounts/logout', views.user_logout, name='logout'),

    path('notes/create/', views.note_create, name='note_create'),
    path('notes/<int:pk>/edit/', views.note_edit, name='note_edit'),
    path('notes/<int:pk>/delete/', views.note_delete, name='note_delete'),

    path('api/notes/', NoteListCreateAPI.as_view(), name='api_note_list_create'),
    path('api/notes/<int:pk>/', NoteRetrieveUpdateDestroyAPI.as_view(), name='api_note_detail'),

]