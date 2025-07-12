from rest_framework.views import APIView
from rest_framework.response import Response
from user_likes.models import UserLikeModels
from user_likes.serializers import LikesSerializers

# Get all records
# Likes
class UserLikesView(APIView):
    def get(self, request, format=None):
        try:
            # Get all data
            likes = UserLikeModels.objects.get(
                post_id=request.data.get("postId"),
                user_id=request.data.get("userId")
            )
            
            if not likes:
                return Response({"code":400, "status":False, "msg":"Something went wrong", "errors":""})
            
            # 🔥 Serialize the queryset, when data comes in multiple
            serialized_likes = LikesSerializers(likes, many=True)
            return Response({"code":200, "status":True, "msg":"All likes.", "data":serialized_likes.data})
            
        except UserLikeModels.DoesNotExist:
            return Response({"code":500, "status":False, "msg":"No like found", "errors":""})
    
    def put(self, request, format=None):
        try:
            # Get all data
            likes = UserLikeModels.objects.get(
                post_id=request.data.get("postId"),
                user_id=request.data.get("userId"),
                comment_id=request.data.get("commentId")
            )
            
            if not likes:
                return Response({"code":400, "status":False, "msg":"Something went wrong", "errors":""})
            
            # 🔥 Serialize the queryset, when data comes in multiple
            serialized_likes = LikesSerializers(likes, many=True)
            return Response({"code":200, "status":True, "msg":"All liks.", "data":serialized_likes.data})
            
        except UserLikeModels.DoesNotExist:
            return Response({"code":500, "status":False, "msg":"No liks found", "errors":""})

    # Add new like
    def post(self, request, format=None):
        try:
            data = {
                "post_id":request.data.get("postId"),
                "user_id":request.data.get("userId"),
                "comment_id":request.data.get("commentId")
            }

            # This line sent data to serialization.
            serializer = LikesSerializers(data=data)

            # Validate data for empty or wrong value
            if serializer.is_valid():
                # Create a new like
                serializer.save()

                return Response({"code":200, "status":True, "msg":"You like the post.", "data":serializer.data})
            
            return Response({"code":400, "status":False, "msg":"Something went wrong", "errors":serializer.errors})
        except Exception as e:
            return Response({"code":500, "status":False, "msg":"Something went wrong", "errors":""})

    # Partial update like
    def delete(self, request, format=None):
        try:
            # Get like for update
            like = UserLikeModels.objects.get(
                like_id=request.data.get("likeId")
            )

            # Create data
            data = {
                "like":request.data.get("like"),
            }

            # Set data for the partial update
            serializer = LikesSerializers(like, data=data, partial=True)

            # Validate data for empty or wrong value
            if serializer.is_valid():
                # Create a new like
                serializer.save()

                return Response({"code":200, "status":True, "msg":"You unlike this post.", "data":serializer.data})
            
            return Response({"code":400, "status":False, "msg":"Something went wrong", "errors":serializer.errors})
        except Exception as e:
            return Response({"code":500, "status":False, "msg":"Something went wrong", "errors":""})
  