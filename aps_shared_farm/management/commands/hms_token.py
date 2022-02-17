from django.core.management.base import BaseCommand, CommandError
import json
import requests
from django.conf import settings
from core.models import Setting


def hms_get_auth_token():
    try:
        data = {"username": settings.HMS_USERNAME,
                "password": settings.HMS_PASSWORD,
                "fcm_token": "testToken"}
        headers = {'content-type': 'application/json'}

        res = requests.post(f"{settings.HMS_URL}/api-token-auth/", data=json.dumps(data), headers=headers)
        token_json = res.json()
        token = token_json['token']
        obj, created = Setting.objects.update_or_create(
            option_name='hms token',
            option_value="Token " + token,
            defaults={'slug': 'hms-token'},
        )

        return obj
    except Exception as e:
        return e


class Command(BaseCommand):
    help = "A description of the command"

    def handle(self, *args, **options):
        self.stdout.write("My sample command just ran.")  # NEW

        token = hms_get_auth_token()
        print(token)
