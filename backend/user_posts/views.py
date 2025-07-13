from rest_framework.views import APIView
from rest_framework.response import Response
from user_posts.serializers import PostSerializers
from user_posts.models import UserPostModels
from linkup.general_function import GeneralFunction

class UserPostView(APIView):
    # Get all records
    def get(self, request, format=None):
        try:
            # Decrypt user id
            user_id = GeneralFunction.decrypt(request.data.get("userId"))
            
            # Get all data
            posts = UserPostModels.objects.filter(user_id=user_id)
            if not posts:
                return Response({"code":400, "status":False, "msg":"Something went wrong", "errors":""})
            
            # 🔥 Serialize the queryset
            serialized_posts = PostSerializers(posts, many=True)
            return Response({"code":200, "status":True, "msg":"You have created a post.", "data":serialized_posts.data})
            
        except UserPostModels.DoesNotExist:
            return Response({"code":500, "status":False, "msg":"No post found", "errors":""})

    # Add new post
    def post(self, request, format=None):
        try:
            # Decrypt user id
            user_id = GeneralFunction.decrypt(request.data.get("userId"))
            data = {
                "user":user_id,
                "desc":request.data.get("desc")
            }

            # This line sent data to serialization.
            serializer = PostSerializers(data=data)

            # Validate data for empty or wrong value
            if serializer.is_valid():
                # Create a new user
                serializer.save()

                return Response({"code":200, "status":True, "msg":"You have created a post.", "data":serializer.data})
            
            return Response({"code":400, "status":False, "msg":"Something went wrong", "errors":serializer.errors})
        except Exception as e:
            return Response({"code":500, "status":False, "msg":"Something went wrong", "errors":""})

    # Partial update post
    def patch(self, request, format=None):
        try:
            # Decrypt user id
            user_id = GeneralFunction.decrypt(request.data.get("userId"))
            
            # Get post for update
            post = UserPostModels.objects.get(id=request.data.get("postId"), user_id=user_id)

            # Create data
            data = {
                "desc":request.data.get("desc"),
            }

            # Set data for the partial update
            serializer = PostSerializers(post, data=data, partial=True)

            # Validate data for empty or wrong value
            if serializer.is_valid():
                # Create a new post
                serializer.save()

                return Response({"code":200, "status":True, "msg":"Your post updated.", "data":serializer.data})
            
            return Response({"code":400, "status":False, "msg":"Something went wrong", "errors":serializer.errors})
        except Exception as e:
            return Response({"code":500, "status":False, "msg":"Something went wrong", "errors":""})
        
    # Update post
    def put(self, request, format=None):
        try:
            # Decrypt user id
            user_id = GeneralFunction.decrypt(request.data.get("userId"))
            
            # Get post for update
            post = UserPostModels.objects.get(id=request.data.get("postId"), user_id=user_id)

            data = {
                "desc":request.data.get("desc"),
                "img":request.data.get("postImg")
            }

            # Set data for the partial update
            serializer = PostSerializers(post, data=data)

            # Validate data for empty or wrong value
            if serializer.is_valid():
                # Create a new user
                serializer.save()

                return Response({"code":200, "status":True, "msg":"Your post updated.", "data":serializer.data})
            
            return Response({"code":400, "status":False, "msg":"Something went wrong", "errors":serializer.errors})
        except Exception as e:
            return Response({"code":500, "status":False, "msg":"Something went wrong", "errors":""})
   
    # Delete post
    def delete(self, request, format=None):
        try:
            # Decrypt user id
            user_id = GeneralFunction.decrypt(request.data.get("userId"))

            # Get post for update
            post = UserPostModels.objects.get(id=request.data.get("postId"), user_id=user_id)

            # Create data
            data = {
                "deleted_at":True,
            }

            # Set data for the partial update
            serializer = PostSerializers(post, data=data, partial=True)

            # Validate data for empty or wrong value
            if serializer.is_valid():
                # Create a new post
                serializer.save()

                return Response({"code":200, "status":True, "msg":"Your post deleted.", "data":serializer.data})
            
            return Response({"code":400, "status":False, "msg":"Something went wrong", "errors":serializer.errors})
        except Exception as e:
            return Response({"code":500, "status":False, "msg":"Something went wrong", "errors":""})
  
