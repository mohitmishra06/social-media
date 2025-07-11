from django.db import models
from django.utils import timezone

# Create your models here.
# User model
class User(models.Model):
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=255, unique=True)
    otp_code = models.IntegerField(default=0)
    otp_expire = models.DateTimeField(auto_now=True)
    password = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    img = models.ImageField(upload_to="user_images", blank=True)
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
