from .models import AdsCollectSliver,User
from django.utils import timezone
from rest_framework import serializers
from datetime import timedelta

No_AdsCollectSliver = 10
Time_AdsCollectSliver = 1



def create_silver_collective(no_,user):
    try:
        acs = AdsCollectSliver.objects.filter(user=user).order_by('-sl_no').first()
        isl = acs.sl_no
    except:
        isl = 0

    for i in range(no_):
        AdsCollectSliver.objects.create(sl_no=(i+isl+1),user=user)
    return True

def daily_reset_silver_collective(user,lcount):
    acs = AdsCollectSliver.objects.filter(user=user).order_by('sl_no')[:lcount]
    for ac in acs:
        if ac.sl_no == 1:
            ac.is_active = True
            ac.active_at = timezone.now()
            ac.is_ready = True

        else:
            ac.is_active = False
            ac.active_at = None
            ac.is_ready = False
            ac.is_watched = False
            ac.watch_at = None
            ac.ads_information = None
        ac.save()
    return True

def is_ready_to_watch(acs):
    acs = acs.filter(is_active=True,active_at__lte=timezone.now()).order_by('sl_no')
    if acs.exists():
        ac = acs.last()
        ac.is_ready = True
        ac.save()

            
def fetch_silver_collective(user):
    acount = No_AdsCollectSliver
    acs = AdsCollectSliver.objects.filter(user=user).order_by('id')
    if not acs.exists():
        create_silver_collective(acount,user)
    if acs.count() < acount:
        lcount = acount - acs.count()
        create_silver_collective(lcount,user)
    if (acs.first()).active_at.date() < timezone.now().date():
        daily_reset_silver_collective(user,acount)
    is_ready_to_watch(acs)

    return acs


def watch_silver_collective(user,sl_no,ads_information=None):
    sl_no = int(sl_no)
    i_min = int(Time_AdsCollectSliver)
    acs = AdsCollectSliver.objects.filter(user=user).order_by('id')
    for ac in acs:
        if ac.sl_no == sl_no:
            ac.is_active = False
            ac.is_ready = False
            ac.is_watched = True
            ac.watch_at = timezone.now()
            ads_information = ads_information
        elif ac.sl_no == sl_no+1:
            ac.is_active = True 
            ac.active_at = timezone.now() + timedelta(minutes=i_min)
        ac.save()
    return True

