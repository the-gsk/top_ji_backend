from django.urls import path,include
from .views import *

urlpatterns = [
    # path('', LoginApi.as_view()),
    path('signup/', UserSignupView.as_view(), name='user-signup'),
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('get-otp/', GetUserOtpView.as_view(), name='user-otp'),
]
