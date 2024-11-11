from django import forms
from .models import *


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
        # labels = {'a_name': 'Назовите альбом', 'a_descr': 'Опишите путешествие', 'j_month': 'Месяц путешествия',
        #           'j_year': 'Год путешествия', 'j_place': 'Место путешествия'}


class EditAlbum(forms.ModelForm):

    class Meta:
        model = JourneyAlbum
        fields = ['a_is_active', 'a_name', 'a_descr', 'j_month', 'j_year', 'j_place', 'travel_participants', 'j_type']


class EditPhoto(forms.ModelForm):

    class Meta:
        model = Photo
        fields = ['ph_is_active', 'ph_file', 'ph_name', 'ph_descr', 'ph_album']
