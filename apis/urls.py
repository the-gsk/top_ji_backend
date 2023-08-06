from django.urls import path,include
from .user_auth import urls as auth_url
from .ads import urls as ads_url

urlpatterns = [
    path('user/', include(auth_url)),
    path('ads/', include(ads_url)),
]
