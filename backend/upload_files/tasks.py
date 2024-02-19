from celery import shared_task

from api.models import File


@shared_task
def downloaded_files(id):
    """
    Celery-задача меняющая после окончания
    поле processed модели File на True.
    """
    file = File.objects.get(id=id)
    file.processed = True
    file.save()
