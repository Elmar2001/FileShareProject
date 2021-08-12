from celery import shared_task
from celery.schedules import crontab
from models import File
from datetime import datetime
from datetime import timedelta


@shared_task(name="check_db")
def print_message(message, *args, **kwargs):
    files = File.objects.all()

    for f in files:
        if f.upload_date > datetime.now() + timedelta(minutes=20):
            print('hiii')
            print(f)
            File.objects.filter(f).delete()
