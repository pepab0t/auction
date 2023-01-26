from typing import Optional

from django import template
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

from .apps import AuctionsConfig

register = template.Library()

class User(AbstractUser):
    id = models.AutoField(primary_key=True)



class Listing(models.Model):

    CATEGORIES = [
        ("FA", "Fashion"),
        ("TO", "Toys"),
        ("EL", "Electronics"),
        ("HO", "Home"),
        ("OT", "Other")
    ]

    id = models.AutoField(primary_key=True)

    title = models.CharField(max_length=64, blank=False, unique=True)
    description = models.TextField(null=False, blank=False)
    category = models.CharField(max_length=2, choices=CATEGORIES, null=False, default="OT")
    image = models.ImageField(upload_to=settings.MEDIA_ROOT, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listing")

    active = models.BooleanField(null=False, default=True)

    winner = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="wins", default=None, null=True, blank=True)

    def close(self, winner: Optional[User] = None):
        self.active = False
        if winner is not None:
            self.winner = winner
        self.save()

    @register.filter
    def by_active(listings, active):
        return listings.filter(active=active)

class Bid(models.Model):
    id = models.AutoField(primary_key=True)

    value = models.FloatField(null=False, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")

class Comment(models.Model):
    id = models.AutoField(primary_key=True)

    text = models.TextField(null=False, blank=False)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")

    created = models.DateTimeField(auto_now_add=True)

class Wishlist(models.Model):
    id = models.AutoField(primary_key=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="wishlist")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="wishlist")

