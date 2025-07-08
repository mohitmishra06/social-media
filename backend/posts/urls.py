from django.urls import path
from posts.views import UserPosts

urlpatterns = [
    path('', UserPosts.as_view(), name='get_post'),
]
