from django.urls import path

from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path('projects/', views.project_list, name='project_list'),
    path('projects/new/', views.project_create, name='project_create'),
    path('projects/<slug:slug>/', views.project_detail, name='project_detail'),
    path('projects/<slug:slug>/edit/', views.project_edit, name='project_edit'),
    path('projects/<slug:slug>/delete/', views.project_delete, name='project_delete'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('moderation/', views.moderation_queue, name='moderation_queue'),
    path('moderation/<slug:slug>/approve/', views.project_approve, name='project_approve'),
    path('moderation/<slug:slug>/reject/', views.project_reject, name='project_reject'),
    path('admin-panel/', views.admin_dashboard, name='admin_dashboard'),
    path('register/', views.register, name='register'),
    path('login/', views.custom_login, name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('projects/<slug:slug>/gallery/upload/', views.project_gallery_upload, name='project_gallery_upload'),
    path('admin-panel/users/', views.admin_users, name='admin_users'),
    path('verify-email/<str:token>/', views.verify_email, name='verify_email'),
]
