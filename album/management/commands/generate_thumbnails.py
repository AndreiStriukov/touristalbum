import os
from django.db.models import Q
from django.core.management.base import BaseCommand
from album.models import Photo
from PIL import Image

class Command(BaseCommand):
    help = 'Генерация миниатюр для изображений, у которых их нет'
    
    """ Команда проходит по всем записям модели Photo и создаёт миниатюры для тех,
        у кого поле ph_thumbnail пустое. Миниатюра сохраняется в директорию thumbnails.
    """

    def handle(self, *args, **kwargs):
            # Находим все изображения, у которых ph_thumbnail пуст или равен NULL
            photos_without_thumbnails = Photo.objects.filter(Q(ph_thumbnail='') | Q(ph_thumbnail__isnull=True))

            for photo in photos_without_thumbnails:
                self.stdout.write(f'Обрабатываем изображение: {photo.ph_file.name}')

                try:
                    # Открываем основное изображение
                    ph = Image.open(photo.ph_file.path)
                    thumb_size = (300, 300)

                    # Создаем уменьшенную версию с сохранением пропорций
                    thumb_image = ph.copy()
                    thumb_image.thumbnail(thumb_size)

                    # Путь для миниатюры
                    thumb_name, thumb_extension = os.path.splitext(photo.ph_file.name)
                    thumb_extension = thumb_extension.lower()

                    # Определяем путь к директории 'thumbnails'
                    thumbnail_dir = os.path.join(os.path.dirname(photo.ph_file.path), 'thumbnails')

                    # Создаем директорию, если она не существует
                    if not os.path.exists(thumbnail_dir):
                        os.makedirs(thumbnail_dir)

                    # Путь для миниатюры в директории 'thumbnails'
                    thumb_path = os.path.join(thumbnail_dir, f'{os.path.basename(thumb_name)}_thumb{thumb_extension}')

                    # Сохраняем миниатюру
                    thumb_image.save(thumb_path)

                    # Обновляем поле миниатюры
                    photo.ph_thumbnail = os.path.join('img/photos/thumbnails', f'{os.path.basename(thumb_name)}_thumb{thumb_extension}')
                    photo.save()

                    self.stdout.write(self.style.SUCCESS(f'Миниатюра создана для: {photo.ph_file.name}'))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Ошибка при создании миниатюры для: {photo.ph_file.name}. Ошибка: {e}'))
