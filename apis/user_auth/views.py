from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from users.models import User,UserOtp
from users.user_utils import create_otp
from .serilizers import UserSignupSerializer,UserLoginSerializer,UserOtpSerializer
from rest_framework.authtoken.models import Token

class UserSignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSignupSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        otp = create_otp(user)

        response_data = {
            'message': 'User registered successfully.',
            'user_id': user.id,
            'otp': otp,  # Include the OTP in the response
        }
        return Response(response_data, status=status.HTTP_201_CREATED)



class UserLoginView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=status.HTTP_200_OK)
    
class GetUserOtpView(generics.GenericAPIView):
    serializer_class = UserOtpSerializer


    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # user = serializer.validated_data['otp']
        return Response(serializer.validated_data, status=status.HTTP_200_OK)