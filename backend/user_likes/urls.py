from django.urls import path
from user_likes.views import UserLikesView

urlpatterns = [
    path('', UserLikesView.as_view(), name='likes')
]
