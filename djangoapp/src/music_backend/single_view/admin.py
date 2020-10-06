from django.contrib import admin

from music_backend.single_view.models import Song, Contributor, Source


@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    fields = ['title', 'iswc', 'contributors', 'source']


@admin.register(Contributor)
class ContributorAdmin(admin.ModelAdmin):
    fields = ['name']


@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    fields = ['name', 'ident']
