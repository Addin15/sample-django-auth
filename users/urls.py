from django.urls import path, include
from . import views

from knox import views as knox_views

urlpatterns = [
    path('api/register/', views.RegisterApi.as_view(), name='register'),
    path('api/login/', views.LoginApi.as_view(), name='login'),
    path('api/user/', views.UserApi.as_view(), name='user'),
    path('api/users/', views.UsersApi.as_view(), name='users'),
    path('api/logout/', views.LogoutApi.as_view(), name='knox_logout'),
    path('api/logoutall/', views.LogoutAllApi.as_view(), name='knox_logoutall'),
]
