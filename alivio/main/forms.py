from django import forms
from django.forms import ModelForm
from .models import *

class CartForm(forms.Form):
    potency= forms.ChoiceField()
    quantity = forms.IntegerField(max_value = 20 , min_value = 1)

class CartQuantityItem(forms.Form):
    potency= forms.IntegerField()
    btn=forms.IntegerField()

class DeleteButton(forms.Form):
    potency = forms.IntegerField()
