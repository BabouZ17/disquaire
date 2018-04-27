from django import forms

class BookingForm(forms.Form):
    name = forms.CharField(
        label='Name:',
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=True
        )
    email = forms.EmailField(
        label='Email:',
        max_length=100,
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        required=True
        )

class SearchForm(forms.Form):
    search = forms.CharField(
        label='Search:',
        max_length=200
    )

class ContactForm(forms.Form):
    first_name = forms.CharField(
        label='First Name:',
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=True
        )
    last_name = forms.CharField(
        label='Last Name:',
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=True
        )
    email = forms.EmailField(
        label='Email:',
        max_length=100,
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        required=True
        )
    company = forms.CharField(
        label='Company:',
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=True
        )
    message = forms.CharField(
        label='Message:',
        widget=forms.Textarea,
        max_length=500,
        required=True
        )
