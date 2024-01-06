# forms.py
from django import forms

class CheckoutForm(forms.Form):
    address = forms.CharField(max_length=100, required=True)
    phone = forms.CharField(max_length=20, required=True)
    # Add other fields as needed