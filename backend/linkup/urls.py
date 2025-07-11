from django.contrib import admin
from django.urls import path, include

# Images upload
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('user_auth.urls')),
    path('api/posts/', include('user_posts.urls'))
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
