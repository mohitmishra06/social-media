from django.urls import path, include
from user_auth.views import UserAuthentication, UserLogin, UserTokenValidation
from . import views

urlpatterns = [
    path('login/', UserLogin.as_view(), name='login'),
    path('logout/', UserLogin.as_view(), name='logout'),
    path('register/', UserAuthentication.as_view(), name='register'),
    path('otp-validate/', UserAuthentication.as_view(), name='otp-validate'),
    path('change-password/', UserAuthentication.as_view(), name='change-password'),
    path('new-otp/', views.new_otp, name='new-otp'),
    path('token_validation/', UserTokenValidation.as_view(), name="token_validation")
]
