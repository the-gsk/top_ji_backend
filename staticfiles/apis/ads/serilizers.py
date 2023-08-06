from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from users.models import User, AdsCollectSliver
from users.user_utils import create_otp


class SilverCollectiveSerializer(serializers.ModelSerializer):

    class Meta:
        model = AdsCollectSliver
        exclude = ['id','user','created_at','updated_at']

    def update(self, instance, validated_data):
        instance.sl_no = validated_data.get('sl_no', instance.sl_no)
        # instance.ads_information = validated_data.get('ads_information', instance.ads_information)
        instance.save()
        return instance

