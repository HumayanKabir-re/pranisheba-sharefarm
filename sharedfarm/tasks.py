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
