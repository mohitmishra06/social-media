from django.urls import path
from user_auth.views import UserAuthentication, UserLogin, UserTokenValidation, ProfileUpdateView
from . import views

urlpatterns = [
    path('login/', UserLogin.as_view(), name='login'),
    path('user-session-data/', UserLogin.as_view(), name='user-session-data'),
    path('logout/', UserLogin.as_view(), name='logout'),
    path('register/', UserAuthentication.as_view(), name='register'),
    path('otp-validate/', UserAuthentication.as_view(), name='otp-validate'),
    path('change-password/', UserAuthentication.as_view(), name='change-password'),
    path('profile/', ProfileUpdateView.as_view(), name='profile'),
    path('user-details/', views.user_details, name='user-details'),
    path('check-username/', views.check_username, name='check-username'),
    path('new-otp/', views.new_otp, name='new-otp'),
    path('token_validation/', UserTokenValidation.as_view(), name="token_validation")
]
