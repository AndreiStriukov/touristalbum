from django.contrib import admin
from .models import *


class JourneyAlbumAdmin(admin.ModelAdmin):
    list_display = ('a_name', 'a_is_active', 'a_slug', 'j_month', 'j_year', 'j_type',
                    'a_date_create', 'a_date_update', 'a_author',)
    readonly_fields = ('a_date_create', 'a_date_update',)
    list_filter = ('j_type', 'travel_participants',)
    prepopulated_fields = {'a_slug': ('a_name',)}


admin.site.register(JourneyAlbum, JourneyAlbumAdmin)


class PhotoAdmin(admin.ModelAdmin):
    list_display = ('ph_name', 'ph_slug', 'ph_file', 'ph_descr', 'ph_album', 'ph_is_active',
                    'ph_date_create', 'ph_date_update')
    readonly_fields = ('ph_date_create', 'ph_date_update',)
    prepopulated_fields = {'ph_slug': ('ph_name',)}
    list_filter = ('ph_album', 'ph_is_active',)


admin.site.register(Photo, PhotoAdmin)


class TypeJourneyAdmin(admin.ModelAdmin):
    list_display = ('j_type_name', 'j_type_descr')


admin.site.register(TypeJourney, TypeJourneyAdmin)


class TravelParticipantsAdmin(admin.ModelAdmin):
    list_display = ('participants',)

admin.site.register(TravelParticipants, TravelParticipantsAdmin)
