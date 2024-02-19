from django.test import Client, TestCase
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from api.models import File
from upload_files.tasks import downloaded_files


class ApiHttpMethodTests(APITestCase):
    """Тест-класс доступности эндпойнтов проекта."""
    def setUp(self):
        self.guest_client = Client()

    def test_get_method_api_files_endpoint(self):
        """
        Тестируем доступность разрешенного метода GET эндпойнта 'api/files'.
        """
        response = self.guest_client.get('/api/files/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_method_api_upload_endpoint(self):
        """
        Тестируем недоступность метода GET эндпойнта 'api/upload'.
        """
        response = self.guest_client.get("/api/upload/")
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)


class BehaviorCheckObjTest(TestCase):
    """Тест-класс проверки объектов модели"""
    def setUp(self):
        self.testfile = File.objects.create(
            file='testfile.txt',
            uploaded_at=timezone.now(),
        )

    def test_status_processed(self):
        """Тестируем статус поля processed при создании obj"""
        self.assertFalse(self.testfile.processed)

    def test_celery_tasks(self):
        """Тестируем Celery-задачу изменять поле processed с False на True"""
        downloaded_files(self.testfile.id)
        self.testfile.refresh_from_db()
        self.assertTrue(self.testfile.processed)
