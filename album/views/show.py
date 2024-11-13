from re import search
from typing import Any

from django.views.generic import ListView, DetailView, CreateView
from album.services import *
from album.utils import *

from django.utils.translation import gettext_lazy as _

class AlbumList:
    """ Вывод списка альбомов на страницу """
    model = JourneyAlbum
    context_object_name = 'albums'

    def get_queryset(self):
        filters = album_filters(self)
        order_by = self.request.GET.get("order_by")
        albums = album_list(self.qty, filters, order_by)
        return albums


class HomePage(AlbumList, ListView):
    """ Главная страница """
    template_name = 'album/index.html'
    qty = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "WorldSNAP. _('Home')"
        return context


class AlbumListView(AlbumList, AlbFilters, ListView):
    """ Просмотр альбомов с окном фильтрации и сортировки """
    template_name = 'album/album_list.html'
    qty = 0 # выводить все записи

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.kwargs.get('user_id')
        context['title'] = 'WorldSNAP. Просмотр альбомов'
        context['top_head'] = 'Альбомы'
        if user_id:
            context['head'] = "Мои"
        else:
            context['head'] = "Все"
        return context


class FilterAlbumListView(AlbumList, ListView):
    """" Представление для вывода альбомов по заданным значениям фильтров и сортировки """
    model = JourneyAlbum
    context_object_name = 'albums'
    template_name = 'album/part_views/albums.html'
    qty = 0


class UserPhotoListView(ListView):
    model = JourneyAlbum
    context_object_name = 'photos'
    template_name = 'album/photo_list.html'
    pk_url_kwarg = 'user_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['title'] = 'WorldSNAP. Фотографии участника ' + str(self.request.user.username)
        context['head'] = _('Photos')
        context['user_photo'] = str(self.request.user.username)
        context['user_id'] = str(self.request.user.pk)
        return context

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        filters = Q(ph_author__id=user_id)
        photos = photo_list(filters)
        return photos


class AlbumView(DetailView):
    model = JourneyAlbum
    context_object_name = 'album'
    slug_url_kwarg = 'alb_slug'
    slug_field = 'a_slug'
    template_name = 'album/album.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'WorldSNAP. Альбом'
        context['top_head'] = _('Albums')
        context['head'] = _('Album')
        return context


class PhotoListView(AlbFilters, ListView):
    """
        Представление для вывода фотографий с фильтраций и сортировкой.
    """
    model = Photo
    context_object_name = 'photos'
    slug_url_kwarg = "alb_slug"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'WorldSNAP. Просмотр фотографий'
        context['alb_slug'] = self.kwargs.get(self.slug_url_kwarg)
        context['top_head'] = 'Альбомы'
        context['head'] = 'Фотографии'
        return context

    def get_queryset(self):
        alb_slug = self.kwargs.get(self.slug_url_kwarg)

        filters = Q(ph_is_active=True)
        if alb_slug:
            filters &= Q(ph_album__a_slug=alb_slug)
        photos = Photo.objects.filter(filters).select_related('ph_album')

        return photos


class PhotoView(DetailView):
    model = Photo
    context_object_name = 'photo'
    slug_url_kwarg = 'photo_slug'
    slug_field = "ph_slug"
    template_name = 'album/photo.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'WorldSNAP. Просмотр фотографии'
        context['top_head'] = 'Фотографии'
        context['head'] = 'Фотография'
        return context
    

class GallaryView(ListView):
    model = Photo
    template_name = 'album/gallary.html'
    context_object_name = 'photos'
    slug_url_kwarg = "alb_slug"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Галерея'
        return context
    
    def get_queryset(self):
        alb_slug = self.kwargs.get(self.slug_url_kwarg)

        filters = Q(ph_is_active=True)
        if alb_slug:
            filters &= Q(ph_album__a_slug=alb_slug)
        photos = Photo.objects.filter(filters).select_related('ph_album')

        return photos


class SearchPhoto(ListView):
    model = Photo
    template_name = 'album/photo_list.html'
    context_object_name = 'photos'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Поиск фото по названию'
        context['head'] = 'Результаты поиска фото'
        return context

    def get_queryset(self):
        search_photo = self.request.GET.get("search_photo")
        filters = Q(ph_name__icontains=search_photo)
        photos = photo_list(filters)
        return photos
