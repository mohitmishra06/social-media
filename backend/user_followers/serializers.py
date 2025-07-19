from rest_framework import  serializers
from user_followers.models import UserFollowerModel, UserFollowerRequestModel, UserBlockModel
from user_auth.models import User
from user_auth.serializers import UserSerializer
from user_comments.serializers import CommentSerializers
from user_likes.serializers import LikesSerializers
from user_posts.serializers import PostSerializers

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

# Get data accourding to join query
# First create user serialization so we can get all records from the user
class UserFriendRequestSerialization(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"        
        extra_kwargs={
            "password":{"write_only":True}
        }

# Create Friends request serialization with the user data
class FriendRequestWithUserDetailsSerialization(serializers.ModelSerializer):
    # First include User serialization for the user/sender data
    sender = UserFriendRequestSerialization()  # nested serializer for related sender
    
    class Meta:
        model = UserFollowerRequestModel
        fields = ["sender", "receiver", "deleted_at"]

class FollowingUserPostWithRelatedDataSerializer(serializers.ModelSerializer):
    following = UserSerializer()  # ✅ show full user data
    user_post = PostSerializers(many=True, source="following.user_post")
    user_comment = CommentSerializers(many=True, source="following.user_comment")
    user_like = LikesSerializers(many=True, source="following.user_like")  # use correct related_name

    class Meta:
        model = UserFollowerModel
        fields = ["id", "following", "user_post", "user_comment", "user_like"]