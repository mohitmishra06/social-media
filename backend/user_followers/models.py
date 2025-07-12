from django.db import models
from user_auth.models import User

# Follows model
class UserFollowerModel(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_follower")
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_following")
    created_at = models.DateTimeField(auto_now_add=True)    # auto_now_add fill time only one time, when save data in table first time, this naver change.
    updated_at = models.DateTimeField(auto_now=True)        # auto_now update the time on every save/update value
    deleted_at = models.BooleanField(default=False)


# Follows Request model 
# when a user follow any one, he couldn't follow directly, he need a mediator for it, this table works as mediator.
class UserFollowerRequestModel(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="request_follower")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="request_following")
    created_at = models.DateTimeField(auto_now_add=True)    # auto_now_add fill time only one time, when save data in table first time, this naver change.
    updated_at = models.DateTimeField(auto_now=True)        # auto_now update the time on every save/update value
    deleted_at = models.BooleanField(default=False)


# Block model
# when a user want to block any one, he couldn't block directly, he need a mediator for it, this table works as mediator.
class UserBlockModel(models.Model):
    blocker = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_blocker")
    blocked = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_blocked")
    created_at = models.DateTimeField(auto_now_add=True)    # auto_now_add fill time only one time, when save data in table first time, this naver change.
    updated_at = models.DateTimeField(auto_now=True)        # auto_now update the time on every save/update value
    deleted_at = models.BooleanField(default=False)

