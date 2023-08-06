from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from users.models import User, UserOtp
from users.user_utils import create_otp

class UserSignupSerializer(serializers.ModelSerializer):
    # password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    name = serializers.CharField(required=True,source='first_name')

    class Meta:
        model = User
        fields = ['mobile_number', 'name']


class UserLoginSerializer(serializers.Serializer):
    mobile_number = serializers.CharField()
    otp = serializers.CharField()

    def validate(self, data):
        mobile_number = data.get('mobile_number')
        otp = data.get('otp')

        # Validate the OTP
        try:
            user_otp = UserOtp.objects.filter(user__mobile_number=mobile_number)
            if not user_otp.exists():
                raise serializers.ValidationError({"mobile_number":"Invalid Mobile Number. Please try again."})
            user_otp = user_otp.last()
            if not user_otp.otp == otp:
                raise serializers.ValidationError({"otp":"Invalid OTP. Please try again."})
            elif not user_otp.is_valid:
                raise serializers.ValidationError({"otp":"This Otp is Expired"})
            elif user_otp.is_verified:
                raise serializers.ValidationError({"otp":"Otp is Used, Please Genrate OTP Again"})
            
            user_otp.is_verified = True
            user_otp.save()

        except UserOtp.DoesNotExist:
            raise serializers.ValidationError('Invalid OTP. Please try again.')

        data['user'] = user_otp.user
        return data
    
class UserOtpSerializer(serializers.Serializer):
    mobile_number = serializers.CharField()

    def validate(self, data):
        mobile_number = data.get('mobile_number')

        # Validate the mobile_number
        try:
            user = User.objects.get(mobile_number=mobile_number)
            otp = create_otp(user)
            print(otp)
        except:
            raise serializers.ValidationError('Invalid Mobile Number. Please try again.')

        data['otp'] = otp
        print(data)
        return data