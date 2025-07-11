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
import json
import os

# This library us for default image create
from PIL import Image, ImageDraw, ImageFont

# Token library
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken

# Developer models and serializer
from user_auth.serializers import UserRegisterSerializer, UserPWDChangeSerializer
from user_auth.models import User

# Create encrypt value for save the hacker
from cryptography.fernet import Fernet, InvalidToken
from django.conf import settings

# Create token for the user
def get_tokens_for_user(user):
    if not user.is_active:
      raise AuthenticationFailed("User is not active")

    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

# Create user default image
def generate_avatar(initials="AB", size=256, font_size=100, output_dir="avatars"):
    os.makedirs(output_dir, exist_ok=True)

    background_colors = [
        "#F44336", "#E91E63", "#9C27B0", "#3F51B5", "#2196F3",
        "#009688", "#4CAF50", "#FF9800", "#795548"
    ]

    bg_color = random.choice(background_colors)

    img = Image.new('RGB', (size, size), bg_color)
    draw = ImageDraw.Draw(img)

    mask = Image.new('L', (size, size), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, size, size), fill=255)

    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except IOError:
        font = ImageFont.load_default()

    text_width, text_height = draw.textsize(initials, font=font)
    position = ((size - text_width) / 2, (size - text_height) / 2 - 10)
    draw.text(position, initials, fill='white', font=font)

    final_img = Image.new("RGB", (size, size))
    final_img.paste(img, mask=mask)

    file_path = os.path.join(output_dir, f"{initials}_avatar.png")
    final_img.save(file_path)

    return file_path

# Login
class UserLogin(APIView):
    # Login
    def post(self, request):
        try:
            # Validate user exits or not.
            user = User.objects.get(username=request.data.get("username"))
        except User.DoesNotExist:
                return Response({"code":404, "status":False, "msg":"No account was found with this username.", "error": ""})

        try:
            
            # Check password is carrect or not
            password = check_password(request.data.get("password"), user.password)

            if not password:
                return Response({"code":400, "status":False, "msg":"Passwords do not match.", "error": ""})
            
            # Call jwt function for create token
            token = get_tokens_for_user(user)
            
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
            return Response({"code":500, "status":False, "msg":"Internal server error", "error": f"Username field may not be blank that's why {str(e)}"})

    # This data use for whole program to work.
    def get(self, request):
        try:
            token = RefreshToken(request.COOKIES.get("refresh_token"))
            user = User.objects.get(id=token["user_id"])

            if user:
                # Make data for user
                user = {
                    "userId":user.id,
                    "userName":user.username,
                    "userImg":user.img
                }

                return Response({"code":200, "status":True, "msg":"Data found.", "data":user})

        except User.DoesNotExist as e:
            return Response({"code":404, "status":False, "msg":"No data was found with this username id.", "error": ""})

    # Logout  
    def put(self, request):
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
                # get fernet_key from settings.py
                fernet = Fernet(settings.FERNET_KEY)
                # convert the email to encrypt value
                encry_email = fernet.encrypt(str(serializer.data['email']).encode()).decode()

                return Response({"code":200, "status":True, "msg":"Registration complete. Please check your email for next steps", "data":encry_email})
            else:
                return Response({"code":400, "status":False, "msg":"Something went wrong", "error": ""})

        return Response({"code":400, "status":False, "msg":"Something went wrong", "error":serializer.errors})
 
    # Check for valid otp
    def get(self, request, format=None):
        try:
            # Get fernet_key from settings.py
            fernet = Fernet(settings.FERNET_KEY)

            # Dcrypt the comming encrypted value
            email = fernet.decrypt(request.GET.get("email").encode()).decode()

            # Get verified user data using email and otp
            user = User.objects.get(
                email=email,
                otp_code=request.GET.get("otp")
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
            # Get fernet_key from settings.py
            fernet = Fernet(settings.FERNET_KEY)

            # Dcrypt the comming encrypted value
            email = fernet.decrypt(request.data.get("email").encode()).decode()

            # Validate user exits or not
            user = User.objects.get(email=email)

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
        except IntegrityError:
            return Response({"code":400, "status":False, "msg":"This username is used already.", "error":""})
              
# Get user by email
def user_details(request):
    # Get fernet_key from settings.py
    fernet = Fernet(settings.FERNET_KEY)

    # Dcrypt the comming encrypted value
    email = fernet.decrypt(request.GET.get("email").encode()).decode()

    try:
        user = User.objects.get(email=email)
        if not user:
            return JsonResponse({"code":404, "status":False, "msg":"User doesn't exists.", "error": ''})
        
        return JsonResponse({"code":200, "status":True, "msg":"Change your username and password", "data":user.username})
    
    except Exception as e:
        return JsonResponse({"code":404, "status":False, "msg":"The OTP you entered is incorrect", "error": e})

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
        return JsonResponse({"code":500, "status":False, "msg":"Internal server error", "error": f"Failed to send email: {str(e)}"})
    
# Genereate new otp
def new_otp(request):
    # When direct api call set email value from the request.body
    # and when register function calls set email value using request.
    email = ''
    try:
        # data = json.loads(request.body)
        # email = data.get("email")

        # Get fernet_key from settings.py
        fernet = Fernet(settings.FERNET_KEY)

        # Dcrypt the comming encrypted value.
        email = fernet.decrypt(request.GET.get("email").encode()).decode()

    # This works when the email is not encrypted.
    except InvalidToken:
        email = request.GET.get("email")

    # When the email come from serializer data.
    except:
        email = request.data.get("email")

    try:
        # Generate otp.
        otp = random.randint(100000, 999999)

        # Update otp in table.
        save_otp = User.objects.get(email=email)
        save_otp.otp_code = otp
        save_otp.save()

        # Send email.
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
                
        # Get fernet_key from settings.py
        fernet = Fernet(settings.FERNET_KEY)
        # Convert the email to encrypt value.
        encry_email = fernet.encrypt(str(email).encode()).decode()
        
        return JsonResponse({"code":200, "status":True, "msg":"Your OTP has been sent to your email! Please check it.", "data":encry_email})
    
    except Exception as e:
        return JsonResponse({"code":500, "status":False, "msg":"Internal server error", "error": f"Failed to send email: {str(e)}"})

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