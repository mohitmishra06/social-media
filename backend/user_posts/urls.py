from django.urls import path
from user_posts.views import UserPostView

urlpatterns = [
    path("", UserPostView.as_view(), name="posts"),
]
