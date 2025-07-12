from rest_framework import  serializers
from user_story.models import UserStoryModel

class StorySerializers(serializers.ModelSerializer):
    class Meta:
        model = UserStoryModel
        fields = ["user", "img_url", "expires_at", "deleted_at"]