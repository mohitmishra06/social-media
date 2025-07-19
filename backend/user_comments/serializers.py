from rest_framework import  serializers
from user_comments.serializers import serializers
from user_comments.models import UserCommentModels

class CommentSerializers(serializers.ModelSerializer):
    class Meta:
        model = UserCommentModels
        fields = ["id", "user", "comment", "post", "deleted_at"]

class PostsCommentsSerializers(serializers.ModelSerializer):
    from user_auth.serializers import UserSerializer
    from user_posts.serializers import PostSerializers

    user = UserSerializer()
    post = PostSerializers()
    
    class Meta:
        model = UserCommentModels
        fields = ["id", "user", "comment", "post", "deleted_at"]