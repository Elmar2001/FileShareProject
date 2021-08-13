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
        days7 = uploaded + timedelta(days=7)  # add 7 days to the uploaded date
        days7 = days7.replace(tzinfo=utc)

        now = datetime.now()
        now = now.replace(tzinfo=utc)

        if now > days7:  # if it's past 7 days delete the file
            File.objects.filter(pk=f.pk).delete()
