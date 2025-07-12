from rest_framework.views import APIView
from rest_framework.response import Response
from user_followers.models import UserFollowerModel, UserFollowerRequestModel, UserBlockModel
from user_followers.serializers import FollowersSerializers, FollowerRequestSerializers, BlockSerializers

# Followers
class UserFollowersView(APIView):
    # Get all records
    # Followers
    def get(self, request, format=None):
        try:
            # Get all data
            followers = UserFollowerModel.objects.filter(follower_id=request.data.get("userId"))
            
            if not followers:
                return Response({"code":400, "status":False, "msg":"Something went wrong", "errors":""})
            
            # 🔥 Serialize the queryset, when data comes in multiple
            serialized_followers = FollowersSerializers(followers, many=True)
            return Response({"code":200, "status":True, "msg":"All yours followers.", "data":serialized_followers.data})
            
        except UserFollowerModel.DoesNotExist:
            return Response({"code":500, "status":False, "msg":"No follower found", "errors":""})
    
    def put(self, request, format=None):
        try:
            # Get all data
            followers = UserFollowerModel.objects.filter(following_id=request.data.get("userId"))
            
            if not followers:
                return Response({"code":400, "status":False, "msg":"Something went wrong", "errors":""})
            
            # 🔥 Serialize the queryset, when data comes in multiple
            serialized_followers = FollowersSerializers(followers, many=True)
            return Response({"code":200, "status":True, "msg":"All you followed.", "data":serialized_followers.data})
            
        except UserFollowerModel.DoesNotExist:
            return Response({"code":500, "status":False, "msg":"No follower found", "errors":""})

    # Add new follower
    def post(self, request, format=None):
        try:
            data = {
                "follower":request.data.get("followerId"),
                "following":request.data.get("followingId"),
            }

            # This line sent data to serialization.
            serializer = FollowersSerializers(data=data)

            # Validate data for empty or wrong value
            if serializer.is_valid():
                # Create a new follower
                serializer.save()

                return Response({"code":200, "status":True, "msg":"You followed him.", "data":serializer.data})
            
            return Response({"code":400, "status":False, "msg":"Something went wrong", "errors":serializer.errors})
        except Exception as e:
            return Response({"code":500, "status":False, "msg":"Something went wrong", "errors":""})

    # Partial update follower
    def delete(self, request, format=None):
        try:
            # Get follower for update
            follower = UserFollowerModel.objects.get(
                follower_id=request.data.get("followerId")
            )

            # Create data
            data = {
                "follower":request.data.get("follower"),
            }

            # Set data for the partial update
            serializer = FollowersSerializers(follower, data=data, partial=True)

            # Validate data for empty or wrong value
            if serializer.is_valid():
                # Create a new follower
                serializer.save()

                return Response({"code":200, "status":True, "msg":"You unfollow updated.", "data":serializer.data})
            
            return Response({"code":400, "status":False, "msg":"Something went wrong", "errors":serializer.errors})
        except Exception as e:
            return Response({"code":500, "status":False, "msg":"Something went wrong", "errors":""})

