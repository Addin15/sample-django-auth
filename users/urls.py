from django.urls import path, include
from . import views

from knox import views as knox_views

urlpatterns = [
    path('register/', views.RegisterApi.as_view(), name='register'),
    path('login/', views.LoginApi.as_view(), name='login'),
    path('user/', views.UserApi.as_view(), name='user'),
    path('users/', views.UsersApi.as_view(), name='users'),
    path('logout/', views.LogoutApi.as_view(), name='logout'),
    path('logoutall/', views.LogoutAllApi.as_view(), name='logoutall'),
]
