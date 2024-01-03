from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *


app_name = 'login'

urlpatterns = [
    #path('login/', auth_views.LoginView.as_view(template_name = 'login/login.html'), name = 'login'),
    path('login/', login, name = 'login'),
    path('nlogin/', nlogin, name = 'nlogin'),
    path('otp/', CheckOTP, name = 'CheckOTP'),
    path('ootp/', OneTimeLogin, name = 'OOTPlogin'),
    path('logout/', auth_views.LogoutView.as_view(), name = 'logout'),
    path('signup/', signup, name = 'signup'),
    path('user/detailuser/',detailuser, name = 'detailuser'),
    path('user/regserial/', regserial, name = 'regserial'),
    
]