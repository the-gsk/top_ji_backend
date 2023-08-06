from django.urls import path
from .views import *


urlpatterns = [
    path('signup/', UserSignupView.as_view(), name='user-signup'),
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('get-otp/', GetUserOtpView.as_view(), name='user-otp'),
    
]