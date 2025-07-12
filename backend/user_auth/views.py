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

# This library us for default image create
from PIL import Image, ImageDraw, ImageFont
from django.core.files.base import ContentFile
import base64
from io import BytesIO


# Token library
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken

# Developer models and serializer
from user_auth.serializers import UserRegisterSerializer, UserPWDChangeSerializer
from user_auth.models import User
from user_followers.models import UserFollowerModel

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
def generate_avatar(initials="PM", size=256, font_size=150, output_dir="user_avatars"):
    # If folder is not exist so its create a new folder
    # os.makedirs(output_dir, exist_ok=True)

    # Creates a random color for img background
    background_colors = "#" + str(random.randint(100000, 999999))

    # This creates a object for the new image with size and background color
    img = Image.new('RGB', (size, size), background_colors)
    # This drow the img accourding to new image object
    draw = ImageDraw.Draw(img)

    # This creates a object for the new image mask
    mask = Image.new('L', (size, size), 0)
    # This drow the img accourding to new image mask object
    ImageDraw.Draw(mask).ellipse((0, 0, size, size), fill=255)

    try:
        # If font fammily is available so use it
        font = ImageFont.truetype("arial.ttf", font_size)
    except IOError:
        # Otherwise use default font familly
        font = ImageFont.load_default()

    # This line create a box for the our character
    bbox = draw.textbbox((0, 0), initials, font=font)
    # This define height and width accourding to cordinate of "x"
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    # Now this line create possition for align center horizontal and vertical of the image
    position = ((size - text_width) / 2, (size - text_height) / 2 - 10)

    # This line creates text with color white, font family and position 
    draw.text(position, initials, fill='white', font=font)

    # This line creats a object which is create a final image
    final_img = Image.new("RGB", (size, size))
    # Here is creating image with the character and mask
    final_img.paste(img, mask=mask)    
    
    # Create a buffer object for store image
    buffer = BytesIO()
    # In buffer object store image as temp
    final_img.save(buffer, format="PNG")
    # Get image reference from the buffer object
    image_png = buffer.getvalue()
    
    # First convert the file into Files object and return a response
    return ContentFile(image_png, name=f"{initials}_avatar.png")

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
            return Response({"code":500, "status":False, "msg":"Internal server error", "errors": f"Username field may not be blank that's why {str(e)}"})

    # This data use for whole program to work.
    def get(self, request):
        try:
            token = RefreshToken(request.COOKIES.get("refresh_token"))
            user = User.objects.get(id=token["user_id"])
            print(user.img.url)
            if user:
                followers = UserFollowerModel.objects.filter(follower_id = token["user_id"]).count()
                print(followers)
                # Make data for user
                user = {
                    "userId": user.id,
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
            img_path = generate_avatar(initial.upper())

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
                serializer.save()

                # # Call for the new otp function for save otp in table
                response = new_otp(serializer)

                # Send response accourding to status
                if response.status_code == 200:
                    # get fernet_key from settings.py
                    fernet = Fernet(settings.FERNET_KEY)
                    # convert the email to encrypt value
                    encry_email = fernet.encrypt(str(serializer.data['email']).encode()).decode()

                return Response({"code":200, "status":True, "msg":"Registration complete. Please check your email for next steps", "data":encry_email})
            
            return Response({"code":400, "status":False, "msg":"Something went wrong", "errors":serializer.errors})
        except Exception as e:
            return Response({"code":500, "status":False, "msg":"Something went wrong", "errors":""})
 
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
            return Response({"code":404, "status":False, "msg":"The OTP you entered is incorrect", "errors": ''})

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
                return Response({"code":400, "status":False, "msg":"Something went wrong", "errors":serializer.errors})
        except IntegrityError:
            return Response({"code":400, "status":False, "msg":"This username is used already.", "errors":""})
              
# Get user by email
def user_details(request):
    # Get fernet_key from settings.py
    fernet = Fernet(settings.FERNET_KEY)

    # Dcrypt the comming encrypted value
    email = fernet.decrypt(request.GET.get("email").encode()).decode()

    try:
        user = User.objects.get(email=email)
        if not user:
            return JsonResponse({"code":404, "status":False, "msg":"User doesn't exists.", "errors": ''})
        
        return JsonResponse({"code":200, "status":True, "msg":"Change your username and password", "data":user.username})
    
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