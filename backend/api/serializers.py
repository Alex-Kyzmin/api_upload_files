from rest_framework import serializers

from api.models import File


class FileSerializers(serializers.ModelSerializer):
    """Сериализатор для загрузки/демонстрации файлов"""
    class Meta:
        model = File
        fields = (
            'file',
            'uploaded_at',
            'processed',
        )
        read_only_fields = (
            'uploaded_at',
            'processed',
        )
