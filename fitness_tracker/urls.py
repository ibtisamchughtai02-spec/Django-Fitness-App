from django.urls import path
from . import views
from .data_utils import import_data, export_data

urlpatterns = [
    # Authentication URLs
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    
    # Dashboard and Profile URLs
    path('', views.dashboard, name='dashboard'),
    path('profile/', views.profile_view, name='profile'),
    
    # Workout CRUD URLs
    path('workouts/', views.workout_list, name='workout_list'),
    path('workouts/<int:pk>/', views.workout_detail, name='workout_detail'),
    path('workouts/create/', views.workout_create, name='workout_create'),
    path('workouts/<int:pk>/edit/', views.workout_edit, name='workout_edit'),
    path('workouts/<int:pk>/delete/', views.workout_delete, name='workout_delete'),
    
    # Exercise CRUD URLs
    path('workouts/<int:workout_pk>/exercises/create/', views.exercise_create, name='exercise_create'),
    path('exercises/<int:pk>/edit/', views.exercise_edit, name='exercise_edit'),
    path('exercises/<int:pk>/delete/', views.exercise_delete, name='exercise_delete'),
    
    # Quick Workout URLs
    path('quick-workout/', views.quick_workout, name='quick_workout'),
    
    # Progress and Statistics URLs
    path('progress/', views.progress_view, name='progress'),
    
    # Data Import/Export URLs
    path('import/', import_data, name='import_data'),
    path('export/', export_data, name='export_data'),
    

]