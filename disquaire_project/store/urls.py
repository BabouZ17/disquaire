from django.urls import path

from . import views

app_name = 'store'

urlpatterns = [
    path('', views.home, name='home'),
    path('album/<int:album_id>', views.album, name='album'),
    #path('album/<int:album_id>/booking', views.post_booking, name='post_booking',
    path('albums/', views.albums, name='albums'),
    path('artist/<int:artist_id>', views.artist, name='artist'),
    path('artists/', views.artists, name='artists'),
    path('search/', views.search, name='search'),
    path('contact/', views.contact, name='contact'),
]
