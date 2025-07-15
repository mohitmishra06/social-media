from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework.response import Response
from user_posts.serializers import PostSerializers, AllPostWithRelatedData
from user_posts.models import UserPostModels
from linkup.general_function import GeneralFunction

class UserPostView(APIView):
    # Get all records
    def get(self, request, format=None):
        try:
            # Decrypt user id
            profile_id = request.GET.get("id")
            
            # Get all data
            start=0
            end=8

            # Get the user posts
            # This query does first it get the record accourding to id and then it filster this record to image is empty or null.
            posts = UserPostModels.objects.filter(user_id=profile_id, post_img__isnull=False).exclude(post_img="").order_by('-created_at')[start:end]
            
            if not posts:
                return Response({"code":400, "status":False, "msg":"Something went wrong", "errors":""})
            
            # 🔥 Serialize the queryset
            serialized_posts = PostSerializers(posts, many=True)

            return Response({"code":200, "status":True, "msg":"You have created a post.", "data":serialized_posts.data})
            
        except Exception as e:
            return Response({"code":500, "status":False, "msg":"No post found", "errors":e})

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
  
# Outside function which is call directly
# Get user post with comment, like, userdetails
def get_all_post_with_all_details(request):
    try:
        # Decrypt user id
        profile_id = request.GET.get("id")
        
        # Get all data
        start=0
        end=8

        posts = 0
        if request.GET.get('id') is None:
            posts = UserPostModels.objects.all().order_by('-created_at')[start:end]
        else:
            posts = UserPostModels.objects.select_related("user").prefetch_related(
                            "post_comment",
                            "post_like"
                        )

            print(posts[0].user.username)
            print(posts[0].post_comment)
            print(posts[0].post_like)

        if not posts:
            return JsonResponse({"code":404, "status":False, "msg":"Something went wrong", "errors":"Data not found."})
        
        # 🔥 Serialize the queryset
        serialized_posts = AllPostWithRelatedData(posts, many=True)
        print(serialized_posts)
        return JsonResponse({"code":200, "status":True, "msg":"You have created a post.", "data":serialized_posts.data})
        
    except Exception as e:
        return JsonResponse({"code":500, "status":False, "msg":"No post found", "errors":str(e)})