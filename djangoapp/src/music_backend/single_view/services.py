import io
import csv
import logging
from typing import Union

from django.core.files.uploadedfile import InMemoryUploadedFile

from fuzzywuzzy import fuzz

from music_backend.single_view.models import Song, Contributor, Source

logger = logging.getLogger(__name__)


class SingleViewService:
    @classmethod
    def raw_csv_to_dict(cls, raw_data: InMemoryUploadedFile) -> list:
        csv_data = list()
        decoded_data = io.StringIO(raw_data.read().decode('utf-8'))
        for row in csv.DictReader(decoded_data):
            csv_data.append(row)
        return csv_data

    @classmethod
    def import_work_single_view(cls, csv_data: list) -> None:
        for single_view in csv_data:
            title = single_view.get('title')
            iswc = single_view.get('iswc')
            contributors_names = single_view.get('contributors', '').split('|')
            source = single_view.get('source')
            ident = int(single_view.get('id'))

            cls._reconcile_single_view(title, iswc, contributors_names, source, ident)

    @classmethod
    def _reconcile_single_view(cls, title: str, iswc: str, contributors_names: list, source: str, ident: int) -> None:
        song = cls._get_song(title, iswc)

        cls._handle_contributors(song, contributors_names)
        cls._handle_source(song, source, ident)

    @classmethod
    def _get_song(cls, title: str, iswc: str) -> Song:
        song = cls._get_song_by_iswc(iswc)
        if not song:
            song = cls._get_song_by_title(title, iswc)
        if not song:
            song = cls._get_song_by_similar_title(title, iswc)
        if not song:
            song = Song.objects.create(title=title,
                                       iswc=iswc)

        return song

    @staticmethod
    def _get_song_by_iswc(iswc: str) -> Union[Song, None]:
        try:
            song = Song.objects.get(iswc=iswc)
        except Song.DoesNotExist:
            song = None
        return song

    @staticmethod
    def _get_song_by_title(title: str, iswc: str) -> Union[Song, None]:
        try:
            song = Song.objects.get(title=title)
            if not song.iswc:
                song.iswc = iswc
        except Song.DoesNotExist:
            song = None
        return song

    @staticmethod
    def _get_song_by_similar_title(title: str, iswc: str) -> Union[Song, None]:
        MIN_CONFIDENCE_RATIO = 97

        songs_titles = Song.objects.all().values_list('title', flat=True)
        for song_title in songs_titles:
            # Try to find similar song names
            similarity_ratio = fuzz.ratio(title, song_title)
            if similarity_ratio >= MIN_CONFIDENCE_RATIO:
                song = Song.objects.get(title=song_title)
                if not song.iswc:
                    song.iswc = iswc
                return song
        return None

    @classmethod
    def _handle_contributors(cls, song: Song, contributors_names: list) -> None:
        contributors = cls._get_contributors(contributors_names)
        for contributor in contributors:
            if contributors not in song.contributors.all().iterator():
                song.contributors.add(contributor)

    @staticmethod
    def _get_contributors(contributors_names_list: list) -> list:
        MIN_CONFIDENCE_RATIO = 70
        contributors = list()

        existing_contributors = Contributor.objects.all().values_list('name', flat=True)
        for contributors_name_list in contributors_names_list:
            found = False
            for existing_contributor in existing_contributors:
                similarity_ratio = fuzz.ratio(existing_contributor, contributors_name_list)
                if similarity_ratio >= MIN_CONFIDENCE_RATIO:
                    contributors.append(Contributor.objects.get(name=existing_contributor))
                    found = True
            if not found:
                contributors.append(Contributor.objects.create(name=contributors_name_list))
        return contributors

    @classmethod
    def _handle_source(cls, song: Song, source: str, ident: int) -> None:
        obj, created = Source.objects.get_or_create(name=source)
        song.source = obj
        song.source.ident = ident
        song.source.save()
        song.save()
