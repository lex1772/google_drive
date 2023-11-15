from django.urls import path

from google_drive_documents.apps import GoogleDriveDocumentsConfig
from google_drive_documents.views import DocumentAPIView

app_name = GoogleDriveDocumentsConfig.name

# Отдельные урлы для приложения создания документов
urlpatterns = [
    path(
        '',
        DocumentAPIView.as_view(),
        name='documents'
    ),
]
