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
    encrypted_id = serializers.SerializerMethodField()      # This line add a column in serializer

    class Meta:
        model = User
        fields="__all__"        
        # fields = ['id', 'encrypted_id', 'name', 'email'] # If we have some fields apply this
        extra_kwargs={
            "password":{"write_only":True}
        }

    def get_encrypted_id(self, obj):
        from linkup.general_function import GeneralFunction # General function import
        return GeneralFunction.encrypt(obj.id)

# Profile
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields=["id","name", "surname", "email", "school", "work", "website", "city", "description", "username", "img", "banner"]
        extra_kwargs={
            "password":{"write_only":True}
        }