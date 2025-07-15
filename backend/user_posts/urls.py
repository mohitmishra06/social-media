from django.urls import path
from user_posts.views import UserPostView
from . import views

urlpatterns = [
    path("", UserPostView.as_view(), name="posts"),
    path("get-all-post-with-all-details/", views.get_all_post_with_all_details, name="get-all-post"),
]
