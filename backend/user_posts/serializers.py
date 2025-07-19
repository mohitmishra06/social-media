from rest_framework import serializers
from user_posts.models import UserPostModels

class PostSerializers(serializers.ModelSerializer):
    class Meta:
        model = UserPostModels
        fields = ["id", "user", "post_img", "desc", "deleted_at"]

class AllPostWithRelatedData(serializers.ModelSerializer):
    from user_auth.serializers import UserSerializer
    from user_comments.serializers import CommentSerializers
    from user_likes.serializers import LikesSerializers
    
    user = UserSerializer()  # ✅ show full user data
    post_comment = CommentSerializers(many=True)  # ✅ include related comments
    post_like = LikesSerializers(many=True)       # ✅ include related likes

    class Meta:
        model = UserPostModels
        fields = ["id", "user", "post_img", "desc", "deleted_at", "post_comment", "post_like"]