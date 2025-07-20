from django.db import models
from user_auth.models import User

# Create your models here.
# Post model
class UserPostModels(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_post")
    post_img=models.ImageField(upload_to="posts/post_img", blank=True, null=True)
    post_video=models.FileField(upload_to="posts/post_vedio", blank=True, null=True)
    desc = models.TextField(max_length=255, default='')
    created_at = models.DateTimeField(auto_now_add=True)    # auto_now_add fill time only one time, when save data in table first time, this naver change.
    updated_at = models.DateTimeField(auto_now=True)        # auto_now update the time on every save/update value
    deleted_at = models.BooleanField(default=False)