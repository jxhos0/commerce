from django import forms
from .models import *

class NewListingForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all())
    auction_duration = forms.IntegerField()

    class Meta:
        model = Listing
        exclude = ['end_dateTime', 'seller']