from django.db import models
from user_auth.models import User

# Story model
class UserStoryModel(models.Model):
    story = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_story")
    img_url = models.CharField(max_length=255, default='')
    expires_at = models.DateTimeField(auto_now_add=True)    # auto_now_add fill time only one time, when save data in table first time, this naver change.
    created_at = models.DateTimeField(auto_now_add=True)    # auto_now_add fill time only one time, when save data in table first time, this naver change.
    updated_at = models.DateTimeField(auto_now=True)        # auto_now update the time on every save/update value