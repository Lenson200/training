from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    # Training Module URLs
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("update/",views.update_trainee_profile,name="update_trainee_profile"),
    path('success/', views.success_page, name='success_page'),
    path('update-profile/', views.update_profile, name='update_profile'),
    # path('register/trainee/', views.trainee_registration, name='trainee_registration'),
    #training resources urls
    path('training-modules/', views.training_module_list, name='training_module_list'),
    path('training-modules/<int:pk>/', views.training_module_detail, name='training_module_detail'),
    path('training-modules/create/', views.training_module_create, name='training_module_create'),
    path('training-modules/<int:pk>/update/', views.training_module_update, name='training_module_update'),
    path('training_module/<int:pk>/delete/', views.training_module_delete, name='training_module_delete'),
    path('show_all/', views.show_all, name='show_all'),
    # Trainee Progress URLs
    path('mark_module_complete/', views.mark_module_complete, name='mark_module_complete'),
    path('mark-progress/', views.mark_progress, name='mark_progress'),
    path('trainee-progress/', views.trainee_progress_list, name='trainee_progress_list'),
    path('trainee-progress/<int:pk>/', views.trainee_progress_detail, name='trainee_progress_detail'),
    path('trainee-progress/create/', views.trainee_progress_create, name='trainee_progress_create'),
    path('trainee-progress/<int:pk>/update/', views.trainee_progress_update, name='trainee_progress_update'),
    path('trainee-progress/<int:pk>/delete/', views.trainee_progress_delete, name='trainee_progress_delete'),

    # Exam URLs
    path('exams/', views.exam_list, name='exam_list'),
    path('exams/<int:pk>/', views.exam_detail, name='exam_detail'),
    path('exams/<int:pk>/page/<int:page>/', views.exam_detail, name='exam_detail_page'),
    path('update_progress/<int:exam_id>/<int:progress>/', views.update_progress, name='update_progress'),
    path('exams/create/', views.exam_create, name='exam_create'),
    path('exams/<int:pk>/update/', views.exam_update, name='exam_update'),
    path('exams/<int:pk>/delete/', views.exam_delete, name='exam_delete'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
