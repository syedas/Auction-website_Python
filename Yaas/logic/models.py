from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _

class Auction(models.Model):
    title = models.CharField(max_length=300, unique=True, blank=False)
    desc = models.TextField(blank=False)
    seller = models.ForeignKey(User, null=False)
    min_price = models.FloatField(null=False, blank=False)
    deadline = models.DateTimeField()
    createdAt = models.DateTimeField(auto_now_add=True)
    modifiedAt = models.DateTimeField(auto_now=True)
    authName = models.CharField(max_length=300)
    tala = models.NullBooleanField()
    is_banned = models.BooleanField(default=False)
    is_locked = models.BooleanField(default=False)
    class Meta:
        db_table = 'auction'


class Bid(models.Model):

    price = models.FloatField(null=False, blank=False)
    time = models.DateTimeField(auto_now_add=True)
    auction = models.IntegerField()
    auctioner = models.CharField(max_length=300)
    bidder = models.CharField(max_length=300)
    class Meta:
        db_table = 'bid'
