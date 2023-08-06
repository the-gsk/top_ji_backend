from django.urls import path
from .views import *


urlpatterns = [
    path('collect-silver/', AdsCollectSliverView.as_view(), name='collect-silver-coin'),
    
]