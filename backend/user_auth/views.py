from django.contrib.auth.hashers import make_password, check_password
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework import status
from rest_framework.views import APIView
from django.core.mail import EmailMultiAlternatives
from django.db import IntegrityError
from django.utils import timezone
import random
import string

# Token library
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken

# Developer models and serializer
from user_auth.serializers import UserRegisterSerializer, UserPWDChangeSerializer, UserSerializer
from user_auth.models import User
from user_followers.models import UserFollowerModel, UserBlockModel
from user_posts.models import UserPostModels

# General function import
from linkup.general_function import GeneralFunction

# Login
class UserLogin(APIView):
    # Login
    def post(self, request):
        try:
            # Validate user exits or not.
            user = User.objects.get(username=request.data.get("username"))
        except User.DoesNotExist:
                return Response({"code":404, "status":False, "msg":"No account was found with this username.", "errors": ""})

        try:            
            # Check password is carrect or not
            password = check_password(request.data.get("password"), user.password)

            if not password:
                return Response({"code":400, "status":False, "msg":"Passwords do not match.", "errors": ""})
            
            # Call jwt function for create token
            token = GeneralFunction.get_tokens_for_user(user)
            
            #  Create response with set_cookie function
            response = Response({"code":200, "status":True, "msg":"Login successful. Session started — enjoy!", "data":token})
            response.set_cookie(
                key="access_token",
                value=str(token.get("access")),
                httponly=True,
                secure=True,
                samesite='Lax'
            )

            response.set_cookie(
                key="refresh_token",
                value=token.get("refresh"),
                httponly=True,
                secure=True,
                samesite='Lax'
            )

            # Send response accourding to status
            return response
        
        except Exception as e:
            print(e)
            return Response({"code":500, "status":False, "msg":"Internal server error", "errors": f"Username field may not be blank that's why {str(e)}"})

    # This data use for whole program to work.
    def get(self, request):
        try:
            # Get current user data
            token = RefreshToken(request.COOKIES.get("refresh_token"))
            user = User.objects.get(id=token["user_id"])
            
            if user:
                followers = UserFollowerModel.objects.filter(follower_id = token["user_id"]).count()
                
                # Make data for user
                user = {
                    "userId": GeneralFunction.encrypt(user.id),
                    "user": user.id,
                    "userName": user.username,
                    "userImg": request.build_absolute_uri(user.img.url) if user.img else None,
                    "userCover": request.build_absolute_uri(user.banner.url) if user.banner else None,
                    "followers": followers if followers else None
                }

                return Response({"code":200, "status":True, "msg":"Data found.", "data":user})

        except User.DoesNotExist as e:
            return Response({"code":404, "status":False, "msg":"No data was found with this username id.", "errors": ""})

    # Logout  
    def put(self, request):
        try:
            response = Response({
                "code": 200,
                "status": True,
                "msg": "Successfully logged out",
                "data": {}
            })

            # Delete the cookie from the response
            response.delete_cookie("access_token")
            response.delete_cookie("refresh_token")

            return response

        except Exception as e:
            return Response({
                "code": 500,
                "status": False,
                "msg": "Internal server error",
                "errors": f"Your session was not deleted: {str(e)}"
            })

