from django import forms
from .models import *

class NewListingForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].label = "Category (optional)"
        self.fields['condition'].label = "Condition (optional)"
        self.fields['image'].label = "Image URL (optional)"
        self.fields['starting_price'].label = "Starting Price (in $)"
        self.fields['auction_duration'].label = "Auction Duration"

        self.fields['title'].widget.attrs.update(placeholder="Enter listing title")
        self.fields['description'].widget.attrs.update(placeholder="Enter listing description")
        self.fields['image'].widget.attrs.update(placeholder="Enter listing image URL")
        self.fields['starting_price'].widget.attrs.update(placeholder="Enter listing starting price")

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    auction_duration = forms.ChoiceField(choices=(
        (1,"1 Day"),
        (3, "3 Days"),
        (7, "1 Week"),
        (14, "2 Weeks"),
        (28, "1 Month"),
    ))

    category = forms.ModelChoiceField(queryset=Category.objects.order_by("category_name"))

    class Meta:
        model = Listing
        exclude = ['end_dateTime', 'seller', 'is_active', 'winner']
        
        
        
    

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

