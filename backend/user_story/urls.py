from django.urls import path
from user_story.views import UserStoryView

urlpatterns = [
    path('', UserStoryView.as_view(), name='stories')
]
