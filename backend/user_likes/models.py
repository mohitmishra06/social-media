from django.db import models
from user_auth.models import User
from user_posts.models import UserPostModels
from user_comments.models import UserCommentModels

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
    deleted_at = models.BooleanField(default=False)
