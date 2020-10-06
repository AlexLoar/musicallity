from rest_framework import serializers

from music_backend.single_view.models import Song, Contributor, Source


class ContributorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contributor
        fields = '__all__'


class SourceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Source
        fields = '__all__'


class SingleViewSerializer(serializers.ModelSerializer):
    contributors = ContributorSerializer(many=True)
    source = SourceSerializer()

    class Meta:
        model = Song
        fields = '__all__'


class SingleViewExportCSVSerializer(serializers.ModelSerializer):
    contributors = serializers.SerializerMethodField()
    source = serializers.SerializerMethodField()
    id = serializers.SerializerMethodField()

    def get_contributors(self, obj):
        contributors_names = obj.contributors.all().values_list('name', flat=True)
        return '|'.join(contributors_names)

    def get_source(self, obj):
        return getattr(obj.source, 'name', '')

    def get_id(self, obj):
        return getattr(obj.source, 'ident', '')

    class Meta:
        model = Song
        fields = ['title', 'iswc', 'contributors', 'source', 'id']
