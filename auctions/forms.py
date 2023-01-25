from django import forms

from .models import Listing


class NewListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ("title", "description", "category", "image")

        # labels = {"bid": "Starting bid"}
