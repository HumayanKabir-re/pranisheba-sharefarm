from celery import shared_task
from celery.schedules import crontab
# from celery import periodic_task
from aps_shared_farm.celery import app
from celery.schedules import crontab
import requests
import json


@shared_task
# @periodic_task(run_every=crontab(), name='create_organisation')
def sample_task():
    print("The sample task jussdfsdft ran.")


def hms_get_auth_token():
    try:
        data = {"username": "sharedfarm",
                "password": "AhXxdAlGdXPtoUZC",
                "fcm_token": "testToken"}
        res = requests.put(f"http://shurjohms.com/api-token-auth/", data=json.dumps(data))
        # headers = {'content-type': 'application/json'}
        # res = requests.post(f"{SmaxtecConfig.smaxtec_url}/users/session_token?user={email}&password={password}", headers=headers)
        token_json = res.json()
        # return token_json
        token = token_json['token']
        return token_json
    except Exception as e:
        return e


@app.task
def add(x, y):
    z = x + y
    print(z)


app.conf.beat_schedule = {
    'add-every-30-seconds': {
        'task': 'tasks.add',
        "schedule": crontab(minute="*/1"),
        'args': (16, 16)
    },
}

from pyfcm import FCMNotification
from core.models import UserFcmToken
from django.conf import settings


@app.task
def fcm_notify(receiver_list, data_message):
    push_service = FCMNotification(api_key=settings.FCM_API_KEY)
    # receiver_list = UserFcmToken.objects.filter(
    #     user__phone="01682803595").values_list('fcm_token', flat=True)
    # data_message = {
    #     "Nick": "Mario",
    #     "body": "great match!",
    #     "Room": "PortugalVSDenmark"
    # }
    print(receiver_list)
    print(data_message)
    if receiver_list:
        registration_ids = receiver_list
        message_title = "New Fund Opportunity Alert!"
        result = push_service.notify_multiple_devices(registration_ids=registration_ids,
                                                      message_title=message_title,
                                                      message_body=data_message["name"],
                                                      data_message=data_message)
        # result = push_service.multiple_devices_data_message(registration_ids=registration_ids, data_message=data_message)

                    # push_service.multiple_devices_data_message()

        pass
    else:
        result = None

    return result
