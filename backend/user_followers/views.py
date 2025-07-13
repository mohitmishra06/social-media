from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from user_followers.models import UserFollowerModel, UserFollowerRequestModel, UserBlockModel
from user_followers.serializers import FollowerRequestSerializers, FriendRequestWithUserDetailsSerialization, BlockSerializers
from linkup.general_function import GeneralFunction

# Import library for token
from rest_framework_simplejwt.tokens import RefreshToken

# Followers
class UserFollowersView(APIView):
    # Get user followed or not
    def get(self, request, formate=None):
        # Get current user id
        current_user = RefreshToken(request.COOKIES.get("refresh_token"))

        # Get profile id
        profile_id = request.GET.get("id")

        try:
            # Let's find user is follow or not
            follow_user = UserFollowerModel.objects.get(follower_id=current_user["user_id"], following_id=profile_id)

            # If user is follow data will not come
            if not follow_user:
                return Response({"code":403, "status":True, "msg":"The user didn't follow you.", "data":False})
            
            return Response({"code":200, "status":True, "msg":"The user follow you.", "data":True})

        # First time do not found any entry that's time genereate exception
        except UserFollowerModel.DoesNotExist:
            return Response({"code":403, "status":True, "msg":"The user didn't follow you.", "data":False})
    
        except Exception as e:
                return Response({"code":500, "status":False, "msg":"Internal Server Error.", "data":e})

    # User follow
    def delete(self, request, formate=None):
        # Get current user id
        current_user = RefreshToken(request.COOKIES.get("refresh_token"))

        # Get profile id
        profile_id = request.data.get("id")

        try:
            # Let's find user is follow or not
            exists_follower = UserFollowerModel.objects.filter(follower_id=current_user["user_id"], following_id=profile_id).first()

            # If user follow him so it delete the row and unfollow the user
            if exists_follower:
                delete_result = UserFollowerModel.objects.filter(id=exists_follower.id).delete()
                return Response({"code":400, "status":True, "msg":"You were not following this user.", "data":False})
            else:
                # Let's find user already give a request for following or not
                exists_request = UserFollowerRequestModel.objects.filter(sender_id=current_user["user_id"], receiver_id=profile_id).first()

                # If user unfollow him so it delete the follow request
                if exists_request:
                    request_delete_result = UserFollowerRequestModel.objects.filter(id=exists_request.id).delete()
                    return Response({"code":400, "status":True, "msg":"Your follow request has been deleted.", "data":False})
                else:
                    # Create a request for the current user follow him
                    data = {
                        "sender":current_user["user_id"], 
                        "receiver":profile_id
                    }

                    follower_request_serializer = FollowerRequestSerializers(data=data)

                    # Validate data for empty or wrong value
                    if follower_request_serializer.is_valid():
                        # Create a new post
                        follower_request_serializer.save()

                        return Response({"code":204, "status":True, "msg":"You followed this user.", "data":True})
       
        except Exception as e:
            return Response({"code":500, "status":False, "msg":"Internal Server Error.", "error":e})

# Followers request
class UserFollowerRequestView(APIView):
    def get(self, request, formate=None):
        # Get current user id
        current_user = RefreshToken(request.COOKIES.get("refresh_token"))

        # Get profile id
        profile_id = request.GET.get("id")

        try:
            # Let's find user is follow request sent or not
            follow_request = UserFollowerRequestModel.objects.get(sender_id=current_user["user_id"], receiver_id=profile_id)

            # If user is follow data will not come
            if not follow_request:
                return Response({"code":403, "status":True, "msg":"The user didn't sent you a follow request.", "data":False})
            
            return Response({"code":200, "status":True, "msg":"The user sent you a follow request.", "data":True})

        # First time do not found any entry that's time genereate exception
        except UserFollowerRequestModel.DoesNotExist:
            return Response({"code":403, "status":True, "msg":"The user didn't sent you a follow request.", "data":False})

# Block users
class UserBlockedView(APIView):
    def get(self, request, formate=None):
        # Get current user id
        current_user = RefreshToken(request.COOKIES.get("refresh_token"))

        # Get profile id
        profile_id = request.GET.get("id")

        try:
            # Let's find user is block or not
            blocked_user = UserBlockModel.objects.get(blocker_id=current_user["user_id"], blocked_id=profile_id)

            # If user is blocked data will not come
            if not blocked_user:
                return Response({"code":403, "status":True, "msg":"The user didn't block you.", "data":False})
            
            return Response({"code":200, "status":True, "msg":"The user blocked you", "data":True})

        # First time do not found any entry that's time genereate exception
        except UserBlockModel.DoesNotExist:
            return Response({"code":403, "status":True, "msg":"The user didn't block you.", "data":False})
        
        except Exception as e:
            return Response({"code":500, "status":False, "msg":"Internal Server Error.", "error":e})
        
    # User block
    def delete(self, request, formate=None):
        # Get current user id
        current_user = RefreshToken(request.COOKIES.get("refresh_token"))

        # Get profile id
        profile_id = request.data.get("id")

        try:
            # Let's find user is block or not
            exists_blocker = UserBlockModel.objects.filter(blocker_id=current_user["user_id"], blocked_id=profile_id).first()

            # If user block him so it delete the row and unblock the user
            if exists_blocker:
                delete_result = UserBlockModel.objects.filter(id=exists_blocker.id).delete()
                return Response({"code":200, "status":True, "msg":"You successfully unblocked this user..", "data":False})
            else:
                # Create a request for the current user block him
                data = {
                    "blocker":current_user["user_id"], 
                    "blocked":profile_id
                }

                # Create serializer for blocking user
                blocker_serializer = BlockSerializers(data=data)

                # Validate data for empty or wrong value
                if blocker_serializer.is_valid():
                    # Create a new post
                    blocker_serializer.save()

                    return Response({"code":204, "status":True, "msg":"You blocked this user.", "data":True})
        except Exception as e:
            return Response({"code":500, "status":False, "msg":"Internal Server Error.", "data":e})

# Get all current user's friend requests
def friend_request(request):
        # Get current user id
        current_user = GeneralFunction.decrypt(request.GET.get("id"))

        try:
            # Get current user friend request
            friends_request = UserFollowerRequestModel.objects.filter(receiver_id=current_user).select_related("sender")
            
            # If no records found to related to current user
            if not friends_request:
                return JsonResponse({"code":404, "status":False, "msg":"No user found.", "errors":""})
            
            # serialize the data
            friends_request_serializer = FriendRequestWithUserDetailsSerialization(friends_request, many=True)

            return JsonResponse({"code":200, "status":True, "msg":"All records found related to current user.", "data":friends_request_serializer.data})

        # First time do not found any entry that's time genereate exception
        except UserFollowerRequestModel.DoesNotExist:
            return JsonResponse({"code":403, "status":True, "msg":"The user didn't sent you a follow request.", "data":False})
