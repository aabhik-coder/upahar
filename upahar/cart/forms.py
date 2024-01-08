# forms.py
from django import forms

class CheckoutForm(forms.Form):
    address = forms.CharField(max_length=100, required=True)
    phone = forms.CharField(max_length=20, required=True)
    amount = forms.CharField(widget=forms.HiddenInput())
    purchase_order_id = forms.CharField(widget=forms.HiddenInput())
    return_url = forms.CharField(widget=forms.HiddenInput())
    fname = forms.CharField(widget=forms.HiddenInput())
    email = forms.CharField(widget=forms.HiddenInput())
    