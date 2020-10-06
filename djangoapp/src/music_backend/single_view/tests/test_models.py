from django.test import TestCase

from music_backend.single_view.tests.factories import SongFactory, ContributorFactory, SourceFactory


class SongTestCase(TestCase):

    def test_song_string(self):
        song = SongFactory()
        expected_representation = f'{song.title} | ISWC: {song.iswc}'

        self.assertEqual(expected_representation, song.__str__())

    def test_contributor_string(self):
        contributor = ContributorFactory()
        expected_representation = f'{contributor.name}'

        self.assertEqual(expected_representation, contributor.__str__())

    def test_source_string(self):
        source = SourceFactory()
        expected_representation = f'{source.name} | ID: {source.ident}'

        self.assertEqual(expected_representation, source.__str__())
