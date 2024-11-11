from django.core.management.base import BaseCommand
from album.models import JourneyAlbum, Photo, TypeJourney, TravelParticipants

class Command(BaseCommand):
    help = 'Копирует оригинальные данные в поля на русском языке'

    def handle(self, *args, **kwargs):
        for album in JourneyAlbum.objects.all():
            # Копируем, только если есть данные в оригинальных полях
            if not album.a_name_ru and album.a_name:  # Проверяем, что есть что копировать
                album.a_name_ru = album.a_name
                self.stdout.write(self.style.SUCCESS(f"Копирование a_name_ru: {album.a_name}"))
            if not album.a_descr_ru and album.a_descr:  # Проверяем, что есть что копировать
                album.a_descr_ru = album.a_descr
                self.stdout.write(self.style.SUCCESS(f"Копирование a_descr_ru: {album.a_descr}"))
            album.save()
        self.stdout.write(self.style.SUCCESS('Данные album успешно скопированы!'))

        for photo in Photo.objects.all():
            if not photo.ph_name_ru and photo.ph_name:
                photo.ph_name_ru = photo.ph_name
            if not photo.ph_descr_ru and photo.ph_descr:
                photo.ph_descr_ru = photo.ph_descr
            photo.save()
        self.stdout.write(self.style.SUCCESS('Данные photo успешно скопированы!'))

        for types in TypeJourney.objects.all():
            if not types.j_type_name_ru and types.j_type_name:
                types.j_type_name_ru = types.j_type_name
            if not types.j_type_descr_ru and types.j_type_descr:
                types.j_type_descr_ru = types.j_type_descr
            types.save()
        self.stdout.write(self.style.SUCCESS('Данные TypeJourney успешно скопированы!'))

        for travel in TravelParticipants.objects.all():
            if not travel.participants_ru and travel.participants:
                travel.participants_ru = travel.participants
            travel.save()
        self.stdout.write(self.style.SUCCESS('Данные TravelParticipants успешно скопированы!'))


