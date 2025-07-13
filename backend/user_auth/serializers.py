from rest_framework import serializers
from user_auth.models import User

# Register
class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields=["id","email", "username", "img"]
        extra_kwargs={
            "otp_code":{"write_only":True}
        }

# Change password
class UserPWDChangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields=["id", "email", "username", "password"]
        extra_kwargs={
            "password":{"write_only":True}
        }

# Users all details
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields="__all__"
        extra_kwargs={
            "password":{"write_only":True}
        }
    