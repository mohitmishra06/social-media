from django.urls import path
from user_followers.views import UserFollowersView, UserFollowerRequestView, UserBlockedView, UserFriendRequestView
from . import views

urlpatterns = [
    path('followers/', UserFollowersView.as_view(), name='followers'),
    path('requests/', UserFollowerRequestView.as_view(), name='requests'),
    path('friend-requests/', UserFriendRequestView.as_view(), name='friend-requests'),
    path('blocked/', UserBlockedView.as_view(), name='blocked'),
    path("get-all-followers/", views.get_all_followers, name="get-all-follower")
]