# Authenticatioin class start
class UserAuthentication(APIView):
    # Register
    def post(self, request, format=None):
        try:
            # Generate a rundum string for username
            username = '' . join(random.sample((string.ascii_uppercase), 8))

            # Get first charactor from the email string
            initial = request.data.get("email")[0]

            # Call the function with required parameter
            img_path = GeneralFunction.generate_avatar(initial.upper())

            # Get data from the api
            data = {
                "email": request.data.get("email"),
                "username": username,
                "img": img_path
            }

            # This line sent data to serialization.
            serializer = UserRegisterSerializer(data=data)

            # Validate data for empty or wrong value
            if serializer.is_valid():
                # Create a new user
                save_data = serializer.save()
                
                # Reserialize data after user update
                serializer = UserRegisterSerializer(save_data)

                # Call for the new otp function for save otp in table
                response = new_otp(serializer)

                # Send response accourding to status
                if response.status_code == 200:
                    # Call general encryption function for encrypt value
                    encry_id = GeneralFunction.encrypt(serializer.data["id"])

                return Response({"code":200, "status":True, "msg":"Registration complete. Please check your email for next steps", "data":encry_id})
            
            return Response({"code":400, "status":False, "msg":"Something went wrong", "errors":serializer.errors})
        except Exception as e:
            return Response({"code":500, "status":False, "msg":"Something went wrong", "errors":""})
 
    # Check for valid otp
    def get(self, request, format=None):
        try:
            # Dcrypt the comming encrypted value
            user_id = GeneralFunction.decrypt(request.GET.get("id"))

            # Get verified user data using email and otp
            user = User.objects.get(
                id=user_id,
                otp_code=request.GET.get("otp")
            )
            
            # This code works if otp_expire code timing less than 10 minuts so its give the data other whise otp expire error msg
            if not timezone.now() <= user.otp_expire + timezone.timedelta(minutes=10):
                return Response({"status": False, "msg": "Your otp has expired"})

            serializer = UserRegisterSerializer(user)

            return Response({"code":200, "status":True, "msg":"Change your username and password", "data":serializer.data})
        except User.DoesNotExist:
            return Response({"code":404, "status":False, "msg":"The OTP you entered is incorrect", "errors": ''})

    # Change password
    def put(self, request, format=None):
        print(request.data)
        try:
            # Dcrypt the comming encrypted value
            user_id = GeneralFunction.decrypt(request.data.get("id"))

            # Validate user exits or not
            user = User.objects.get(id=user_id)

            # Create data
            data = {
                "username":request.data.get("username"),
                "password":make_password(request.data.get("password")),
            }

            # Set data for the partial update
            serializer = UserPWDChangeSerializer(user, data=data, partial=True)

            # Check data for empty
            if serializer.is_valid():
                serializer.save()

                return Response({"code":200, "status":True, "msg":"Success! Your password was changed. Log in to continue.", "data":serializer.data})
            else:
                return Response({"code":400, "status":False, "msg":"Something went wrong", "errors":serializer.errors})
        except IntegrityError:
            return Response({"code":400, "status":False, "msg":"This username is used already.", "errors":""})
              
# Get user by id
def user_details(request):
    try:
        # Dcrypt the comming encrypted value
        user_id = GeneralFunction.decrypt(request.GET.get("id"))
        
        # Get user
        user = User.objects.get(id=user_id)
        
        if not user:
            return JsonResponse({"code":404, "status":False, "msg":"User doesn't exists.", "errors": ''})
        
        # Serialize the data
        user_serialization = UserSerializer(user)

        return JsonResponse({"code":200, "status":True, "msg":"Change your username and password", "data":user_serialization.data})
    
    except Exception as e:
        return JsonResponse({"code":404, "status":False, "msg":"The OTP you entered is incorrect", "errors": e})

# Get profile data using id
def profile_details(request):

    try:
        # Get current user id
        token = RefreshToken(request.COOKIES.get("refresh_token"))

        # Dcrypt the comming encrypted value
        user_id = GeneralFunction.decrypt(request.GET.get("id"))

        # Get user
        user = User.objects.filter(id=user_id).first()

        # Let's find user is block or not
        blocked_user = UserBlockModel.objects.filter(blocker_id=user_id, blocked_id=token["user_id"]).first()

        # If user is blocked data will not come
        if blocked_user:         
            user = {
                "id":user.id,
                "banner":user.banner,
                "img":user.img,
                "username":user.username,
                "email":user.email,
            }
            serializer = UserSerializer(user)
            serialized_data = serializer.data
            serialized_data["block"] = True  # Add custom field here
            return JsonResponse({"code":403, "status":True, "msg":"You can't see this profile because the user blocked you", "data":serialized_data})
   
        # Get currint user followers
        followers = UserFollowerModel.objects.filter(follower_id = user_id).count()

        # Get currint user Following
        following = UserFollowerModel.objects.filter(following_id = user_id).count()

        # Get currint user posts
        posts = UserPostModels.objects.filter(user_id=user_id).count()

        # Serialize the user
        user_data = UserSerializer(user).data

        # Append additional data
        user_data.update({
            "followers": followers,
            "following": following,
            "posts": posts,
        })


        if not user:
            return JsonResponse({"code":404, "status":False, "msg":"User doesn't exists.", "errors": ''})
        
        return JsonResponse({"code":200, "status":True, "msg":"Change your username and password", "data":user_data})
    
    except Exception as e:
        return JsonResponse({"code":404, "status":False, "msg":"The OTP you entered is incorrect", "errors": e})

