from django.http import HttpResponse
from django.db.models import QuerySet

from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.views import APIView

from music_backend.single_view.api.v1.serializers import SingleViewSerializer, SingleViewExportCSVSerializer
from music_backend.single_view.tasks import import_csv_file
from music_backend.single_view.models import Song
from music_backend.single_view.services import SingleViewService
from music_backend.core.csv_handler import CSVHandler
from music_backend.core.exceptions import ISWCNotFound


class WSVViewSet(viewsets.ReadOnlyModelViewSet):
    """Get list of ISWC or an specific one.

    GET /api/v1/wsv/
    GET /api/v1/wsv/(iswc)/
    """
    lookup_field = 'iswc'
    queryset = Song.objects.all()
    serializer_class = SingleViewSerializer


class SingleViewCSVView(APIView):
    serializer_class = SingleViewExportCSVSerializer

    def get(self, request, iswc=None):
        """
            Export to CSV all single views: GET /api/v1/wsv/export-csv/
            Export to CSV single views filtered by ISWC: GET /api/v1/wsv/export-csv/(iswc)
        """
        file_name = 'works_metadata.csv'
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{file_name}"'

        queryset = self._get_queryset(iswc)
        serializer = self.serializer_class(queryset, many=True)
        header = self.serializer_class.Meta.fields

        response = CSVHandler.writer(header=header,
                                     data=serializer.data,
                                     output=response)

        return response

    @staticmethod
    def _get_queryset(iswc: str) -> QuerySet:
        if iswc:
            queryset = Song.objects.filter(iswc=iswc)
            if not queryset:
                raise ISWCNotFound()
        else:
            queryset = Song.objects.all()
        return queryset

    def post(self, request, filename):
        """
            Import from CSV: POST /api/v1/wsv/import-csv/(filename)
        """
        csv_raw_data = request.data['file']
        csv_dict = SingleViewService.raw_csv_to_dict(csv_raw_data)
        task = import_csv_file.delay(csv_dict)
        return Response(data={'message': 'Enqueued task!', 'task_id': task.id}, status=status.HTTP_202_ACCEPTED)
