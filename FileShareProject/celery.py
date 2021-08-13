import os

from celery import Celery, shared_task
from celery.schedules import crontab


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

print("CELERY.PY")

app.conf.beat_schedule = {
    # Execute the Speed Test every 10 minutes
    'check-db-every-5min': {
        'task': 'share.tasks.check_db',
        'schedule': 5,
    },
}
# crontab(minute='*/2')
# app.conf.beat_schedule = {
#     'add-every-30-seconds': {
#         'task': 'tasks.checkdb',
#         'schedule': 30.0,
#     },
# }
app.conf.timezone = 'UTC'
