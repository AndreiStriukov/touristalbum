import json
from django import template
from django.urls import reverse
from django.utils.translation import get_language
from album.models import *

from django.urls import NoReverseMatch

register = template.Library()

# Функция для загрузки и обработки структуры меню
def load_menu_json(menu_key, menu_file, user=None):
    # Загрузка структуры меню из JSON
    with open(f'menu/{menu_file}', 'r', encoding='utf-8') as structure_file:
        menu_data = json.load(structure_file)

    # Определение, какой файл с текстами загрузить в зависимости от языка
    current_lang = get_language()
    language_files = {
        'ru': 'menu/menu_ru.json',
        'en': 'menu/menu_en.json',
        'de': 'menu/menu_de.json',
        'pl': 'menu/menu_pl.json'
    }

    language_file = language_files.get(current_lang, 'menu/menu_en.json')

    # Загрузка текста для текущего языка
    with open(language_file, 'r', encoding='utf-8') as text_file:
        menu = json.load(text_file)

    # Получение структуры меню (пользователь или гость)
    menu_structure = menu_data.get(menu_key, [])

    # Замена плейсхолдеров и генерация URL
    for item in menu_structure:
        item['name'] = menu.get(item['name'], item['name'])  # Перевод имени
        
        # Генерация URL по имени маршрута, если это не '#'
        if 'url_name' in item and item['url_name'] != '#':
            if '{user_id}' in item['url_name'] and user:
                item['url_name'] = item['url_name'].replace('{user_id}', str(user.id))
            item['url_name'] = reverse(item['url_name'])  # Генерация URL по имени маршрута
        
        # Проверка на наличие подменю и замена плейсхолдеров для подменю
        for sub_key in ['sub1', 'sub2', 'sub3']:
            if sub_key in item:
                item[sub_key]['name'] = menu.get(item[sub_key]['name'], item[sub_key]['name']).replace(
                    '{username}', user.username if user else ''
                )
                
                # Генерация URL для подменю, если это не '#'
                if 'url_name' in item[sub_key] and item[sub_key]['url_name'] != '#':
                    if '{user_id}' in item[sub_key]['url_name'] and user:
                        # Заменяем {user_id} на реальный user.id
                        item[sub_key]['url_name'] = item[sub_key]['url_name'].replace('{user_id}', str(user.id))
                        # Получаем имя шаблона URL, например 'user_albums_list', без ID
                        url_name = item[sub_key]['url_name'].split('/')[0]
                        # Используем reverse с параметром user_id
                        item[sub_key]['url_name'] = reverse(url_name, kwargs={'user_id': user.id})
                    else:
                        # Для других ссылок, которые не содержат {user_id}
                        item[sub_key]['url_name'] = reverse(item[sub_key]['url_name'])


    return menu_structure

# Тег для главного меню
@register.simple_tag()
def get_main_menu(user=None):
    menu_key = 'main_menu_user' if user and user.id else 'main_menu_guest'
    return load_menu_json(menu_key, 'menu_structure.json', user)

# Тег для breadcrumb меню
@register.simple_tag()
def get_breadcrumbs_menu(user=None, menu_key='album_list'):
    return load_menu_json(menu_key, 'breadcrumbs_structure.json', user)

