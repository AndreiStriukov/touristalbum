import json
from django import template
from django.shortcuts import get_object_or_404
from album.models import *

from django.utils.translation import get_language

register = template.Library()


# Переделка на JSON

def get_url_menu(link, param=None):
    """Функция для генерации URL. Если передан параметр, он используется в URL."""
    if link == '#':  # Проверка на ссылку-заглушку
        return '#'
    
    if param:
        return reverse(link, kwargs={'user_id': param})
    else:
        return reverse(link)

@register.simple_tag()
def load_menu_json(user=None):
    """Загрузка меню для пользователя или гостя."""
    # Загрузка JSON структуры
    with open('menu/menu_structure.json', 'r', encoding='utf-8') as structure_file:
        menu_data = json.load(structure_file)
    
    # Определение меню для авторизованного пользователя или гостя
    if user and user.id:
        menu_structure = menu_data.get('main_menu_user', [])
    else:
        menu_structure = menu_data.get('main_menu_guest', [])
    
    # Определение текущего языка
    current_lang = get_language()
    language_files = {
        'ru': 'menu/menu_ru.json',
        'en': 'menu/menu_en.json',
    }

    language_file = language_files.get(current_lang, 'menu/menu_en.json')
    with open(language_file, 'r', encoding='utf-8') as text_file:
        menu = json.load(text_file)

    # Объединение структуры и текстов
    for i, item in enumerate(menu_structure):
        item['name'] = menu['main_menu_user'][i]['name'] if user and user.id else menu['main_menu_guest'][i]['name']
        
        # Генерация ссылок через get_url_menu, пропуская элементы с '#'
        if 'url_name' in item:
            if item['url_name'] == '#':
                item['url_name'] = '#'
            elif '{user_id}' in item['url_name'] and user:
                item['url_name'] = item['url_name'].replace('{user_id}', str(user.id))
                item['url_name'] = get_url_menu(item['url_name'], user.id)
            else:
                item['url_name'] = get_url_menu(item['url_name'])
        
        # Обработка подменю
        for sub_key in ['sub1', 'sub2', 'sub3']:
            if sub_key in item:
                item[sub_key]['name'] = menu['main_menu_user'][i][sub_key]['name'] if user and user.id else menu['main_menu_guest'][i][sub_key]['name']
                if item[sub_key]['url_name'] == '#':
                    item[sub_key]['url_name'] = '#'
                elif '{user_id}' in item[sub_key]['url_name'] and user:
                    item[sub_key]['url_name'] = item[sub_key]['url_name'].replace('{user_id}', str(user.id))
                    item[sub_key]['url_name'] = get_url_menu(item[sub_key]['url_name'], user.id)
                else:
                    item[sub_key]['url_name'] = get_url_menu(item[sub_key]['url_name'])

    return menu_structure


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
