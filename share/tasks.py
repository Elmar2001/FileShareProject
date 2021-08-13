from celery import shared_task
from celery.schedules import crontab
from .models import File
from datetime import datetime
from datetime import timedelta

# @app.on_after_configure.connect
# def setup_periodic_tasks(sender, **kwargs):
#     # Calls test('hello') every 10 seconds.
#     sender.add_periodic_task(10.0, checkdb(), name='add every 10')

print("TASKS.PY")

@shared_task(name="check_db")
def check_db():
    print("inside CHECK_DB")
    files = File.objects.all()

    for f in files:
        if f.upload_date > datetime.now() + timedelta(minutes=1):
            print('DELETED: ')
            print(f)
            File.objects.filter(f).delete()

