from rest_framework import generics, status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response

from api.models import File
from api.serializers import FileSerializers
from upload_files.tasks import downloaded_files


class FileLoadView(generics.CreateAPIView):
    """
    Представления для эндпойнта 'upload'.
    Принимает только POST-запросы для загрузки файлов.
    """
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = FileSerializers

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        """
        Реализуем Celery-задачу для асинхронной обработки файла.
        """
        file = serializer.save()
        downloaded_files.delay(file.id)


class ListFileView(generics.ListAPIView):
    """
    Представления для эндпойнта 'files'.
    Принимает только GET-запросы для демонстрации
    всех загруженных файлов в приложении.
    """
    queryset = File.objects.all()
    serializer_class = FileSerializers
    parser_classes = (MultiPartParser, FormParser)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset.exists():
            return Response({'message': 'Нет загруженных файлов'},
                            status=status.HTTP_200_OK)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
