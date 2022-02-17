import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "aps_shared_farm.settings")

app = Celery("aps_shared_farm")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
