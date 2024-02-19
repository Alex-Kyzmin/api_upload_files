from django.db import models


class File(models.Model):
    """Модель для загружаемых файлов"""
    file = models.FileField(
        verbose_name='Загружаемый файл',
        upload_to='media/downloaded_files',
    )
    uploaded_at = models.DateTimeField(
        verbose_name='Дата загрузки файла',
        auto_now_add=True,
    )
    processed = models.BooleanField(
        verbose_name='Статус обработки файла',
        default=False,
    )

    class Meta:
        ordering = ('uploaded_at',)
        verbose_name = 'Загруженные файлы'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'Файл {self.file.name} - загружен {self.uploaded_at.date()}'
