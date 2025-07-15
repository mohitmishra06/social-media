from rest_framework import  serializers
from user_comments.serializers import serializers
from user_comments.models import UserCommentModels

class CommentSerializers(serializers.ModelSerializer):
    class Meta:
        model = UserCommentModels
        fields = ["id", "comment", "deleted_at"]