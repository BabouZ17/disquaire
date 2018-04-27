from django.test import TestCase, tag
from django.urls import reverse
from .models import Album, Artist, Contact, Booking


@tag('home')
class IndexPageTestCase(TestCase):
    @tag('200')
    def test_index_page(self):
        response = self.client.get(reverse('store:home'))
        self.assertEqual(response.status_code, 200)


@tag('album')
class AlbumPageTestCase(TestCase):
    def setUp(self):
        Album.objects.create(title='Test')

    # Test that the album detail page returns 200 if album exists
    @tag('200')
    def test_album_page_returns_200(self):
        album_id = Album.objects.get(title='Test').id
        response = self.client.get(reverse('store:album', args=[album_id]))
        self.assertEqual(response.status_code, 200)

    # Test that the album detail page is redirected if album does not exists
    @tag('404')
    def test_album_page_returns_404(self):
        album_id = Album.objects.get(title='Test').id + 1
        response = self.client.get(reverse('store:album', args=[album_id]))
        self.assertEqual(response.status_code, 404)


@tag('artist')
class ArtistPageTestCase(TestCase):
    def setUp(self):
        Artist.objects.create(name='Bob')

    # Test 200 on artist
    @tag('200')
    def test_artist_page_returns_200(self):
        artist_id = Artist.objects.get(name='Bob').id
        response = self.client.get(reverse('store:artist', args=[artist_id]))
        self.assertEqual(response.status_code, 200)

    # Test 404 on artist
    @tag('404')
    def test_artist_page_returns_404(self):
        artist_id = Artist.objects.get(name='Bob').id + 1
        response = self.client.get(reverse('store:artist', args=[artist_id]))
        self.assertEqual(response.status_code, 404)


@tag('booking')
class BookingPageTestCase(TestCase):
    def setUp(self):
        forever = Album.objects.create(title='Forever')
        one_direction = Artist.objects.create(name='One Direction')
        Contact.objects.create(name='Freddie', email='fred@gmail.com')
        forever.artists.add(one_direction)
        self.contact = Contact.objects.get(name='Freddie')
        self.album = Album.objects.get(title='Forever')

    def test_new_booking(self):
        bookings_before = Booking.objects.count()
        album_id = self.album.id
        name = self.contact.name
        email = self.contact.email
        response = self.client.post(reverse('store:album', args=[album_id]), {
            'name': name,
            'email': email
        })
        bookings_now = Booking.objects.count()
        self.assertEqual(bookings_before + 1, bookings_now)
