# Create encrypt value for save the hacker
from cryptography.fernet import Fernet, InvalidToken
from django.conf import settings

# Token library
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken

# This library us for default image create
from PIL import Image, ImageDraw, ImageFont
from django.core.files.base import ContentFile
import base64
from io import BytesIO
import random

class GeneralFunction:
    # Encrypt
    def encrypt(data):
        # get fernet_key from settings.py
        fernet = Fernet(settings.FERNET_KEY)
        # convert the email to encrypt value
        return fernet.encrypt(str(data).encode()).decode()

    # Decrypt
    def decrypt(data):
        try:
            # Get fernet_key from settings.py
            fernet = Fernet(settings.FERNET_KEY)
            # Dcrypt the comming encrypted value
            return fernet.decrypt(data.encode()).decode()
        
        # This works when the email is not encrypted.
        except InvalidToken:
            return False

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
