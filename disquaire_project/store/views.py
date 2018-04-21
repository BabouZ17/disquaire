from django.shortcuts import render
from .models import Artist, Album, Contact, Booking

# Create your views here.
def index(request):
    message = 'test'
    data = {
        'artists': Artist.objects.all()
    }
    return render(request, 'home.html', {"message": message, "data": data})

def show(request, item_id):
    message = item_id
    return render(request, 'home.html', {"message": message})

def search(request):
    if request.GET.__contains__('query'):
        item = request.GET['query']
    else:
        item = "Not recognized"
    return render(request, 'search.html', {"message": item})
