from django import forms

class BookingForm(forms.Form):
    name = forms.CharField(label='Name:', max_length=100)
    email = forms.EmailField(label='Email:', required=True, max_length=100)

class SearchForm(forms.Form):
    search = forms.CharField(label='Search:', max_length=200)

class ContactForm(forms.Form):
    first_name = forms.CharField(label='First Name:', max_length=100)
    last_name = forms.CharField(label='Last Name:', max_length=100)
    email = forms.EmailField(label='Email:', required=True, max_length=200)
    company = forms.CharField(label='Company:', max_length=200)
    message = forms.CharField(label='Message:', widget=forms.Textarea,
    required=True, max_length=500)
