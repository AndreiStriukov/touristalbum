from django.urls import path
from .views.show import *
from .views.change import (
    AddPhoto, del_photo,
    AddAlbum, AlbumUpdate, PhotoUpdate,
)

urlpatterns = [
    path('', HomePage.as_view(), name='index'),

    path('albums/', AlbumListView.as_view(), name='show_albums_list'),
    path('albums/filters', FilterAlbumListView.as_view(), name='filter_albums_list'),
    path('albums/user/<int:user_id>/', AlbumListView.as_view(), name='user_albums_list'),
    path('album/<slug:alb_slug>', AlbumView.as_view(), name='get_album'),

    path('photo/', PhotoListView.as_view(), name='show_photos_list'),
    path('show_album/<slug:alb_slug>', PhotoListView.as_view(), name='show_album_photo'),
    path('gallery/<slug:alb_slug>', GallaryView.as_view(), name='gallery'),
    path('photo/<slug:photo_slug>', PhotoView.as_view(), name='get_photo'),
    path('photos/user/<int:user_id>/', UserPhotoListView.as_view(), name='user_photo_list'),
    path('photos/search/', SearchPhoto.as_view(), name='search_photo'),

    path('add_photo/', AddPhoto.as_view(), name='add_photo'),
    path('add_photo/<slug:alb_slug>', AddPhoto.as_view(), name='add_album_photo'),
    path('albums/add_album/', AddAlbum.as_view(), name='add_album'),
    path('edit_photo/<slug:photo_slug>/', PhotoUpdate.as_view(), name='edit_photo'),
    path('edit_album/<slug:alb_slug>/', AlbumUpdate.as_view(), name='edit_album'),
    path('del_photo/', del_photo, name='del_photo'),
]

