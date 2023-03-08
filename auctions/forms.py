from django import forms
from .models import *

class NewListingForm(forms.ModelForm):
    auction_duration = forms.IntegerField()

    class Meta:
        model = Listing
        exclude = ['end_dateTime', 'seller', 'is_active']

class NewCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = "__all__"
        widgets = {
            "listing" : forms.HiddenInput(),
            "commenter" : forms.HiddenInput()
        }


class NewBidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = "__all__"
        widgets = {
            "listing" : forms.HiddenInput(),
            "bidder" : forms.HiddenInput()
        }

