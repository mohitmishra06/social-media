from rest_framework.views import APIView
from rest_framework.response import Response
from user_story.models import UserStoryModel
from user_followers.models import UserFollowerModel
from user_story.serializers import StorySerializers, StoriesWithUserSerializers
# Count the number of rows in join query
from pathlib import Path

# Get story which is not expire yet, expiry time is 24hours
from django.utils import timezone
from datetime import timedelta

class UserStoryView(APIView):
    # Get all records
    def get(self, request, format=None):
        try:            
            # Get current time
            now = timezone.now()

            # Calculate 24 hours ago
            time_threshold = now - timedelta(hours=24)
            
            # Get followed users
            followed_users = UserFollowerModel.objects.filter(follower_id=request.GET.get("userId")).values_list('following', flat=True)

            # Filter stories from followed users that are not expired
            valid_stories = UserStoryModel.objects.filter(
                user__in=followed_users,
                created_at__gte=timezone.now() - timedelta(hours=24)
            )
            
            # If users have come
            if not valid_stories:
                return Response({"code":404, "status":False, "msg":"No records found.", "errors":""})
            
            # 🔥 Serialize the queryset, when data comes in multiple
            serialized_story = StoriesWithUserSerializers(valid_stories, many=True)

            return Response({"code":200, "status":True, "msg":"All story.", "data":serialized_story.data})
            
        except Exception as e:
            return Response({"code":500, "status":False, "msg":"No story found", "errors":str(e)})

    # Add new story
    def post(self, request, format=None):
        try:
            data = {
                "user": request.POST.get('userId')             # From FormData field
            }

            # Get file comming from angular
            # Get file if exists
            file = request.FILES.get('file', None)

            if file:
                uploadFile = Path(file.name)
                extension = uploadFile.suffix.lower()

                allowed_img_exts = [".png", ".jpg", ".jpeg", ".svg"]
                allowed_video_exts = [".mp3", ".mp4"]

                # Extenstion validation
                if extension not in allowed_img_exts and extension not in allowed_video_exts:
                    return Response({
                        "code": 400,
                        "status": False,
                        "msg": "Something went wrong",
                        "errors": "File format should be png, jpg, jpeg, mp3, or mp4."
                    })

                # Size validation
                # if file.size > 5 * 1024 * 1024:
                #     return Response({
                #         "code": 400,
                #         "status": False,
                #         "msg": "File too large.",
                #         "errors": "Maximum allowed size is 5MB."
                #     })

                # Decide whether it's an image or video
                if extension in allowed_img_exts:
                    data["img_url"] = file
                elif extension in allowed_video_exts:
                    data["video_url"] = file

                # Let's find user is follow or not
                exists_story = UserStoryModel.objects.filter(user_id=request.POST.get('userId')).first()

                # If user follow him so it delete the row and unfollow the user
                if exists_story:
                    delete_result = UserStoryModel.objects.filter(id=exists_story.id).delete()
                    return Response({"code":400, "status":True, "msg":"Your story is deleted.", "data":False})
                else:                       
                    # Send to serializer
                    serializer = StorySerializers(data=data)

                    if serializer.is_valid():
                        serializer.save()
                        return Response({
                            "code": 200,
                            "status": True,
                            "msg": "You have created a post.",
                            "data": serializer.data
                        })
                        
                # Handle serializer errors
                if serializer.errors.get("video_url"):
                    error = serializer.errors["video_url"]
                elif serializer.errors.get("img_url"):
                    error = serializer.errors["img_url"]
                else:
                    error = serializer.errors

                return Response({"code":400, "status":False, "msg":"Something went wrong", "errors":error})
        except Exception as e:
            return Response({"code":500, "status":False, "msg":"Internal Server Error", "errors":str(e)})

    # Partial update story
    def patch(self, request, format=None):
        try:
            # Get story for update
            story = UserStoryModel.objects.get(
                user_id=request.data.get("userId"),
                id=request.data.get("storyId")
            )

            # Create data
            data = {
                "img_url":request.data.get("img_url"),
            }

            # Set data for the partial update
            serializer = StorySerializers(story, data=data, partial=True)

            # Validate data for empty or wrong value
            if serializer.is_valid():
                # Create a new story
                serializer.save()

                return Response({"code":200, "status":True, "msg":"Your story updated.", "data":serializer.data})
            
            return Response({"code":400, "status":False, "msg":"Something went wrong", "errors":serializer.errors})
        except Exception as e:
            return Response({"code":500, "status":False, "msg":"Something went wrong", "errors":""})
        
    # Update story
    def put(self, request, format=None):
        try:            
            # Get story for update
            story = UserStoryModel.objects.get(
                user_id=request.data.get("userId"),
                id=request.data.get("storyId")
            )

            data = {
                "img_url":request.data.get("img_url")
            }

            # Set data for the partial update
            serializer = StorySerializers(story, data=data)

            # Validate data for empty or wrong value
            if serializer.is_valid():
                # Create a new user
                serializer.save()

                return Response({"code":200, "status":True, "msg":"Your story updated.", "data":serializer.data})
            
            return Response({"code":400, "status":False, "msg":"Something went wrong", "errors":serializer.errors})
        except Exception as e:
            return Response({"code":500, "status":False, "msg":"Something went wrong", "errors":""})
   
    # Delete story
    def delete(self, request, format=None):
        try:
            # Get story for update
            story = UserStoryModel.objects.get(
                user_id=request.data.get("userId"),
                id=request.data.get("storyId")
            )

            # Create data
            data = {
                "deleted_at":True,
            }

            # Set data for the partial update
            serializer = StorySerializers(story, data=data, partial=True)

            # Validate data for empty or wrong value
            if serializer.is_valid():
                # Create a new story
                serializer.save()

                return Response({"code":200, "status":True, "msg":"Your story deleted.", "data":serializer.data})
            
            return Response({"code":400, "status":False, "msg":"Something went wrong", "errors":serializer.errors})
        except Exception as e:
            return Response({"code":500, "status":False, "msg":"Something went wrong", "errors":""})
  