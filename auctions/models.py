import base64

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    id = models.IntegerField(primary_key=True)


class Listing(models.Model):

    CATEGORIES = [
        ("FA", "Fashion"),
        ("TO", "Toys"),
        ("EL", "Electronics"),
        ("HO", "Home"),
    ]

    id = models.IntegerField(primary_key=True)

    title = models.CharField(max_length=64, blank=False)
    description = models.TextField(null=False, blank=False)
    bid = models.FloatField(null=False)
    category = models.CharField(max_length=2, choices=CATEGORIES, null=True, blank=True)
    image = models.BinaryField(null=True, default=None, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listing")


class Bid(models.Model):
    id = models.IntegerField(primary_key=True)


class Comment(models.Model):
    id = models.IntegerField(primary_key=True)
