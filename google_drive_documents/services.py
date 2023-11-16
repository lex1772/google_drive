import os

from google.oauth2 import service_account
from googleapiclient.discovery import build

# Данные для входа в сервисный аккаунт
scopes = ['https://www.googleapis.com/auth/drive.file',
          'https://www.googleapis.com/auth/drive',
          'https://www.googleapis.com/auth/documents']
service_account_file = os.getenv('SERVICE_ACCOUNT_FILE')
credentials = service_account.Credentials.from_service_account_file(
    service_account_file, scopes=scopes)


def google_drive(data: dict):
    """Функция для создания файла в google drive"""
    service = build('drive', 'v3', credentials=credentials)

    file_metadata = {
        'name': data['name'],
        'parents': [os.getenv('FOLDER_ID')],
        'mimeType': 'application/vnd.google-apps.document'
    }

    file = service.files().create(body=file_metadata).execute()

    file_id = file.get('id')
    return file_id


def google_docs(data: dict, file_id):
    """Функция для заполнения созданного файла"""
    docs_service = build('docs', 'v1', credentials=credentials)

    # Добавление текста в документ
    requests = [
        {
            'insertText': {
                'location': {
                    'index': 1,
                },
                'text': data['data'],
            },
        },
    ]

    try:
        docs_service.documents().batchUpdate(
            documentId=file_id,
            body={'requests': requests}
        ).execute()
    except Exception:
        return "Не удалось создать файл"
    else:
        return "Файл создан"


def check_names(data: dict):
    """Функция для валидации передаваемых данных"""
    if sorted(list(data.keys())) == sorted(['data', 'name']):
        return True
