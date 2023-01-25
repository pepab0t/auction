import base64

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

from .apps import AuctionsConfig


class User(AbstractUser):
    id = models.IntegerField(primary_key=True)



class Listing(models.Model):

    CATEGORIES = [
        ("FA", "Fashion"),
        ("TO", "Toys"),
        ("EL", "Electronics"),
        ("HO", "Home"),
    ]

    id = models.AutoField(primary_key=True)

    title = models.CharField(max_length=64, blank=False)
    description = models.TextField(null=False, blank=False)
    category = models.CharField(max_length=2, choices=CATEGORIES, null=True, blank=True)
    image = models.ImageField(upload_to=settings.MEDIA_ROOT, null=True, default=None, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listing")

class Bid(models.Model):
    id = models.AutoField(primary_key=True)

    value = models.FloatField(null=False, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")

class Comment(models.Model):
    id = models.IntegerField(primary_key=True)

class Wishlist(models.Model):
    id = models.IntegerField(primary_key=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="wishlist")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="wishlist")
