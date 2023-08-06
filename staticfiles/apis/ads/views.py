from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from users.models import User,AdsCollectSliver
from users.user_utils import create_otp
from users.ads_utils import fetch_silver_collective, watch_silver_collective
from .serilizers import SilverCollectiveSerializer
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone


No_AdsCollectSliver = 10
Time_AdsCollectSliver = 1



class AdsCollectSliverView(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    model = AdsCollectSliver
    serializer_class = SilverCollectiveSerializer

    def get(self,request):
        ruser = request.user
        acs = fetch_silver_collective(ruser)
        serializer = self.serializer_class(instance=acs,many=True)
        return Response (serializer.data,status=status.HTTP_200_OK)
    
    def patch(self, request):
        ruser = request.user
        instance = ruser.users_ads_collect_silver
        data = request.data

        sl_no = data.get('sl_no')
        ads_information = data.get('ads_information')

        if not sl_no:
            return Response({"sl_no": "this fields is required!"},400)
        if not str(sl_no).isdigit():
            return Response({"sl_no": "this fields must be in integer!"},400)
        if not instance.filter(sl_no=int(sl_no)).exists():
            return Response({"sl_no": f"If You Are Bad, I Am Your Dad!. Please send proper 'sl_no'. "},400)
        
        a_instance = instance.get(sl_no=int(sl_no))

        if a_instance.is_watched:
            return Response({"sl_no": f"This Ads is Already Watched!. Please send proper 'sl_no'. "},400)
        if not a_instance.is_active:
            return Response({"sl_no": f"This Ads is not Activate Yet!. Please send proper 'sl_no'. "},400)
        if a_instance.active_at > timezone.now():
            return Response({"sl_no": f"This Ads is not Ready to Watch!. Please send proper 'sl_no'. "},400)
       
        watch_silver_collective(ruser,sl_no,ads_information)

        serializer = self.serializer_class(instance=instance,many=True)

        # serializer = self.serializer_class(instance, data=request.data, partial=True)
        # if serializer.is_valid():
        #     serializer.save()
        #     return Response(serializer.data)
        return Response(serializer.data)


    # def post(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     user = serializer.validated_data['user']
    #     token, created = Token.objects.get_or_create(user=user)
    #     return Response({'token': token.key}, status=status.HTTP_200_OK)
    
