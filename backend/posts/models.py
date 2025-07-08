from django.db import models
from user_auth.models import User

# Create your models here.
# Post model
class UserPostModels(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_post")
    post_img=models.CharField(max_length=255, default='')
    desc = models.TextField(max_length=255, default='')
    created_at = models.DateTimeField(auto_now_add=True)    # auto_now_add fill time only one time, when save data in table first time, this naver change.
    updated_at = models.DateTimeField(auto_now=True)        # auto_now update the time on every save/update value

# Comment model
class UserCommentModels(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_comment")
    post = models.ForeignKey(UserPostModels, on_delete=models.CASCADE, related_name="post_comment")
    comment = models.CharField(max_length=255, default='')
    created_at = models.DateTimeField(auto_now_add=True)    # auto_now_add fill time only one time, when save data in table first time, this naver change.
    updated_at = models.DateTimeField(auto_now=True)        # auto_now update the time on every save/update value

# Like model
class UserLikeModels(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_like")
    post = models.ForeignKey(UserPostModels,
                on_delete=models.CASCADE, 
                related_name="post_like",
                null=True,      # This line allows to field can be null
                blank=True      # This line allows to field can be blank or empty 
            )
    comment = models.ForeignKey(
                UserCommentModels,
                on_delete=models.CASCADE,
                related_name="comment_like",
                null=True,      # This line allows to field can be null
                blank=True      # This line allows to field can be blank or empty 
            )
    created_at = models.DateTimeField(auto_now_add=True)    # auto_now_add fill time only one time, when save data in table first time, this naver change.
    updated_at = models.DateTimeField(auto_now=True)        # auto_now update the time on every save/update value