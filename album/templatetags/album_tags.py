from django import template
from django.shortcuts import get_object_or_404
from album.models import *

register = template.Library()


@register.simple_tag()
def get_main_menu(user):
    if user.id:
        main_menu = [
            {'name': "Главная", 'url_name': get_url_menu('index'), 'class': 'fa-home'},
            {'name': "Альбомы", 'class': 'fa-folder-open', 'id': '1',
            'sub1': {'name': "Все альбомы", 'url_name': get_url_menu('show_albums_list'), 'id': '11', 'class': 'fa-folder-open'},
            'sub2': {'name': "Мои альбомы", 'url_name': get_url_menu('user_albums_list', user.id), 'id': '12', 'class': 'fa-address-book-o'},
            'sub3': {'name': "Создать альбом", 'url_name': get_url_menu('add_album'), 'id': '13', 'class': 'fa-plus'}
            },
            {'name': "Фото", 'class': 'fa-file-image-o', 'id': '2',
            'sub1': {'name': "Все фото", 'url_name': get_url_menu('show_photos_list'), 'id': '21', 'class': 'fa-file-image-o'},
            'sub2': {'name': "Мои фото", 'url_name': get_url_menu('user_photo_list', user.id), 'id': '22', 'class': 'fa-camera'},
            'sub3': {'name': "Загрузить фото", 'url_name': get_url_menu('add_photo'), 'id': '23', 'class': 'fa-download'}
            },
            {'name': "Профиль", 'class': 'fa-user', 'id': '3',
            'sub1': {'name': user.username, 'url_name': get_url_menu('profile', user.id), 'id': '31', 'class': ' fa-address-card-o'},
            'sub2': {'name': "Выйти", 'url_name': get_url_menu('logout'), 'id': '32', 'class': 'fa-sign-out'},
            },
        ]
    else:
        main_menu = [
            {'name': "Главная", 'url_name': get_url_menu('index'), 'class': 'fa-home'},
            {'name': "Альбомы", 'url_name': get_url_menu('show_albums_list'), 'class': 'fa-folder-open', 'id': '1'},
            {'name': "Фото", 'url_name': get_url_menu('show_photos_list'), 'class': 'fa-file-image-o', 'id': '2'},
            {'name': "Войти", 'class': 'fa-sign-in', 'id': '3',
            'sub1': {'name': "Войти", 'url_name': '#', 'id': 'window', 'class': 'fa-sign-in'},
            'sub2': {'name': "Присоединиться", 'url_name': get_url_menu('registration'), 'id': '32', 'class': 'fa-sign-in'},
            },
        ]
    return main_menu

def get_url_menu(link, param=None):
    if param:
        return reverse(link, kwargs={'user_id': param})
    else:
        return reverse(link)



@register.simple_tag(name='get_username')
def user_name(g_user):
    if g_user:
        if g_user.first_name:
            username = g_user.first_name
            if g_user.last_name:
                username = username + ' ' + g_user.last_name
        else:
            username = g_user.username
    else:
        username = "не определен"
    return username

@register.simple_tag(name='get_alb_cover')
def album_cover(alb):
    """
        Функция возвращает фото обложки альбома
        это первая фото которую можно получить
    """


    if Photo.objects.filter(ph_album=alb).exists():
        cover = Photo.objects.filter(ph_album=alb).first().ph_file.url
    else:
        cover = '/media/img/no_image.png'

    return cover


@register.simple_tag(name='get_photo_count')
def ph_count(alb):
    """    Подсчет количества фото в альбоме   """
    count = Photo.objects.filter(ph_album=alb).count()
    return count

@register.simple_tag(name='get_alb_access')
def alb_access(var_access):
    """    Отображение доступа к альбому   """
    if var_access:
        ico = "fa-unlock"
        text = 'Открытый доступ'
    else:
        ico = "fa-lock"
        text = 'Приватный доступ'
    return ico, text

@register.simple_tag(name='in_month')
def mon(num):
    """    Определить месяц по его номеру   """
    months = {1: 'в январе', 2: 'в феврале', 3: 'в марте', 4: 'в апреле', 5: 'в мае', 6: 'в июне', 7: 'в июле',
              8: 'в августе', 9: 'в сентябре', 10: 'в октябре', 11: 'в ноябре', 12: 'в декабре'}
    return months[num]
