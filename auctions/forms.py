from django import forms
from .models import *

class NewListingForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all())

    class Meta:
        model = Listing
        fields = "__all__"