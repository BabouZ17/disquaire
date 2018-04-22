from django import forms

class BookingForm(forms.Form):
    name = forms.CharField(label='Name:', max_length=100)
    email = forms.EmailField(label='Email:', max_length=100)

class SearchForm(forms.Form):
    search = forms.CharField(label='Search:', max_length=200)
