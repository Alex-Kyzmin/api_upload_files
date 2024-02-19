import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'upload_files.settings')

app = Celery('upload_files')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
app.conf.beat_schedule = {
    'upload-files': {
        'task': 'upload_files.tasks.downloaded_files',
        'schedule': crontab(minute="*/1"),
    },
}
app.conf.timezone = 'Europe/Moscow'
