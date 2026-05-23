from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

app_name = 'core'

urlpatterns = [
    # Home
    path('', views.HomeView.as_view(), name='home'),

    # Autenticación
    path('login/', views.CustomLoginView.as_view(), name='login'),
   path(
    'logout/',
    LogoutView.as_view(
        next_page='core:home'
    ),
    name='logout'
),
    path('register/', views.register, name='register'),

    # Gestión de CV
    path('cv/create/', views.CVWizardView.as_view(), name='cv_create'),
    path('cv/<int:user_id>/', views.CVDetailView.as_view(), name='cv_detail'),
    path('cvs/', views.CVListView.as_view(), name='cv_list'),

    # Perfil de usuario
    path('profile/', views.ProfileView.as_view(), name='profile'),

     path(
        'delete-cv/',
        views.delete_cv,
        name='delete_cv'
    ),
]