from django.contrib import admin
from .models import *

from modeltranslation.admin import TranslationAdmin

from django import forms
from .models import JourneyAlbum
# from ckeditor_uploader.widgets import CKEditorUploadingWidget 



# class JourneyAlbumAdminForm(forms.ModelForm):
#     """Форма для редактирования переведённых полей"""
#     a_name_ru = forms.CharField(label="Имя альбома (Русский)", widget=forms.TextInput())
#     a_name_en = forms.CharField(label="Имя альбома (Английский)", widget=forms.TextInput())
    
#     a_descr_ru = forms.CharField(label="Описание альбома (Русский)")
#     a_descr_en = forms.CharField(label="Описание альбома (Английский)")

#     class Meta:
#         model = JourneyAlbum
#         fields = ['a_name_ru', 'a_name_en', 'a_descr_ru', 'a_descr_en']

@admin.register(JourneyAlbum)
class JourneyAlbumAdmin(TranslationAdmin):
    list_display = ('a_slug', 'a_name', 'a_is_active', 'j_month', 'j_year', 'j_type',
                    'a_date_create', 'a_date_update', 'a_author',)
    readonly_fields = ('a_date_create', 'a_date_update',)
    list_filter = ('j_type', 'travel_participants',)
    prepopulated_fields = {'a_slug': ('a_name',)}


@admin.register(Photo)
class PhotoAdmin(TranslationAdmin):
    list_display = ('ph_name', 'ph_slug', 'ph_file', 'ph_descr', 'ph_album', 'ph_is_active',
                    'ph_date_create', 'ph_date_update')
    readonly_fields = ('ph_date_create', 'ph_date_update',)
    prepopulated_fields = {'ph_slug': ('ph_name',)}
    list_filter = ('ph_album', 'ph_is_active',)


@admin.register(TypeJourney)
class TypeJourneyAdmin(TranslationAdmin):
    list_display = ('j_type_name', 'j_type_descr')


@admin.register(TravelParticipants)
class TravelParticipantsAdmin(TranslationAdmin):
    list_display = ('participants',)

