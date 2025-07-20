from rest_framework import serializers
from user_posts.models import UserPostModels

class PostSerializers(serializers.ModelSerializer):
    class Meta:
        model = UserPostModels
        fields = ["id", "user", "post_img", "post_video", "desc", "deleted_at"]
    
    # Validate image should not be greater then 2MB
    def validate_post_img(self, value):
        if value is None:
            return value  # skip validation if empty
        max_size = 2 * 1024 * 1024
        if value.size > max_size:
            raise serializers.ValidationError("Image size should not exceed 2MB.")
        return value

    # Validate video should not be greater then 5MB
    def validate_post_video(self, value):
        if value is None:
            return value  # skip validation if empty
        max_size = 5 * 1024 * 1024
        if value.size > max_size:
            raise serializers.ValidationError("Video size should not exceed 5MB.")
        return value

class AllPostWithRelatedData(serializers.ModelSerializer):
    from user_auth.serializers import UserSerializer
    from user_comments.serializers import CommentSerializers
    from user_likes.serializers import LikesSerializers
    
    user = UserSerializer()  # ✅ show full user data
    post_comment = CommentSerializers(many=True)  # ✅ include related comments
    post_like = LikesSerializers(many=True)       # ✅ include related likes

    class Meta:
        model = UserPostModels
        fields = ["id", "user", "post_img", "post_video", "desc", "deleted_at", "post_comment", "post_like"]