from django.urls import path
from user_comments.views import UserCommentView

urlpatterns = [
    path('', UserCommentView.as_view(), name='comments')
]
