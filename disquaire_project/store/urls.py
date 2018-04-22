from django.urls import path

from . import views

app_name = 'store'

urlpatterns = [
    path('', views.index, name='index'),
    path('album/<int:album_id>', views.show_album, name='show_album'),
    path('album/<int:album_id>/booking', views.post_booking, name='post_booking'),
    path('albums/', views.show_albums, name='show_albums'),
    path('artist/<int:artist_id>', views.show_artist, name='show_artist'),
    path('artists/', views.show_artists, name='show_artists'),
    path('search/', views.search, name='search'),
]
