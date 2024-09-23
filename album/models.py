from django.db import models
from django.urls import reverse
from PIL import Image
from account.models import AdvUser, Lang


class JourneyAlbum(models.Model):
    a_name = models.CharField(max_length=32, verbose_name='Имя альбома')
    a_slug = models.SlugField(max_length=32, unique=True, db_index=True, verbose_name='Имя альбома в адресной строке')
    j_month = models.PositiveSmallIntegerField(default=1, verbose_name='Месяц путешествия')
    j_year = models.PositiveSmallIntegerField(default=2024, verbose_name='Год путешествия')
    j_place = models.CharField(max_length=64, verbose_name='Место путешествия')
    travel_participants = models.ForeignKey('TravelParticipants', on_delete=models.CASCADE, null=True,
                                            verbose_name='Участники путешествия')
    j_type = models.ForeignKey('TypeJourney', on_delete=models.CASCADE, verbose_name='Характер (тип) путешествия')
    a_descr = models.TextField(blank=True, null=True, verbose_name='Описание альбома, эмоции')
    a_date_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    a_author = models.ForeignKey(AdvUser, on_delete=models.CASCADE, default=1, verbose_name='Автор публикации')
    a_date_update = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    a_is_active = models.BooleanField(default=False, verbose_name='Отображать альбом')

    def __str__(self):
        return self.a_name

    def get_absolute_url(self):
        return reverse('show_album_photo', kwargs={'alb_slug': self.a_slug})

    def get_alb_url(self):
        return reverse('get_album', kwargs={'alb_slug': self.a_slug})

    class Meta:
        ordering = ['a_name']


class Photo(models.Model):
    ph_file = models.ImageField(upload_to='img/photos', verbose_name='Файл')
    ph_name = models.CharField(max_length=36, verbose_name='Имя фото')
    ph_slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='Имя фото в адресной строке')
    ph_descr = models.TextField(blank=True, null=True, verbose_name='Описание фото, эмоции')
    ph_album = models.ForeignKey('JourneyAlbum', on_delete=models.PROTECT, verbose_name='Альбом',
                                 related_name='photos')
    ph_date_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    ph_date_update = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    ph_is_active = models.BooleanField(default=True, verbose_name='Отображать фото')
    ph_author = models.ForeignKey(AdvUser, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.ph_name

    def save(self, *args, **kwargs):
        super().save()
        ph = Image.open(self.ph_file.path)
        if ph.width > 1200 or ph.height > 1200:
            output_size = (1200, 1200)
            ph.thumbnail(output_size)
            ph.save(self.ph_file.path)

    def get_absolute_url(self):
        return reverse('get_photo', kwargs={'photo_slug': self.ph_slug})

    class Meta:
        ordering = ['-ph_date_create']


class TypeJourney(models.Model):
    j_type_name = models.CharField(max_length=32, verbose_name='Тип путешествия')
    j_type_descr = models.CharField(max_length=256, verbose_name='Описание типа путешествия')

    def __str__(self):
        return self.j_type_name


class TravelParticipants(models.Model):
    participants = models.CharField(max_length=32, verbose_name='Участники путешествия')

    def __str__(self):
        return self.participants
