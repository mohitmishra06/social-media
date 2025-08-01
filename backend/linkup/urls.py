from django.contrib import admin
from django.urls import path, include

# Images upload
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/", include("user_auth.urls")),
    path("api/posts/", include("user_posts.urls")),
    path("api/users/", include("user_followers.urls")),
    path("api/users/likes/", include("user_likes.urls")),
    path("api/users/comments/", include("user_comments.urls")),
    path("api/users/story/", include("user_story.urls")),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
