from django.contrib import admin
from django.contrib.auth.models import Group

# настройка админ-зоны для импортируемой модели
from api.models import File


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'uploaded_at',
        'processed',
    )
    search_fields = (
        'id',
        'processed',
    )


admin.site.unregister(Group)
