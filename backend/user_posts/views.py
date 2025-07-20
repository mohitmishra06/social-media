from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework.response import Response
from pathlib import Path
from user_posts.serializers import PostSerializers, AllPostWithRelatedData
from user_posts.models import UserPostModels
from linkup.general_function import GeneralFunction
# Count the number of rows in join query
from django.db.models import Count

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
            user_id = GeneralFunction.decrypt(request.POST.get('userId'))           # From FormData field

            # Create data
            data = {
                "user":user_id,
                "desc":request.POST.get("description"),           # Description from FormData
            }

            # Get file comming from angular
            # Get file if exists
            file = request.FILES.get('file', None)

            if file:
                uploadFile = Path(file.name)
                extension = uploadFile.suffix.lower()

                allowed_img_exts = [".png", ".jpg", ".jpeg", ".svg"]
                allowed_video_exts = [".mp3", ".mp4"]

                if extension not in allowed_img_exts and extension not in allowed_video_exts:
                    return Response({
                        "code": 400,
                        "status": False,
                        "msg": "Something went wrong",
                        "errors": "File format should be png, jpg, jpeg, mp3, or mp4."
                    })

                # Decide whether it's an image or video
                if extension in allowed_img_exts:
                    data["post_img"] = file
                elif extension in allowed_video_exts:
                    data["post_video"] = file

            # Send to serializer
            serializer = PostSerializers(data=data)

            if serializer.is_valid():
                serializer.save()
                return Response({
                    "code": 200,
                    "status": True,
                    "msg": "You have created a post.",
                    "data": serializer.data
                })

            # Handle serializer errors
            if serializer.errors.get("post_video"):
                error = serializer.errors["post_video"]
            elif serializer.errors.get("post_img"):
                error = serializer.errors["post_img"]
            else:
                error = serializer.errors

            return Response({"code":400, "status":False, "msg":"Something went wrong", "errors":error})
        except Exception as e:
            return Response({"code":500, "status":False, "msg":"Internal Server Error", "errors":str(e)})

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
            # Get post for update
            post = UserPostModels.objects.filter(id=request.data.get("postId"), user_id=request.data.get("userId")).first()

            if not post:
                return Response({"code":404, "status":False, "msg":"Something went wrong.", "errors":""})


            # Delete record
            delete_record, record = post.delete();

            if(delete_record):
                return Response({"code":200, "status":True, "msg":"Your post was deleted.", "data":""})
            
        except Exception as e:
            return Response({"code":500, "status":False, "msg":"Internal Server Error.", "errors":str(e)})
  
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
            # posts = UserPostModels.objects.select_related("user").prefetch_related(
            #                 "post_comment",
            #                 "post_like"
            #             )

            # Get data with use_id, Join with post, user, comment and like table
            posts = UserPostModels.objects.filter(user_id=profile_id).select_related("user").prefetch_related(
                "post_comment",
                "post_like"
            ).annotate(
                comment_count=Count("post_comment"),
                like_count=Count("post_like")
            ).order_by('-created_at')[start:end]

        if not posts:
            return JsonResponse({"code":404, "status":False, "msg":"Something went wrong", "errors":"Data not found."})
        
        # 🔥 Serialize the queryset
        serialized_posts = AllPostWithRelatedData(posts, many=True)
        
        return JsonResponse({"code":200, "status":True, "msg":"You have created a post.", "data":serialized_posts.data})
        
    except Exception as e:
        return JsonResponse({"code":500, "status":False, "msg":"No post found", "errors":str(e)})