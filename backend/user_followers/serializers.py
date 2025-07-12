from rest_framework import  serializers
from user_followers.models import UserFollowerModel, UserFollowerRequestModel, UserBlockModel

class FollowersSerializers(serializers.ModelSerializer):
    class Meta:
        model = UserFollowerModel
        fields = ["follower", "following", "deleted_at"]

class FollowerRequestSerializers(serializers.ModelSerializer):
    class Meta:
        model = UserFollowerRequestModel
        fields = ["sender", "receiver", "deleted_at"]

class BlockSerializers(serializers.ModelSerializer):
    class Meta:
        model = UserBlockModel
        fields = ["blocker", "blocked", "deleted_at"]