import random

import factory
from faker import Factory

from music_backend.single_view.models import Song
from music_backend.single_view.models import Contributor
from music_backend.single_view.models import Source

faker = Factory.create()


class ContributorFactory(factory.django.DjangoModelFactory):
    name = factory.lazy_attribute(lambda o: faker.name())

    class Meta:
        model = Contributor


sources_names = ['warner', 'sony', 'universal']
class SourceFactory(factory.django.DjangoModelFactory):
    name = factory.lazy_attribute(lambda o: random.choice(sources_names))
    ident = factory.lazy_attribute(lambda o: str(faker.random_digit_not_null()))

    class Meta:
        model = Source


class SongFactory(factory.django.DjangoModelFactory):
    title = factory.lazy_attribute(lambda o: faker.name())
    iswc = factory.lazy_attribute(lambda o: faker.isbn10().replace('-', ''))
    source = factory.SubFactory(SourceFactory)

    @factory.post_generation
    def contributors(self, created, extracted, **kwargs):
        if not created:
            return
        if extracted:
            for contributor in extracted:
                self.contributors.add(contributor)

    class Meta:
        model = Song
