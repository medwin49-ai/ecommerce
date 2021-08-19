from django import forms
from django.forms import ModelForm
from django.forms.widgets import HiddenInput
from .models import *

class CartForm(forms.Form):
    potency = forms.ChoiceField()
    quantity = forms.IntegerField(max_value=20 , min_value=1, initial=1)
    potency.widget.attrs.update({'class':'form-control mb-3'})
    quantity.widget.attrs.update({'class': 'form-control mb-3'})

class HomeCartForm(forms.Form):
    potency = forms.IntegerField()

class CartQuantityItem(forms.Form):
    potency = forms.IntegerField()
    btn = forms.IntegerField()

class DeleteButton(forms.Form):
    potency = forms.IntegerField()

class SuccessForm(forms.Form):
    order_id = forms.CharField()
