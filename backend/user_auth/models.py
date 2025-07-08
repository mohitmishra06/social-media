from django.db import models
from django.utils import timezone

# Create your models here.
# User model
class User(models.Model):
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=255, unique=True)
    otp_code = models.IntegerField(default=0)
    otp_expire = models.DateTimeField(auto_now_add=True)
    password = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    img = models.CharField(max_length=255, default='')
    banner = models.CharField(max_length=255, default='')
    name = models.CharField(max_length=255, default='')
    surname = models.CharField(max_length=255, default='')
    description = models.CharField(max_length=255, default='')
    city = models.CharField(max_length=255, default='')
    school = models.CharField(max_length=255, default='')
    work = models.CharField(max_length=255, default='')
    website = models.CharField(max_length=255, default='')
    created_at = models.DateTimeField(auto_now_add=True)    # auto_now_add fill time only one time, when save data in table first time, this naver change.
    updated_at = models.DateTimeField(auto_now=True)        # auto_now update the time on every save/update value

# Follows model
class UserFollowerModel(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_follower")
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_following")
    created_at = models.DateTimeField(auto_now_add=True)    # auto_now_add fill time only one time, when save data in table first time, this naver change.
    updated_at = models.DateTimeField(auto_now=True)        # auto_now update the time on every save/update value

# Follows Request model 
# when a user follow any one, he couldn't follow directly, he need a mediator for it, this table works as mediator.
class UserFollowerRequestModel(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="request_follower")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="request_following")
    created_at = models.DateTimeField(auto_now_add=True)    # auto_now_add fill time only one time, when save data in table first time, this naver change.
    updated_at = models.DateTimeField(auto_now=True)        # auto_now update the time on every save/update value

# Block model
# when a user want to block any one, he couldn't block directly, he need a mediator for it, this table works as mediator.
class UserBlockModel(models.Model):
    blocker = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_blocker")
    blocked = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_blocked")
    created_at = models.DateTimeField(auto_now_add=True)    # auto_now_add fill time only one time, when save data in table first time, this naver change.
    updated_at = models.DateTimeField(auto_now=True)        # auto_now update the time on every save/update value

# Story model
class UserStoryModel(models.Model):
    story = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_story")
    img_url = models.CharField(max_length=255, default='')
    expires_at = models.DateTimeField(auto_now_add=True)    # auto_now_add fill time only one time, when save data in table first time, this naver change.
    created_at = models.DateTimeField(auto_now_add=True)    # auto_now_add fill time only one time, when save data in table first time, this naver change.
    updated_at = models.DateTimeField(auto_now=True)        # auto_now update the time on every save/update value
