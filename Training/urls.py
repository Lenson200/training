from django.urls import path
from . import views

urlpatterns = [
    # Training Module URLs
    path("", views.index, name="index"),
    path('training-modules/', views.training_module_list, name='training_module_list'),
    path('training-modules/<int:pk>/', views.training_module_detail, name='training_module_detail'),
    path('training-modules/create/', views.training_module_create, name='training_module_create'),
    path('training-modules/<int:pk>/update/', views.training_module_update, name='training_module_update'),
    path('training-modules/<int:pk>/delete/', views.training_module_delete, name='training_module_delete'),
    
    # Trainee Progress URLs
    path('trainee-progress/', views.trainee_progress_list, name='trainee_progress_list'),
    path('trainee-progress/<int:pk>/', views.trainee_progress_detail, name='trainee_progress_detail'),
    path('trainee-progress/create/', views.trainee_progress_create, name='trainee_progress_create'),
    path('trainee-progress/<int:pk>/update/', views.trainee_progress_update, name='trainee_progress_update'),
    path('trainee-progress/<int:pk>/delete/', views.trainee_progress_delete, name='trainee_progress_delete'),

    # Exam URLs
    path('exams/', views.exam_list, name='exam_list'),
    path('exams/<int:pk>/', views.exam_detail, name='exam_detail'),
    path('exams/create/', views.exam_create, name='exam_create'),
    path('exams/<int:pk>/update/', views.exam_update, name='exam_update'),
    path('exams/<int:pk>/delete/', views.exam_delete, name='exam_delete'),
]
