from rest_framework.views import APIView
from rest_framework.response import Response
from user_comments.models import UserCommentModels
from user_comments.serializers import CommentSerializers

class UserCommentView(APIView):
    # Get all records
    def get(self, request, format=None):
        try:
            # Get all data
            comments = UserCommentModels.objects.filter(user_id=request.data.get("userId"), post_id=request.data.get("postId"))
            
            if not comments:
                return Response({"code":400, "status":False, "msg":"Something went wrong", "errors":""})
            
            # 🔥 Serialize the queryset, when data comes in multiple
            serialized_comments = CommentSerializers(comments, many=True)
            return Response({"code":200, "status":True, "msg":"All comments related to this post.", "data":serialized_comments.data})
            
        except UserCommentModels.DoesNotExist:
            return Response({"code":500, "status":False, "msg":"No comment found", "errors":""})

    # Add new comment
    def post(self, request, format=None):
        try:
            data = {
                "user":request.data.get("userId"),
                "post":request.data.get("postId"),
                "comment":request.data.get("comment")
            }

            # This line sent data to serialization.
            serializer = CommentSerializers(data=data)

            # Validate data for empty or wrong value
            if serializer.is_valid():
                # Create a new user
                serializer.save()

                return Response({"code":200, "status":True, "msg":"You gave your review on a post.", "data":serializer.data})
            
            return Response({"code":400, "status":False, "msg":"Something went wrong", "errors":serializer.errors})
        except Exception as e:
            return Response({"code":500, "status":False, "msg":"Something went wrong", "errors":""})

    # Partial update comment
    def patch(self, request, format=None):
        try:
            # Get comment for update
            comment = UserCommentModels.objects.get(
                post_id=request.data.get("postId"),
                user_id=request.data.get("userId"),
                id=request.data.get("commentId")
            )

            # Create data
            data = {
                "comment":request.data.get("comment"),
            }

            # Set data for the partial update
            serializer = CommentSerializers(comment, data=data, partial=True)

            # Validate data for empty or wrong value
            if serializer.is_valid():
                # Create a new comment
                serializer.save()

                return Response({"code":200, "status":True, "msg":"Your commnet updated.", "data":serializer.data})
            
            return Response({"code":400, "status":False, "msg":"Something went wrong", "errors":serializer.errors})
        except Exception as e:
            return Response({"code":500, "status":False, "msg":"Something went wrong", "errors":""})
        
    # Update comment
    def put(self, request, format=None):
        try:            
            # Get comment for update
            comment = UserCommentModels.objects.get(
                post_id=request.data.get("postId"),
                user_id=request.data.get("userId"),
                id=request.data.get("commentId")
            )

            data = {
                "comment":request.data.get("comment")
            }

            # Set data for the partial update
            serializer = CommentSerializers(comment, data=data)

            # Validate data for empty or wrong value
            if serializer.is_valid():
                # Create a new user
                serializer.save()

                return Response({"code":200, "status":True, "msg":"Your comment updated.", "data":serializer.data})
            
            return Response({"code":400, "status":False, "msg":"Something went wrong", "errors":serializer.errors})
        except Exception as e:
            return Response({"code":500, "status":False, "msg":"Something went wrong", "errors":""})
   
    # Delete comment
    def delete(self, request, format=None):
        try:
            # Get comment for update
            comment = UserCommentModels.objects.get(
                post_id=request.data.get("postId"),
                user_id=request.data.get("userId"),
                id=request.data.get("commentId")
            )

            # Create data
            data = {
                "deleted_at":True,
            }

            # Set data for the partial update
            serializer = CommentSerializers(comment, data=data, partial=True)

            # Validate data for empty or wrong value
            if serializer.is_valid():
                # Create a new comment
                serializer.save()

                return Response({"code":200, "status":True, "msg":"Your comment deleted.", "data":serializer.data})
            
            return Response({"code":400, "status":False, "msg":"Something went wrong", "errors":serializer.errors})
        except Exception as e:
            return Response({"code":500, "status":False, "msg":"Something went wrong", "errors":""})
  