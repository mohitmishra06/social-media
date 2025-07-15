from django.urls import path
from user_followers.views import UserFollowersView, UserFollowerRequestView, UserBlockedView, UserFriendRequestView

urlpatterns = [
    path('followers/', UserFollowersView.as_view(), name='followers'),
    path('requests/', UserFollowerRequestView.as_view(), name='requests'),
    path('friend-requests/', UserFriendRequestView.as_view(), name='friend-requests'),
    path('blocked/', UserBlockedView.as_view(), name='blocked')
]
