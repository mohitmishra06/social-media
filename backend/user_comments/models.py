from django.db import models
from user_auth.models import User
from user_posts.models import UserPostModels

# Comment model
class UserCommentModels(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_comment")
    post = models.ForeignKey(UserPostModels, on_delete=models.CASCADE, related_name="post_comment")
    comment = models.CharField(max_length=255, default='')
    created_at = models.DateTimeField(auto_now_add=True)    # auto_now_add fill time only one time, when save data in table first time, this naver change.
    updated_at = models.DateTimeField(auto_now=True)        # auto_now update the time on every save/update value
    deleted_at = models.BooleanField(default=False)