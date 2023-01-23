import base64

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):

    CATEGORIES = [
        ('FA', 'Fashion'),
        ('TO', 'Toys'),
        ('EL', 'Electronics'),
        ('HO', 'Home')
    ]

    title = models.CharField(max_length=64, blank=False)
    description = models.TextField(null=False, blank=False)
    bid = models.FloatField(null=False)
    category = models.CharField(max_length=2, choices=CATEGORIES, null=True, default=None)
    image = models.BinaryField(null=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listing")


class Bid(models.Model):
    pass

class Comment(models.Model):
    pass