# Followers request
class UserFollowersView(APIView):
    # Get all records
    # Followers
    def get(self, request, format=None):
        try:
            # Get all data
            followers = UserFollowerModel.objects.filter(follower_id=request.data.get("userId"))
            
            if not followers:
                return Response({"code":400, "status":False, "msg":"Something went wrong", "errors":""})
            
            # 🔥 Serialize the queryset, when data comes in multiple
            serialized_followers = FollowersSerializers(followers, many=True)
            return Response({"code":200, "status":True, "msg":"All yours followers.", "data":serialized_followers.data})
            
        except UserFollowerModel.DoesNotExist:
            return Response({"code":500, "status":False, "msg":"No follower found", "errors":""})
    
    def put(self, request, format=None):
        try:
            # Get all data
            followers = UserFollowerModel.objects.filter(following_id=request.data.get("userId"))
            
            if not followers:
                return Response({"code":400, "status":False, "msg":"Something went wrong", "errors":""})
            
            # 🔥 Serialize the queryset, when data comes in multiple
            serialized_followers = FollowersSerializers(followers, many=True)
            return Response({"code":200, "status":True, "msg":"All you followed.", "data":serialized_followers.data})
            
        except UserFollowerModel.DoesNotExist:
            return Response({"code":500, "status":False, "msg":"No follower found", "errors":""})

    # Add new follower
    def post(self, request, format=None):
        try:
            data = {
                "follower":request.data.get("followerId"),
                "following":request.data.get("followingId"),
            }

            # This line sent data to serialization.
            serializer = FollowersSerializers(data=data)

            # Validate data for empty or wrong value
            if serializer.is_valid():
                # Create a new follower
                serializer.save()

                return Response({"code":200, "status":True, "msg":"You followed him.", "data":serializer.data})
            
            return Response({"code":400, "status":False, "msg":"Something went wrong", "errors":serializer.errors})
        except Exception as e:
            return Response({"code":500, "status":False, "msg":"Something went wrong", "errors":""})

    # Partial update follower
    def delete(self, request, format=None):
        try:
            # Get follower for update
            follower = UserFollowerModel.objects.get(
                follower_id=request.data.get("followerId")
            )

            # Create data
            data = {
                "follower":request.data.get("follower"),
            }

            # Set data for the partial update
            serializer = FollowersSerializers(follower, data=data, partial=True)

            # Validate data for empty or wrong value
            if serializer.is_valid():
                # Create a new follower
                serializer.save()

                return Response({"code":200, "status":True, "msg":"You unfollow updated.", "data":serializer.data})
            
            return Response({"code":400, "status":False, "msg":"Something went wrong", "errors":serializer.errors})
        except Exception as e:
            return Response({"code":500, "status":False, "msg":"Something went wrong", "errors":""})

# Block users
class UserFollowersView(APIView):
    # Get all records
    # Followers
    def get(self, request, format=None):
        try:
            # Get all data
            followers = UserFollowerModel.objects.filter(follower_id=request.data.get("userId"))
            
            if not followers:
                return Response({"code":400, "status":False, "msg":"Something went wrong", "errors":""})
            
            # 🔥 Serialize the queryset, when data comes in multiple
            serialized_followers = FollowersSerializers(followers, many=True)
            return Response({"code":200, "status":True, "msg":"All yours followers.", "data":serialized_followers.data})
            
        except UserFollowerModel.DoesNotExist:
            return Response({"code":500, "status":False, "msg":"No follower found", "errors":""})
    
    def put(self, request, format=None):
        try:
            # Get all data
            followers = UserFollowerModel.objects.filter(following_id=request.data.get("userId"))
            
            if not followers:
                return Response({"code":400, "status":False, "msg":"Something went wrong", "errors":""})
            
            # 🔥 Serialize the queryset, when data comes in multiple
            serialized_followers = FollowersSerializers(followers, many=True)
            return Response({"code":200, "status":True, "msg":"All you followed.", "data":serialized_followers.data})
            
        except UserFollowerModel.DoesNotExist:
            return Response({"code":500, "status":False, "msg":"No follower found", "errors":""})

    # Add new follower
    def post(self, request, format=None):
        try:
            data = {
                "follower":request.data.get("followerId"),
                "following":request.data.get("followingId"),
            }

            # This line sent data to serialization.
            serializer = FollowersSerializers(data=data)

            # Validate data for empty or wrong value
            if serializer.is_valid():
                # Create a new follower
                serializer.save()

                return Response({"code":200, "status":True, "msg":"You followed him.", "data":serializer.data})
            
            return Response({"code":400, "status":False, "msg":"Something went wrong", "errors":serializer.errors})
        except Exception as e:
            return Response({"code":500, "status":False, "msg":"Something went wrong", "errors":""})

    # Partial update follower
    def delete(self, request, format=None):
        try:
            # Get follower for update
            follower = UserFollowerModel.objects.get(
                follower_id=request.data.get("followerId")
            )

            # Create data
            data = {
                "follower":request.data.get("follower"),
            }

            # Set data for the partial update
            serializer = FollowersSerializers(follower, data=data, partial=True)

            # Validate data for empty or wrong value
            if serializer.is_valid():
                # Create a new follower
                serializer.save()

                return Response({"code":200, "status":True, "msg":"You unfollow updated.", "data":serializer.data})
            
            return Response({"code":400, "status":False, "msg":"Something went wrong", "errors":serializer.errors})
        except Exception as e:
            return Response({"code":500, "status":False, "msg":"Something went wrong", "errors":""})
  