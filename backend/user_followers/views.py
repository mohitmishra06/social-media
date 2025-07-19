from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from user_followers.models import UserFollowerModel, UserFollowerRequestModel, UserBlockModel
from user_followers.serializers import FollowersSerializers, FollowerRequestSerializers, FriendRequestWithUserDetailsSerialization, BlockSerializers, FollowingUserPostWithRelatedDataSerializer
from linkup.general_function import GeneralFunction
# Count the number of rows in join query
from django.db.models import Count, Prefetch

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
                return Response({"code":500, "status":False, "msg":"Internal Server Error.", "data":str(e)})

    # User follow request
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

                        return Response({"code":204, "status":True, "msg":"Your request for following user has been sent.", "data":True})
       
        except Exception as e:
            return Response({"code":500, "status":False, "msg":"Internal Server Error.", "error":str(e)})

# Followers request
class UserFollowerRequestView(APIView):
    # User sent followed request or not
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
        
        except Exception as e:
                return Response({"code":500, "status":False, "msg":"Internal Server Error.", "data":str(e)})

# Block users
class UserBlockedView(APIView):
    # Get records about user block or not
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
            return Response({"code":500, "status":False, "msg":"Internal Server Error.", "error":str(e)})
        
    # Block or Unblock User
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
            return Response({"code":500, "status":False, "msg":"Internal Server Error.", "data":str(e)})

# Friend request and accept block
class UserFriendRequestView(APIView):
    # Get all current user's friend requests
    def get(self, request, formate=None):
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

    # User friend request accept function
    def post(self, request, formate=None):
        # Get current user id
        current_user = RefreshToken(request.COOKIES.get("refresh_token"))

        # Get profile id
        profile_id = request.data.get("id")

        try:
            # Let's find user a friend request
            friend_request = UserFollowerRequestModel.objects.filter(sender_id=profile_id, receiver_id=current_user["user_id"]).first()

            # User have a friend request it will be delete.
            if friend_request:
                delete_result, delete_object = UserFollowerRequestModel.objects.filter(id=friend_request.id).delete()

                if delete_result > 0:
                    # If we accept the request the user will be follow us
                    data = {
                        "follower":profile_id, 
                        "following":current_user["user_id"]
                    }

                    # Create serializer for following user
                    accept_serializing = FollowersSerializers(data=data)

                    # Validate data for empty or wrong value
                    if accept_serializing.is_valid():
                        # Create a new post
                        accept_serializing.save()
                        return Response({"code":204, "status":True, "msg":"You accepted this user request.", "data":True})
                    else:                        
                        return Response({"code":204, "status":False, "msg":"Data doesn't insert.", "data":False})
                else:
                    return Response({"code":400, "status":False, "msg":"Something went wrong.", "error":"Record not deleted."})
            else:
                return Response({"code":404, "status":False, "msg":"No data found.", "error":""})

        except Exception as e:
            return Response({"code":500, "status":False, "msg":"Internal Server Error.", "data":str(e)})
        
    # User friend request delete function
    def delete(self, request, formate=None):
        # Get current user id
        current_user = RefreshToken(request.COOKIES.get("refresh_token"))

        # Get profile id
        profile_id = request.data.get("id")

        try:
            # Let's find user a friend request
            friend_request = UserFollowerRequestModel.objects.filter(sender_id=profile_id, receiver_id=current_user["user_id"]).first()

            # User have a friend request it will be delete.
            if friend_request:
                delete_result, delete_object = UserFollowerRequestModel.objects.filter(id=friend_request.id).delete()
                
                if delete_result > 0:
                    return Response({"code":200, "status":True, "msg":"You didn't accept this user request.", "data":True})
                else:
                    return Response({"code":400, "status":False, "msg":"Something went wrong.", "data":False})
            else:
                return Response({"code":404, "status":False, "msg":"No data found.", "error":""})

        except Exception as e:
            return Response({"code":500, "status":False, "msg":"Internal Server Error.", "data":str(e)})
        
# Get user post with comment, like, userdetails
def get_all_followers(request):
    try:
        # Get profile id
        profile_id = request.GET.get("id")
        try:
            # Get all data
            start=0
            end=8

            
            followers = UserFollowerModel.objects.filter(following_id=profile_id).select_related("following").prefetch_related(
                Prefetch("following__user_post"),
                Prefetch("following__user_comment"),
                Prefetch("following__user_like")
            ).annotate(
                comment_count=Count("following__user_comment", distinct=True),
                like_count=Count("following__user_like", distinct=True)
            ).order_by('-created_at')[start:end]
            
            # If user is follow data will not come
            if not followers:
                return JsonResponse({"code":404, "status":False, "msg":"The user didn't follow you.", "data":False})
            
            serialization =  FollowingUserPostWithRelatedDataSerializer(followers, many=True)
            
            return JsonResponse({"code":200, "status":True, "msg":"The user follow you.", "data":serialization.data})

        # First time do not found any entry that's time genereate exception
        except UserFollowerModel.DoesNotExist:
            return JsonResponse({"code":404, "status":False, "msg":"The user didn't follow you.", "errors":False})
    
    except Exception as e:
            return JsonResponse({"code":500, "status":False, "msg":"Internal Server Error.", "errors":str(e)})