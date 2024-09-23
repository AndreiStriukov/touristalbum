from django.db.models import Prefetch, Count
from album.models import *
from album.utils import *


def album_list(qty=0,  filters=None, order_by=None):
    photos = (Photo.objects.only('ph_file').filter(ph_is_active=True))
    albums = JourneyAlbum.objects

    if filters:
        albums = albums.filter(filters)
    else:
        albums = albums.all()

    if qty != 0:
        albums = albums[:qty]

    if order_by:
        albums = albums.order_by(order_by)

    albums = albums.annotate(count_photos=Count("photos")).prefetch_related(Prefetch('photos', queryset=photos))
    return albums


def photo_list(filters=None, order_by=None):
    photos = Photo.objects

    if filters:
        photos = photos.filter(filters)
    else:
        photos = photos.all()
    photos = photos.select_related('ph_album')
    return photos


class AlbFilters:
    """Фильтры для фотографий"""

    def get_periods(self):
        return JourneyAlbum.objects.filter(a_is_active=True)

    def get_types(self):
        get_place = TypeJourney.objects.all()
        return get_place

    def get_participants(self):
        return TravelParticipants.objects.all()

    def get_years(self):
        return JourneyAlbum.objects.filter(a_is_active=True).order_by('j_year').values('j_year').distinct()

