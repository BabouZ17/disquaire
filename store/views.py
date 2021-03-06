from django.http import Http404, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from .models import Artist, Album, Contact, Booking
from .forms import BookingForm, ContactForm

# Create your views here.
def home(request):
    context = {
        'artists': Artist.objects.all()
    }
    return render(request, 'store/home.html', {"context": context})

def contact(request):
    if request.method == 'GET':
        form = ContactForm()
        return render(request, 'store/contact.html', {"form": form})
    elif request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Send a mail to the admin
            success = send_mail(
                'Query from: ' + form.cleaned_data['first_name'] + ' ' +
                form.cleaned_data['last_name'] + ' ' +
                form.cleaned_data['email'],
                form.cleaned_data['message'],
                'no-reply@com',
                [settings.EMAIL_HOST_USER],
                fail_silently=False,
            )
            if success:
                messages.success(request, 'Mail Sent To The Admin !')
            else:
                messages.error(request, 'Failed to deliver the mail !')
        else:
            messages.error(request, 'Error in your request ')
        return HttpResponseRedirect(reverse('store:contact'))

def albums(request):
    albums_items = Album.objects.all().order_by('id')
    paginator = Paginator(albums_items, 5)
    page = request.GET.get('page')
    try:
        albums = paginator.page(page)
    except PageNotAnInteger:
        albums = paginator.page(1)
    except EmptyPage:
        albums = paginator.page(paginator.num_pages)
    context = {
        "albums": albums,
        "paginate": True
    }
    return render(request, 'store/albums.html', context)

def album(request, album_id):
    if request.method == 'GET':
        album = get_object_or_404(Album, id=album_id)
        booking = Booking.objects.filter(album=Album.objects.get(id=album_id))
        form = BookingForm()
        context = {
            "album": album,
            "booking": booking,
            "form": form
        }
        return render(request, 'store/album.html', context)
    elif request.method == 'POST':
        form = BookingForm(request.POST)
        try:
            album = Album.objects.get(pk=album_id)
        except Album.DoesNotExist:
            messages.error(request, 'Album does not exists!')
            return HttpResponseRedirect(reverse('store:albums'))
        if form.is_valid() and album.available:
            contact, contact_created = Contact.objects.get_or_create(\
            name=form.cleaned_data['name'], email=form.cleaned_data['email'])
            booking = Booking.objects.filter(album=album, contact=contact)
            if not booking.exists():
                booking = Booking.objects.create(album=album, contact=contact)
                album.available = False
                album.save()
                messages.success(request, 'Booking Done')
            else:
                messages.error(request, 'Already Booked :/')
        else:
            messages.error(request, 'Error with your email address !')
        return HttpResponseRedirect(reverse('store:album',\
        args=[album_id]))

def artist(request, artist_id):
    artist = get_object_or_404(Artist, id=artist_id)
    context = {
        "artist": artist
    }
    return render(request, 'store/artist.html', context)


def artists(request):
    artists_items = Artist.objects.all().order_by('id')
    paginator = Paginator(artists_items, 5)
    page = request.GET.get('page')
    try:
        artists = paginator.page(page)
    except PageNotAnInteger:
        artists = paginator.page(1)
    except EmptyPage:
        artists = paginator.page(paginator.num_pages)
    context = {
        "artists": artists,
        "paginate": True
    }
    return render(request, 'store/artists.html', context)


def search(request):
    result = ''
    if request.method == 'POST':
        search = request.POST['search']
        # Look for album
        if Album.objects.filter(title__icontains=search).exists():
            form = BookingForm()
            result = Album.objects.filter(title__icontains=search)[0]
            bookings = Booking.objects.filter(album=Album.objects.get(id=result.id))
            context = {
                "album": result,
                "bookings": bookings,
                "form": form
            }
            return render(request, 'store/album.html', context)
        # Look for artist
        elif Artist.objects.filter(name__icontains=search).exists():
            result = Artist.objects.filter(name__icontains=search)[0]
            context = {
                "artist": result
            }
            return render(request, 'store/artist.html', context)
        else:
            messages.warning(request, 'We didn\'t found what you were looking for!')
            return HttpResponseRedirect(reverse('store:home'))
    else:
        return HttpResponseRedirect(reverse('store:home'))
