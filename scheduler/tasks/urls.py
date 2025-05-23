from django.urls import path
from . import views

urlpatterns = [
    path('', views.task_list, name='task_list'),
    path('create/', views.task_create, name='task_create'),
    path('create_internal/', views.task_create_internal, name='task_create_internal'),
    path('create_inline/', views.create_task_inline, name='create_task_inline'),
    path('<int:pk>/', views.task_detail, name='task_detail'),
    path('<int:pk>/update/', views.task_update, name='task_update'),
    path('<int:pk>/delete/', views.task_delete, name='task_delete'),
    path('reject/', views.reject_inquiry, name='reject_inquiry'),
    path('<int:pk>/update_field/', views.update_task_field, name='update_task_field'),
    path('<int:pk>/upload_report/', views.upload_report, name='upload_report'),
    path('<int:pk>/download_report/', views.download_report, name='download_report'),
] 