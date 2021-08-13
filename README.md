# FileShareProject v0.1
Basic file sharing app in Django and Celery (redis)

Files older than 7 days get deleted by a Celery task

## Credentials from the free elephantsql acc are not removed.

To start celery:
`celery --app FileShareProject worker --beat --loglevel=INFO`

to start the web app: `python manage.py runserver`

