from django.urls import path
from user_followers.views import UserFollowersView, UserFollowerRequestView, UserBlockedView
from . import views

urlpatterns = [
    path('followers/', UserFollowersView.as_view(), name='followers'),
    path('requests/', UserFollowerRequestView.as_view(), name='requests'),
    path('friend-requests/', views.friend_request, name='requests'),
    path('blocked/', UserBlockedView.as_view(), name='blocked')
]
