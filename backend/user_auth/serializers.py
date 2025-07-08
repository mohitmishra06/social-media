from rest_framework import serializers
from user_auth.models import User

# Register
class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields=['email', 'username']
        extra_kwargs={
            'otp_code':{'write_only':True}
        }

# Change password
class UserPWDChangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields=['email', 'username', 'password']
        extra_kwargs={
            'password':{'write_only':True}
        }   
    