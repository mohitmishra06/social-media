from rest_framework import  serializers
from user_likes.models import UserLikeModels

class LikesSerializers(serializers.ModelSerializer):
    class Meta:
        model = UserLikeModels
        fields = ["id", "user", "post", "comment", "deleted_at"]