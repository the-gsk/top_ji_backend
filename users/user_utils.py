from .models import UserOtp,random_pin


def create_otp(user):
    # Create an OTP entry for the user
    user_otp = UserOtp.objects.create(user=user,otp=random_pin())
    return user_otp.otp