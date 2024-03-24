from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('register/', userRegister, name="register"),
    path('login/', userLogin, name="login"),
    path('logout/', userLogout, name="logout"),
    path('change-password/', change_password, name='change_password'),
    path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),

]