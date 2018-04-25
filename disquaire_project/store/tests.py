from django.test import TestCase
from django.urls import reverse
from .models import Album, Artist, Contact, Booking

class IndexPageTestCase(TestCase):
    def test_index_page(self):
        response = self.client.get(reverse('store:home'))
        self.assertEqual(response.status_code, 200)


class AlbumPageTestCase(TestCase):
    def setUp(self):
        Album.objects.create(title='Test')

    # Test that the album detail page returns 200 if album exists
    def test_album_page_returns_200(self):
        album_id = Album.objects.get(title='Test').id
        response = self.client.get(reverse('store:album', args=[album_id]))
        self.assertEqual(response.status_code, 200)

    # Test that the album detail page is redirected if album does not exists
    def test_album_page_returns_404(self):
        album_id = Album.objects.get(title='Test').id + 1
        response = self.client.get(reverse('store:album', args=[album_id]))
        self.assertEqual(response.status_code, 404)

class ArtistPageTestCase(TestCase):
    def setUp(self):
        Artist.objects.create(name='Bob')

    # Test 200 on artist
    def test_artist_page_returns_200(self):
        artist_id = Artist.objects.get(name='Bob').id
        response = self.client.get(reverse('store:artist', args=[artist_id]))
        self.assertEqual(response.status_code, 200)

    # Test 404 on artist
    def test_artist_page_returns_404(self):
        artist_id = Artist.objects.get(name='Bob').id + 1
        response = self.client.get(reverse('store:artist', args=[artist_id]))
        self.assertEqual(response.status_code, 404)
