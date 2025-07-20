from rest_framework import  serializers
from user_story.models import UserStoryModel

class StorySerializers(serializers.ModelSerializer):
    class Meta:
        model = UserStoryModel
        fields = ["user", "img_url", "video_url", "expires_at", "deleted_at"]
    
    # Validate image should not be greater then 2MB
    def validate_img_url(self, value):
        if value is None:
            return value  # skip validation if empty
        max_size = 2 * 1024 * 1024
        if value.size > max_size:
            raise serializers.ValidationError("Image size should not exceed 2MB.")
        return value

    # Validate video should not be greater then 5MB
    def validate_video_url(self, value):
        if value is None:
            return value  # skip validation if empty
        max_size = 5 * 1024 * 1024
        if value.size > max_size:
            raise serializers.ValidationError("Video size should not exceed 5MB.")
        return value

class StoriesWithUserSerializers(serializers.ModelSerializer):
    from user_auth.serializers import UserSerializer
    user = UserSerializer()

    class Meta:
        model = UserStoryModel
        fields = ["user", "img_url", "video_url", "expires_at", "deleted_at"]