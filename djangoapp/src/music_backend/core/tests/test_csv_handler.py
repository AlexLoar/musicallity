import os
import io

from django.test import SimpleTestCase

from music_backend.core.csv_handler import CSVHandler, CSVDialect

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))


class CSVHandlerTestCase(SimpleTestCase):

    def test_reader_can_read_a_csv_file(self):
        file_name = 'test_works_metadata.csv'
        path_to_file = os.path.join(CURRENT_DIR, file_name)
        data = list()

        for row in CSVHandler.reader(file_name=path_to_file, dialect=CSVDialect):
            data.append(row)

        self.assertEqual(2, len(data))
        self.assertEqual('Shape of You', data[0]['title'])
        self.assertEqual('Edward Sheeran', data[0]['contributors'])
        self.assertEqual('T9204649558', data[0]['iswc'])
        self.assertEqual('warner', data[0]['source'])
        self.assertEqual('1', data[0]['id'])

    def test_writer_can_generate_csv_data(self):
        header = ['title', 'contributors', 'iswc', 'source', 'id']
        data = [{
            'title': 'Shape of You',
            'contributors': 'Edward Sheeran',
            'iswc': 'T9204649558',
            'source': 'warner',
            'id': '1'
        }]
        output = io.StringIO()

        csv_buffer = CSVHandler.writer(header=header, data=data, output=output)

        csv_data = csv_buffer.getvalue()
        generated_headers = csv_data.split('\n')[0].split(',')
        generated_body = csv_data.split('\n')[1].split(',')
        self.assertCountEqual(header, generated_headers)
        self.assertCountEqual(list(data[0].values()), generated_body)
