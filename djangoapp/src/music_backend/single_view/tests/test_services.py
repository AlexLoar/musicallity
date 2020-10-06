import io

from django.test import TestCase
from django.core.files.uploadedfile import InMemoryUploadedFile

from music_backend.single_view.services import SingleViewService
from music_backend.single_view.models import Song


class SingleViewServiceTestCase(TestCase):
    def test_raw_csv_to_dict_parse_date_properly(self):
        csv_memory_data = self._generate_csv_buffer()

        parsed_data = SingleViewService.raw_csv_to_dict(csv_memory_data)

        self.assertEqual('Shape of You', parsed_data[0]['title'])
        self.assertEqual('Edward Sheeran', parsed_data[0]['contributors'])
        self.assertEqual('T9204649558', parsed_data[0]['iswc'])
        self.assertEqual('warner', parsed_data[0]['source'])
        self.assertEqual('1', parsed_data[0]['id'])
        self.assertEqual('Adventure of a Lifetime', parsed_data[1]['title'])
        self.assertEqual('O Brien Edward John|Yorke Thomas Edward|Greenwood Colin Charles',
                         parsed_data[1]['contributors'])
        self.assertEqual('T0101974597', parsed_data[1]['iswc'])
        self.assertEqual('warner', parsed_data[1]['source'])
        self.assertEqual('2', parsed_data[1]['id'])

    @staticmethod
    def _generate_csv_buffer() -> InMemoryUploadedFile:
        content_file = b"title,contributors,iswc,source,id\n" \
                       b"Shape of You,Edward Sheeran,T9204649558,warner,1\n" \
                       b"Adventure of a Lifetime,O Brien Edward John|Yorke Thomas Edward|Greenwood Colin Charles,T0101974597,warner,2"
        file = io.BytesIO(content_file)
        field_name = 'file'
        name = 'test_works_metadata.csv'
        content_type = 'text/csv'
        size = 300
        charset = None
        return InMemoryUploadedFile(file, field_name, name, content_type, size, charset)

    def test_import_work_single_view_do_it_properly(self):
        csv_data = self._get_csv_list()

        self.assertEqual(0, Song.objects.count())

        SingleViewService.import_work_single_view(csv_data)

        self.assertEqual(2, Song.objects.count())
        song_1 = Song.objects.first()
        song_2 = Song.objects.last()
        self.assertEqual(csv_data[0]['title'], song_1.title)
        self.assertEqual(csv_data[0]['iswc'], song_1.iswc)
        self.assertEqual(csv_data[0]['contributors'], '|'.join(song_1.contributors.all().values_list('name', flat=True)))
        self.assertEqual(csv_data[0]['source'], song_1.source.name)
        self.assertEqual(csv_data[0]['id'], song_1.source.ident)
        self.assertEqual(csv_data[2]['title'], song_2.title)
        self.assertEqual(csv_data[2]['iswc'], song_2.iswc)
        self.assertIn(csv_data[2]['contributors'], '|'.join(song_2.contributors.all().values_list('name', flat=True)))
        self.assertEqual(csv_data[2]['source'], song_2.source.name)
        self.assertEqual(csv_data[2]['id'], song_2.source.ident)

    @staticmethod
    def _get_csv_list():
        return [
            {
                'title': 'Shape of You',
                'contributors': 'Edward Sheeran',
                'iswc': 'T9204649558',
                'source': 'sony',
                'id': '1'
            },
            {
                'title': 'Shape of You',
                'contributors': 'Edward Christopher Sheeran',
                'iswc': 'T9204649558',
                'source': 'sony',
                'id': '1'
            },
            {
                'title': 'Adventure of a Lifetime',
                'contributors': 'O Brien Edward John|Yorke Thomas Edward|Greenwood Colin Charles',
                'iswc': 'T0101974597',
                'source': 'warner',
                'id': '2'
            },
            {
                'title': 'Adventure of a Lifetime',
                'contributors': 'O Brien Edward John|Selway Philip James',
                'iswc': 'T0101974597',
                'source': 'warner',
                'id': '2'
            }
        ]
