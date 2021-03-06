from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

from datetime import date

# Create your models here.

class Supplier(models.Model):
    name = models.CharField(max_length=128)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name


class Item(models.Model):
    user = models.ForeignKey(User)
    supplier = models.ForeignKey(Supplier)
    name = models.CharField(max_length=128)
    rate = models.DecimalField(default=0, decimal_places=2, max_digits=10)
    cost = models.DecimalField(default=0, decimal_places=2, max_digits=10)
    stock = models.DecimalField(default=0, decimal_places=2, max_digits=10)
    lastUpdated = models.DateField(default=date.today)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

    class Meta:
        unique_together = ("user", "supplier", "name")
