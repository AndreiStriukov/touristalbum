from django import forms
from .models import *

from django.utils.translation import gettext_lazy as _


class AddPhotoForm(forms.ModelForm):

    class Meta:
        model = Photo
        fields = ['ph_file', 'ph_name', 'ph_descr', 'ph_album']
        # labels = {'ph_file': 'Выберите файл', 'ph_name': 'Назовите',
        #          'ph_descr': 'Описание', 'ph_album': 'Укажите альбом'}


class AddAlbum(forms.ModelForm):

    class Meta:
        model = JourneyAlbum
        fields = ['a_name', 'a_descr', 'j_month', 'j_year', 'j_place', 'travel_participants', 'j_type']
        labels = {'a_name': _('Album name'), 'a_descr': _('Album description, emotions'), 'j_month': _('Travel month'),
                  'j_year': _('Travel year'), 'j_place': _('Travel destination'), 
                  'travel_participants': _('Travel participants'), 'j_type': _('Nature of travel')}


class EditAlbum(forms.ModelForm):

    class Meta:
        model = JourneyAlbum
        fields = ['a_is_active', 'a_name', 'a_descr', 'j_month', 'j_year', 'j_place', 'travel_participants', 'j_type']


class EditPhoto(forms.ModelForm):

    class Meta:
        model = Photo
        fields = ['ph_is_active', 'ph_file', 'ph_name', 'ph_descr', 'ph_album']
