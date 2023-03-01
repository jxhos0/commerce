from django import forms
from .models import *

class NewListingForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all())
    auction_duration = forms.IntegerField()

    class Meta:
        model = Listing
        exclude = ['end_dateTime', 'seller']

class NewComment(forms.ModelForm):
    class Meta:
        model = Comment
        fields = "__all__"
        widgets = {
            "listing" : forms.HiddenInput(),
            "commenter" : forms.HiddenInput()
        }


class NewBid(forms.ModelForm):
    class Meta:
        model = Bid
        fields = "__all__"
        widgets = {
            "listing" : forms.HiddenInput(),
            "bidder" : forms.HiddenInput()
        }

