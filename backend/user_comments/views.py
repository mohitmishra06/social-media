from rest_framework.views import APIView
from rest_framework.response import Response
from user_comments.models import UserCommentModels
from user_comments.serializers import CommentSerializers, PostsCommentsSerializers

class UserCommentView(APIView):
    # Get all records
    def get(self, request, format=None):
        try:
            post_id = request.GET.get("postId")

            if not post_id:
                return Response({"code":400, "status":False, "msg":"postId is required", "errors":""})

            comments = UserCommentModels.objects.filter(post_id=post_id).select_related("post")
            
            if not comments.exists():
                return Response({"code":404, "status":False, "msg":"No data found", "errors":""})

            serialized_comments = PostsCommentsSerializers(comments, many=True)
            return Response({
                "code":200,
                "status":True,
                "msg":"All comments related to this post.",
                "data":serialized_comments.data
            })

        except Exception as e:
            return Response({
                "code":500,
                "status":False,
                "msg":"Internal Server Error",
                "errors":str(e)
            })

    # Add new comment
    def post(self, request, format=None):
        try:
            data = {
                "user":request.data.get("userId"),
                "post":request.data.get("postId"),
                "comment":request.data.get("desc")
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
            return Response({"code":500, "status":False, "msg":"Something went wrong", "errors":str(e)})

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
  