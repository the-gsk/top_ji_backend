from django.urls import path,include
from .user_auth import urls as auth_url

urlpatterns = [
    path('user/', include(auth_url)),
]
