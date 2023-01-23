from django import forms

from .models import Listing


class NewListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ("title", "description", "bid", "category")

        labels = {"bid": "Starting bid"}
