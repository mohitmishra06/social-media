from rest_framework import  serializers
from user_posts.models import UserPostModels

class PostSerializers(serializers.ModelSerializer):
    class Meta:
        model = UserPostModels
        fields = ["user", "post_img", "desc", "deleted_at"]