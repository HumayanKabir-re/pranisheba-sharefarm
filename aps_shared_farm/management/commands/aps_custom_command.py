from django.core.management.base import BaseCommand, CommandError
import json
import requests
from django.conf import settings
from core.models import Setting
from sharedfarm.models import HmsCattle


def get_hms_token():
    authorization = Setting.objects.get(slug='hms-token')
    return authorization.option_value


def hms_cattle_list():
    try:
        authorization = get_hms_token()
        headers = {'content-type': 'application/json', 'Authorization': f'{authorization}'}
        res = requests.get(f"{settings.HMS_URL}/hmsapi/cow/?farm__category=SHARE_FARMING&is_unassigned=True",
                           headers=headers)
        res_json = res.json()
        # http://shurjohms.com/hmsapi/cow/?farm__category=SHARE_FARMING
        return res_json
    except Exception as e:
        return e


def update_hms_cow(cow_list):
    for each_cow in cow_list:
        print(each_cow['id'])
        obj, created = HmsCattle.objects.update_or_create(
            cow_id=each_cow['id'],
            cow_name=each_cow['cow_name'],
            ear_tag=each_cow['ear_tag'],
            farm_id=each_cow['farm']['id'],
            farm_name=each_cow['farm']['name'],
            farm_no=each_cow['farm']['farm_no'],
            defaults={'cow_id': each_cow['id']},
        )
        if each_cow['id'] == 345:
            break


class Command(BaseCommand):
    help = "A description of the command"

    def handle(self, *args, **options):
        self.stdout.write("My sample command just ran.")  # NEW

        cow_list = hms_cattle_list()
        update_hms_cow(cow_list)
        print('cow obj created!')

        # self.stdout.write(f'{res.json()}')  # NEW


# location /media/ {
#     #alias /var/lib/docker/volumes/pranisheba-sharedfarm_media_volume/_data/;
#     proxy_pass          http://localhost:8080;
# proxy_read_timeout  90;
# }
