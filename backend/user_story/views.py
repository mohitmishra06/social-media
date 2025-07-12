from rest_framework.views import APIView
from rest_framework.response import Response
from user_story.models import UserStoryModel
from user_story.serializers import StorySerializers

class UserStoryView(APIView):
    # Get all records
    def get(self, request, format=None):
        try:
            # Get all data
            story = UserStoryModel.objects.filter(user_id=request.data.get("userId"))
            
            if not story:
                return Response({"code":400, "status":False, "msg":"Something went wrong", "errors":""})
            
            # 🔥 Serialize the queryset, when data comes in multiple
            serialized_story = StorySerializers(story, many=True)
            return Response({"code":200, "status":True, "msg":"All story.", "data":serialized_story.data})
            
        except UserStoryModel.DoesNotExist:
            return Response({"code":500, "status":False, "msg":"No story found", "errors":""})

    # Add new story
    def post(self, request, format=None):
        try:
            data = {
                "user":request.data.get("userId"),
                "img_url":request.data.get("imgUrl")
            }

            # This line sent data to serialization.
            serializer = StorySerializers(data=data)

            # Validate data for empty or wrong value
            if serializer.is_valid():
                # Create a new user
                serializer.save()

                return Response({"code":200, "status":True, "msg":"You add a story today.", "data":serializer.data})
            
            return Response({"code":400, "status":False, "msg":"Something went wrong", "errors":serializer.errors})
        except Exception as e:
            return Response({"code":500, "status":False, "msg":"Something went wrong", "errors":""})

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
  