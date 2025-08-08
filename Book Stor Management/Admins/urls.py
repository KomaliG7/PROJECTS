from django.urls import path
from .views import (
    IndexView, AdminLoginView, UserLoginView, UserRegisterView,
    AdminLoginAction, UserLoginAction, UserRegisterAction, LogoutView
)
app_name = 'admins'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('admin-login/', AdminLoginView.as_view(), name='AdminLogin'),
    path('user-login/', UserLoginView.as_view(), name='UserLogin'),
    path('user-register/', UserRegisterView.as_view(), name='UserRegister'),

    # ✅ Fix: add .as_view()
    path('admin-login-action/', AdminLoginAction.as_view(), name='AdminLoginAction'),
    path('user-login-action/', UserLoginAction.as_view(), name='UserLoginAction'),
    path('user-register-action/', UserRegisterAction.as_view(), name='UserRegisterAction'),

    path('logout/', LogoutView.as_view(), name='logout'),
]
