from django import forms
from django.forms import ModelForm
from .models import *

class CartForm(forms.Form):
    potency = forms.ChoiceField()
    quantity = forms.IntegerField(max_value=20 , min_value=1, initial=1)
    potency.widget.attrs.update({'class':'form-control mb-3'})
    quantity.widget.attrs.update({'class': 'form-control mb-3'})