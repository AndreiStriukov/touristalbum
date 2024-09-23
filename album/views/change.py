from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView, UpdateView, CreateView
from django.urls import reverse_lazy

from album.forms import *


class AddPhoto(LoginRequiredMixin, CreateView):
    form_class = AddPhotoForm
    template_name = 'album/add_photo.html'
    extra_context = {
        'title': 'Добавление фотографии. АЛЬБОМ Туриста',
        'head': 'Добавление фотографии',
        'button': 'Добавить фото',
    }

    def get_success_url(self):
        user = self.request.user.pk
        return reverse_lazy('user_photo_list', kwargs={'user_id': user})

    # def get_context_data(self, *args, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['alb_slug'] = self.kwargs['alb_slug']
    #     return context

    # def get_initial(self, *args, **kwargs):
    #     # Get the initial dictionary from the superclass method
    #     initial = super(AddPhoto, self).get_initial(**kwargs)
    #     # Copy the dictionary so we don't accidentally change a mutable dict
    #     initial = initial.copy()
    #     slug = self.kwargs['alb_slug']
    #     initial['ph_name'] = slug
    #     initial['ph_album'] = JourneyAlbum.objects.filter(a_slug=slug)
    #     print(initial['ph_album'])
    #     return initial

    def get_initial(self):
        initial = super().get_initial()
        slug = self.kwargs.get('alb_slug')
        if slug:
            alb = get_object_or_404(JourneyAlbum, a_slug=slug)
            initial['ph_album'] = alb
        return initial

    def form_valid(self, form):
        fields = form.save(commit=False)
        user = self.request.user
        fields.ph_author = user
        # fields.save()
        return super(AddPhoto, self).form_valid(form)


class AddAlbum(LoginRequiredMixin, CreateView):
    template_name = 'album/add_album.html'
    form_class = AddAlbum
    model = Photo
    extra_context = {
        'title': 'Создание альбома. АЛЬБОМ Туриста',
        'head': 'Создание альбома',
        'button': 'Создать альбом',
    }

    def get_success_url(self):
        user = self.request.user.pk
        return reverse_lazy('user_albums_list', kwargs={'user_id': user})

    def form_valid(self, form):
        fields = form.save(commit=False)
        user = self.request.user
        fields.a_author = user
        fields.save()
        return super(AddAlbum, self).form_valid(form)


class AlbumUpdate(UpdateView):
    model = JourneyAlbum
    form_class = EditAlbum
    slug_url_kwarg = 'alb_slug'
    slug_field = 'a_slug'
    # fields = ['a_name', 'a_descr']
    template_name = 'album/update_album.html'

    def get_success_url(self):
        alb_slug = self.kwargs['alb_slug']
        return reverse_lazy('get_album', kwargs={'alb_slug': alb_slug})

    def get_context_data(self, *, object_list=None, **kwargs):
        alb_slug = self.kwargs['alb_slug']
        context = super().get_context_data(**kwargs)
        context['title'] = 'Изменить свойства альбома'
        context['head'] = 'Изменить свойства альбома'
        context['button'] = 'Изменить'
        context['a_selected'] = alb_slug
        return context


class PhotoUpdate(UpdateView):
    model = Photo
    form_class = EditPhoto
    slug_url_kwarg = 'photo_slug'
    slug_field = 'ph_slug'
    template_name = 'album/update_photo.html'

    def get_success_url(self):
        photo_slug = self.kwargs['photo_slug']
        return reverse_lazy('get_photo', kwargs={'photo_slug': photo_slug})

    def get_context_data(self, *, object_list=None, **kwargs):
        photo_slug = self.kwargs['photo_slug']
        context = super().get_context_data(**kwargs)
        context['title'] = 'Изменить свойства фото'
        context['head'] = 'Изменить свойства фото'
        context['button'] = 'Изменить'
        context['ph_selected'] = photo_slug
        return context


def del_photo():
    return None
