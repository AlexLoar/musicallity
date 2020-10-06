import io
import csv

from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status

from music_backend.single_view.tests.factories import SongFactory, ContributorFactory, SourceFactory
from music_backend.single_view.api.v1.serializers import SingleViewExportCSVSerializer
from music_backend.single_view.models import Song
from music_backend.core.exceptions import ISWCNotFound


class WSVViewSetTestCase(APITestCase):

    def test_list_of_song_do_it_properly(self):
        SongFactory.create_batch(2)
        response = self.client.get(reverse('song-list'))
        expected_songs_number = Song.objects.count()

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(expected_songs_number, len(response.data['results']))

    def test_get_song_by_iwc_do_it_properly(self):
        contributor = ContributorFactory()
        iswc = 'T123456798'
        song = SongFactory(iswc=iswc, contributors=(contributor,))

        response = self.client.get(reverse('song-detail', kwargs={'iswc': iswc}))

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(song.title, response.data['title'])
        self.assertEqual(song.iswc, response.data['iswc'])
        self.assertEqual(contributor.id, response.data['contributors'][0]['id'])
        self.assertEqual(contributor.name, response.data['contributors'][0]['name'])
        self.assertEqual(song.source_id, response.data['source']['id'])
        self.assertEqual(song.source.name, response.data['source']['name'])


class SingleViewCSVView(APITestCase):

    def test_export_all_to_csv_do_it_properly(self):
        contributor = ContributorFactory()
        song_1 = SongFactory(contributors=(contributor,))
        song_2 = SongFactory(contributors=(contributor,))

        response = self.client.get(reverse('wsv-export-csv'))

        content = response.content.decode('utf-8')
        cvs_reader = csv.reader(io.StringIO(content))
        body = list(cvs_reader)
        headers = body.pop(0)

        expected_headers = SingleViewExportCSVSerializer.Meta.fields
        expected_body_1 = [song_1.title, song_1.iswc, song_1.contributors.first().name, song_1.source.name, song_1.source.ident]
        expected_body_2 = [song_2.title, song_2.iswc, song_2.contributors.first().name, song_2.source.name, song_2.source.ident]
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(expected_headers, headers)
        self.assertEqual(expected_body_1, body[0])
        self.assertEqual(expected_body_2, body[1])

    def test_export_given_iswc_to_csv_do_it_properly(self):
        contributor = ContributorFactory()
        song = SongFactory(contributors=(contributor,))
        SongFactory(contributors=(contributor,))

        response = self.client.get(reverse('wsv-export-csv', kwargs={'iswc': song.iswc}))

        content = response.content.decode('utf-8')
        cvs_reader = csv.reader(io.StringIO(content))
        body = list(cvs_reader)
        headers = body.pop(0)

        expected_headers = SingleViewExportCSVSerializer.Meta.fields
        expected_body_1 = [song.title, song.iswc, song.contributors.first().name, song.source.name, song.source.ident]
        number_of_rows = Song.objects.filter(iswc=song.iswc).count()
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(number_of_rows, len(body))
        self.assertEqual(expected_headers, headers)
        self.assertEqual(expected_body_1, body[0])

    def test_export_given_a_iswc_that_does_not_exist_returns_404(self):
        non_existent_iswc = '000000'
        response = self.client.get(reverse('wsv-export-csv', kwargs={'iswc': non_existent_iswc}))

        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)
        self.assertEqual(ISWCNotFound.default_detail, response.data['detail'])
