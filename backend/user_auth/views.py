from django.contrib.auth.hashers import make_password, check_password
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework import status
from rest_framework.views import APIView
from django.core.mail import EmailMultiAlternatives
from django.utils import timezone
import random
import string
import json

# Token library
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken

# Developer models and serializer
from user_auth.serializers import UserRegisterSerializer, UserPWDChangeSerializer
from user_auth.models import User

# Create token for the user
def get_tokens_for_user(user):
    if not user.is_active:
      raise AuthenticationFailed("User is not active")

    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

# Login
class UserLogin(APIView):
    # Login
    def post(self, request):
        try:
            # Validate user exits or not.
            user = User.objects.get(username=request.data.get("username"))

            # If user does not exits.
            if not user:
                return Response({"code":404, "status":False, "msg":"No account found with this email.", "error": ""})

            # Check password is carrect or not
            password = check_password(request.data.get("password"), user.password)

            if not password:
                return Response({"code":400, "status":False, "msg":"Entered passwords are not the same.", "error": ""})
            
            # Call jwt function for create token
            token = get_tokens_for_user(user)
            
            #  Create response with set_cookie function
            response = Response({"code":200, "status":True, "msg":"Registration complete. Please check your email for next steps", "data":token})
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
            return Response({"code":500, "status":False, "msg":"Internal server error", "error": f"Username field may not be blank that's why {str(e)}"})

    # Logout  
    def get(self, request):
        try:
            access_token = request.COOKIES.get("access_token")
            refresh_token = request.COOKIES.get("refresh_token")

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
                "error": f"Your session was not deleted: {str(e)}"
            })

# Authenticatioin class start
class UserAuthentication(APIView):
    # Register
    def post(self, request, format=None):
        
        # Generate a rundum string for username
        username = '' . join(random.sample((string.ascii_uppercase), 8))

        # Get data from the api
        data = {
            'email': request.data.get('email'),
            'username': username
        }

        # This line sent data to serialization.
        serializer = UserRegisterSerializer(data=data)

        # Validate data for empty or wrong value
        if serializer.is_valid():
            # Create a new user
            serializer.save()

            # Call for the new otp function for save otp in table
            response = new_otp(serializer)

            # Send response accourding to status
            if response.status_code == 200:
                return Response({"code":200, "status":True, "msg":"Registration complete. Please check your email for next steps", "data":serializer.data})
            else:
                return Response({"code":400, "status":False, "msg":"Something went wrong", "error": ""})

        return Response({"code":400, "status":False, "msg":"Something went wrong", "error":serializer.errors})
 
    # Check for valid otp
    def get(self, request, format=None):
        try:
            # Get verified user data using email and otp
            user = User.objects.get(
                email=request.data.get("email"),
                otp_code=request.data.get("otp")
            )
            
            # This code works if otp_expire code timing less than 10 minuts so its give the data other whise otp expire error msg
            if not timezone.now() <= user.otp_expire + timezone.timedelta(minutes=10):
                return Response({"status": False, "msg": "Your otp has expired"})

            serializer = UserRegisterSerializer(user)

            return Response({"code":200, "status":True, "msg":"Change your username and password", "data":serializer.data})
        except User.DoesNotExist:
            return Response({"code":404, "status":False, "msg":"The OTP you entered is incorrect", "error": ''})

    # Change password
    def put(self, request, format=None):
        try:
            # Validate user exits or not
            user = User.objects.get(email=request.data.get("email"))

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
                return Response({"code":400, "status":False, "msg":"Something went wrong", "error":serializer.errors})
        except Exception as e:
            return Response({"code":500, "status":False, "msg":"Internal server error", "error": f"Email field may not be blank that's why {str(e)}"})

 # Genereate new otp

def new_otp(request):
    # When direct api call set email value from the request.body
    # and when register function calls set email value using request.data
    
    email = ''
    try:
        data = json.loads(request.body)
        email = data.get("email")
    except:
        email = request.data.get("email")

    try:
        # Generate otp
        otp = random.randint(100000, 999999)

        # Update otp in table
        save_otp = User.objects.get(email=email)
        save_otp.otp_code = otp
        save_otp.save()

        # Send email
        subject = 'You received an OTP to change your LinkUP password.'
        msg = f'''
            <p>Your OTP is <strong>{otp}</strong> to change your password.</p>
            <p>The OTP will expire in 10 minutes.</p>
        '''
        email_from = 'mohitmishra.falna850@yahoo.com'
        to = email

        user_msg = EmailMultiAlternatives(subject, msg, email_from, [to])
        user_msg.content_subtype = 'html'
        user_msg.send()
        
        return JsonResponse({"code":200, "status":True, "msg":"Please check your email for next steps", "data":email})
    
    except Exception as e:
        return JsonResponse({"code":500, "status":False, "msg":"Internal server error", "error": f"Failed to send email: {str(e)}"})
    
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
                    "error": str(e),
                    "data": False
                })

                # Delete the cookie from the response
                response.delete_cookie("access_token")
                response.delete_cookie("refresh_token")

                # If token is expired or invalid, this line will raise an exception
                return response
        
        # User is not available
        return Response({"code":401, "status":False, "msg":"Refresh token invalid.", "data":False})