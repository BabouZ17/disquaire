from django.http import Http404, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages

from .models import Artist, Album, Contact, Booking
from .forms import BookingForm

# Create your views here.
def index(request):
    data = {
        'artists': Artist.objects.all()
    }
    return render(request, 'store/home.html', {"data": data})


def show_album(request, album_id):
    try:
        album = Album.objects.get(id=album_id)
        bookings = Booking.objects.filter(album=Album.objects.get(id=album_id))
    except Album.DoesNotExist:
        messages.error(request, 'Album Does Not Exist !')
        return HttpResponseRedirect(reverse('store:show_albums'))
    form = BookingForm()
    return render(request, 'store/show_album.html', {"album": album, \
    "form": form, "bookings": bookings})

def show_albums(request):
    albums = Album.objects.all()
    return render(request, 'store/show_albums.html', {"albums": albums})

def post_booking(request, album_id):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            contact, contact_created = Contact.objects.get_or_create(\
            name=form.cleaned_data['name'], email=form.cleaned_data['email'])
            album = Album.objects.get(pk=album_id)
            try:
                booking, booking_created = Booking.objects.get_or_create(\
                album=album, contact=contact)
            except IntegrityError:
                pass
            return HttpResponseRedirect(reverse('store:show_album',\
            args=[album_id]))
    else:
        return HttpResponseRedirect(reverse('store:index'))

def show_artist(request, artist_id):
    try:
        artist = Artist.objects.get(id=artist_id)
    except Artist.DoesNotExist:
        messages.error(request, 'Artist Does Not Exist !')
        return HttpResponseRedirect(reverse('store:show_artists'))
    return render(request, 'store/show_artist.html', {"artist": artist})


def show_artists(request):
    artists = Artist.objects.all()
    return render(request, 'store/show_artists.html', {"artists": artists})


def search(request):
    result = ''
    if request.method == 'POST':
        search = request.POST['search']
        # Look for album
        if Album.objects.filter(title__icontains=search).exists():
            form = BookingForm()
            result = Album.objects.filter(title__icontains=search)[0]
            bookings = Booking.objects.filter(album=Album.objects.get(id=result.id))
            return render(request, 'store/show_album.html', \
            {"album": result, "bookings": bookings, "form": form})
        # Look for artist
        elif Artist.objects.filter(name__icontains=search).exists():
            result = Artist.objects.filter(name__icontains=search)[0]
            return render(request, 'store/show_artist.html', \
            {"artist": result})
        else:
            messages.warning(request, 'We didn\'t found what you were looking for!')
            return HttpResponseRedirect(reverse('store:index'))
    else:
        return HttpResponseRedirect(reverse('store:index'))
