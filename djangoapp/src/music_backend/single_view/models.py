from django.db import models
from django.utils.translation import ugettext_lazy as _

from music_backend.core.models import TimesTampModel


class Song(TimesTampModel):
    title = models.CharField(_('Title'), max_length=250, db_index=True, blank=True)
    iswc = models.CharField(_('ISWC'), max_length=250, db_index=True, blank=True)
    contributors = models.ManyToManyField('Contributor',
                                          verbose_name=_('Contributor'),
                                          related_name='songs',
                                          blank=True)
    source = models.ForeignKey('Source',
                               verbose_name=_('Sources'),
                               related_name='songs',
                               on_delete=models.SET_NULL,
                               null=True,
                               blank=True)

    class Meta:
        unique_together = ['title', 'iswc']

    def __str__(self):
        return f'{self.title} | ISWC: {self.iswc}'


class Contributor(TimesTampModel):
    name = models.CharField(_('Name'), max_length=250)

    def __str__(self):
        return f'{self.name}'


class Source(TimesTampModel):
    name = models.CharField(_('Name'), max_length=250)
    ident = models.CharField(_('Identifier'), max_length=250)

    def __str__(self):
        return f'{self.name} | ID: {self.ident}'
