from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView 
from .import views

app_name = 'api'

urlpatterns = [
    path('auth/register/', views.RegisterView.as_view(), name='register'),
    path('auth/login/', views.LoginView.as_view(), name='login'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('auth/logout/', views.LogOutView.as_view(), name='logout'),
    path('auth/me/', views.MeView.as_view(), name='me'),
]   