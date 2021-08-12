import os

from celery import Celery, shared_task
from celery.schedules import crontab

from share.models import File
from datetime import datetime
from datetime import timedelta

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FileShareProject.settings')

app = Celery('FileShareProject')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')


# @shared_task(name="check_db")
# def print_message(message, *args, **kwargs):
#     files = File.objects.all()
#
#     for f in files:
#         if f.upload_date > datetime.now() + timedelta(days=7):
#             File.objects.filter(f).delete()


app.conf.beat_schedule = {
    # Execute the Speed Test every 10 minutes
    'check-db-every-5min': {
        'task': 'check_db',
        'schedule': crontab(minute='*/5'),
    },
}