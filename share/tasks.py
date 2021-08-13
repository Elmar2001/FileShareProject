from celery import shared_task
from .models import File

from datetime import datetime, timedelta
import pytz


@shared_task
def check_db():
    utc = pytz.UTC
    files = File.objects.all()

    for f in files:
        uploaded = f.upload_date.replace(tzinfo=utc)
        days7 = uploaded + timedelta(minutes=2)
        days7 = days7.replace(tzinfo=utc)

        now = datetime.now()
        now = now.replace(tzinfo=utc)

        if now > days7:
            File.objects.filter(pk=f.pk).delete()
