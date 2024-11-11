from modeltranslation.translator import register, TranslationOptions
from .models import JourneyAlbum, Photo, TypeJourney, TravelParticipants

@register(JourneyAlbum)
class JourneyAlbumTranslationOptions(TranslationOptions):
    fields = ('a_name', 'a_descr')

@register(Photo)
class PhotoTranslationOptions(TranslationOptions):
    fields = ('ph_name', 'ph_descr')

@register(TypeJourney)
class TypeJourneyTranslationOptions(TranslationOptions):
    fields = ('j_type_name', 'j_type_descr')

@register(TravelParticipants)
class TravelParticipantsTranslationOptions(TranslationOptions):
    fields = ('participants',)
