from django.urls import path

from api.views import FileLoadView, ListFileView

app_name = 'api'

urlpatterns = [
    path('files/', ListFileView.as_view()),
    path('upload/', FileLoadView.as_view()),
]
