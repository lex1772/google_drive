import json
from json import JSONDecodeError

from rest_framework.response import Response
from rest_framework.views import APIView

from google_drive_documents.services import check_names, google_drive, google_docs


class DocumentAPIView(APIView):
    """Контроллер для добавления файла в Google Drive"""

    def post(self, request):
        """Метод POST, который приниямает на вход JSON с названием файла и содержимым"""
        try:
            data = json.loads(request.body)
        except JSONDecodeError:
            return Response("Нет данных")
        if check_names(data):
            return Response(google_docs(data, google_drive(data)))
        return Response("Переданы не верные данные")
