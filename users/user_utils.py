from .models import UserOtp,random_pin
from rest_framework.authtoken.models import Token


def create_otp(user):
    # Create an OTP entry for the user
    user_otp = UserOtp.objects.create(user=user,otp=random_pin())
    return user_otp.otp

def get_or_create_token(user):
    token, created = Token.objects.get_or_create(user=user)
    return token.key