# Live username check
def check_username(request):
    try:
        # Capital letter to small letter
        username = request.GET.get('username', '').strip().lower()

        # Search query
        exists = User.objects.filter(username__iexact=username).exists()
        if not exists:
            return JsonResponse({"code":200, "status":True, "msg":{"msg":"Available", "textName":" text-green-600"}, "data":True})

        return JsonResponse({"code":200, "status":True, "msg":{"msg":"Username already taken", "textName":" text-red-600"}, "data":True})
    
    except Exception as e:
        return JsonResponse({"code":500, "status":False, "msg":"Internal server error", "errors": f"Failed to send email: {str(e)}"})
    
# Genereate new otp
def new_otp(request):
    user_id = 0

    # If request is come with data method using serialization
    if not hasattr(request, 'data'):
        # Dcrypt the comming encrypted value
        res = GeneralFunction.decrypt(request.GET.get("id"))

        if int(res) > 0:
            user_id = res
        else:
            user = User.objects.get(email=request.GET.get("id"))
            user_id = user.id
    else:
        user_id = request.data.get("id")

    try:
        # Generate otp.
        otp = random.randint(100000, 999999)

        # Update otp in table.
        save_otp = User.objects.get(id=user_id)
        save_otp.otp_code = otp
        save_otp.save()

        # Send email.
        subject = 'You received an OTP to change your LinkUP password.'
        msg = f'''
            <p>Your OTP is <strong>{otp}</strong> to change your password.</p>
            <p>The OTP will expire in 10 minutes.</p>
        '''
        email_from = 'mohitmishra.falna850@yahoo.com'
        to = save_otp.email

        user_msg = EmailMultiAlternatives(subject, msg, email_from, [to])
        user_msg.content_subtype = 'html'
        user_msg.send()

        # Convert the email to encrypt value.
        encry_id = GeneralFunction.encrypt(user_id)

        return JsonResponse({"code":200, "status":True, "msg":"Your OTP has been sent to your email! Please check it.", "data":encry_id})
    
    except Exception as e:
        return JsonResponse({"code":500, "status":False, "msg":"Internal server error", "errors": f"Failed to send email: {str(e)}"})

# This is use for check user validation from angular auth guard   
class UserTokenValidation(APIView):
    def post(self, request, format=None):
        # Get token
        refresh_token = request.COOKIES.get("refresh_token")
        accss_token = request.COOKIES.get("access_token")
        
        # Check token come or not
        if not refresh_token:
            return Response({"code":401, "status":False, "msg":"No refresh token found.", "data":False})

        # Check token come or not
        if not accss_token:
            return Response({"code":401, "status":False, "msg":"No access token found.", "data":False})
        
        # Get token original value
        ref_token = RefreshToken(refresh_token)

        # Varify user
        user = User.objects.get(id=ref_token['user_id'], is_active=True) # get id from refresh_token

        # when user did not come
        if user:
            # Check access token did not expire
            try:
                token = AccessToken(accss_token)
                return Response({"code":200, "status":True, "msg":"Valid user.", "data":True})            
            except Exception as e:
                # If token expired
                response = Response({
                    "code": 401,
                    "status": True,
                    "msg": "Access token expire.",
                    "errors": str(e),
                    "data": False
                })

                # Delete the cookie from the response
                response.delete_cookie("access_token")
                response.delete_cookie("refresh_token")

                # If token is expired or invalid, this line will raise an exception
                return response
        
        # User is not available
        return Response({"code":401, "status":False, "msg":"Refresh token invalid.", "data":False})